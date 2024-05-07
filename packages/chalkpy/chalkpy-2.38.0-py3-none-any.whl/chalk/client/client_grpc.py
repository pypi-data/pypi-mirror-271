from __future__ import annotations

import datetime as dt
import random
from functools import cached_property
from typing import Any, Dict, List, Literal, Mapping, Optional, Sequence, Union, final

import grpc
import grpc.experimental
from google.protobuf import timestamp_pb2

from chalk import DataFrame, EnvironmentId
from chalk._gen.chalk.auth.v1.agent_pb2 import CustomClaim
from chalk._gen.chalk.auth.v1.permissions_pb2 import Permission
from chalk._gen.chalk.common.v1 import online_query_pb2
from chalk._gen.chalk.engine.v1 import query_server_pb2
from chalk._gen.chalk.engine.v1.query_server_pb2_grpc import QueryServiceStub
from chalk._gen.chalk.server.v1.auth_pb2_grpc import AuthServiceStub
from chalk._gen.chalk.server.v1.team_pb2 import CreateServiceTokenRequest, CreateServiceTokenResponse
from chalk._gen.chalk.server.v1.team_pb2_grpc import TeamServiceStub
from chalk.client import ChalkAuthException, FeatureReference
from chalk.client.serialization.protos import OnlineQueryConverter
from chalk.config.auth_config import load_token
from chalk.features._encoding.json import FeatureEncodingOptions
from chalk.features._encoding.outputs import encode_outputs
from chalk.features.feature_set import is_feature_set_class
from chalk.parsed._proto.utils import datetime_to_proto_timestamp, value_to_proto
from chalk.utils import df_utils
from chalk.utils.df_utils import record_batch_to_arrow_ipc
from chalk.utils.grpc import AuthenticatedChalkClientInterceptor, TokenRefresher, UnauthenticatedChalkClientInterceptor


@final
class ChalkGRPCClient:
    def __init__(
        self,
        environment_id: EnvironmentId | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        api_server: str | None = None,
        additional_headers: list[tuple[str, str]] | None = None,
    ):
        additional_headers_nonempty: list[tuple[str, str]] = [] if additional_headers is None else additional_headers
        token_config = load_token(
            client_id=client_id,
            client_secret=client_secret,
            active_environment=environment_id,
            api_server=api_server,
            skip_cache=False,
        )
        if token_config is None:
            raise ChalkAuthException()

        server_host: str = (
            (token_config.apiServer or "api.chalk.ai")
            .removeprefix("https://")
            .removeprefix("http://")
            .removeprefix("www.")
        )

        channel_options: list[tuple[str, str | int]] = [
            ("grpc.max_send_message_length", 1024 * 1024 * 100),  # 100MB
            ("grpc.max_receive_message_length", 1024 * 1024 * 100),  # 100MB
            # https://grpc.io/docs/guides/performance/#python
            (grpc.experimental.ChannelOptions.SingleThreadedUnaryStream, 1),
        ]
        _unauthenticated_server_channel: grpc.Channel = (
            grpc.insecure_channel(
                target=server_host,
                options=channel_options,
            )
            if server_host.startswith("localhost") or server_host.startswith("127.0.0.1")
            else grpc.secure_channel(
                target=server_host,
                credentials=grpc.ssl_channel_credentials(),
                options=channel_options,
            )
        )

        self._auth_stub: AuthServiceStub = AuthServiceStub(
            grpc.intercept_channel(
                _unauthenticated_server_channel,
                UnauthenticatedChalkClientInterceptor(
                    server="go-api",
                    additional_headers=additional_headers_nonempty,
                ),
            )
        )

        token_refresher: TokenRefresher = TokenRefresher(
            auth_stub=self._auth_stub,
            client_id=token_config.clientId,
            client_secret=token_config.clientSecret,
        )

        t = token_refresher.get_token()

        self._environment_id = token_config.activeEnvironment or t.primary_environment
        if self._environment_id is None or self._environment_id == "":
            raise ValueError("No environment specified")

        if self._environment_id not in t.environment_id_to_name:
            lower_env_id = self._environment_id.lower()
            valid = [eid for eid, ename in t.environment_id_to_name.items() if ename.lower() == lower_env_id]
            if len(valid) > 1:
                raise ValueError(f"Multiple environments with name {self._environment_id}: {valid}")
            elif len(valid) == 0:
                raise ValueError(f"No environment with name {self._environment_id}: {t.environment_id_to_name}")
            else:
                self._environment_id = valid[0]

        self._server_channel: grpc.Channel = grpc.intercept_channel(
            _unauthenticated_server_channel,
            AuthenticatedChalkClientInterceptor(
                refresher=token_refresher,
                server="go-api",
                environment_id=self._environment_id,
                additional_headers=additional_headers_nonempty,
            ),
        )

        grpc_url = t.grpc_engines.get(self._environment_id, None)
        engine_headers = additional_headers_nonempty + [("x-chalk-deployment-type", "engine-grpc")]
        self._engine_channel: grpc.Channel | None = (
            None
            if grpc_url is None
            else (
                grpc.intercept_channel(
                    grpc.insecure_channel(
                        target=grpc_url,
                        options=channel_options,
                    )
                    if grpc_url.startswith("localhost") or grpc_url.startswith("127.0.0.1")
                    else grpc.secure_channel(
                        target=grpc_url,
                        credentials=grpc.ssl_channel_credentials(),
                        options=channel_options,
                    ),
                    AuthenticatedChalkClientInterceptor(
                        refresher=token_refresher,
                        environment_id=self._environment_id,
                        server="engine",
                        additional_headers=engine_headers,
                    ),
                )
            )
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self._server_channel.close()
        if self._engine_channel is not None:
            self._engine_channel.close()

    @cached_property
    def _team_stub(self):
        return TeamServiceStub(self._server_channel)

    @cached_property
    def _query_stub(self) -> QueryServiceStub:
        if self._engine_channel is None:
            raise ValueError(f"No engine channel available for environment {self._environment_id}")
        return QueryServiceStub(self._engine_channel)

    def ping_engine(self, num: Optional[int] = None) -> int:
        if num is None:
            num = random.randint(0, 999)
        response = self._query_stub.Ping(query_server_pb2.PingRequest(num=num))
        return response.num

    def online_query(
        self,
        input: Union[Mapping[FeatureReference, Any], Any],
        output: Sequence[FeatureReference] = (),
        now: Optional[dt.datetime] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: Union[bool, Literal["only"]] = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: Optional[float] = None,
    ) -> Any:
        raise NotImplementedError(
            "Online Query not yet implemented for GRPC, use the Bulk Query Endpoint (ChalkGRPCClient.online_query_bulk(...)) with one row of inputs instead."
        )

    def online_query_bulk(
        self,
        input: Union[Mapping[FeatureReference, Sequence[Any]], DataFrame],
        output: Sequence[FeatureReference] = (),
        now: Optional[Sequence[dt.datetime]] = None,
        staleness: Optional[Mapping[FeatureReference, str]] = None,
        tags: Optional[List[str]] = None,
        correlation_id: Optional[str] = None,
        query_name: Optional[str] = None,
        query_name_version: Optional[str] = None,
        include_meta: bool = False,
        meta: Optional[Mapping[str, str]] = None,
        explain: Union[bool, Literal["only"]] = False,
        store_plan_stages: bool = False,
        encoding_options: Optional[FeatureEncodingOptions] = None,
        required_resolver_tags: Optional[List[str]] = None,
        planner_options: Optional[Mapping[str, Union[str, int, bool]]] = None,
        request_timeout: Optional[float] = None,
    ):

        if isinstance(input, DataFrame):
            import pyarrow as pa

            inputs_table: pa.Table = input.to_pyarrow()
            input_batch = df_utils.pa_table_to_recordbatch(inputs_table)
        else:
            import pyarrow as pa

            encoded_inputs = {str(k): v for k, v in input.items()}
            input_batch = pa.RecordBatch.from_pydict(encoded_inputs)
        inputs_bytes = record_batch_to_arrow_ipc(input_batch)
        outputs, _ = encode_outputs(output)

        extra_headers = {}
        if query_name is not None:
            extra_headers["x-chalk-query-name"] = query_name

        now_proto: Optional[List[timestamp_pb2.Timestamp]] = None
        if now is not None:
            now_proto = []
            for ts in now:
                if ts.tzinfo is None:
                    ts = ts.astimezone(tz=dt.timezone.utc)
                now_proto.append(datetime_to_proto_timestamp(ts))

        staleness_encoded = {}
        if staleness is not None:
            for k, v in staleness.items():
                if is_feature_set_class(k):
                    for f in k.features:
                        staleness_encoded[f.root_fqn] = v
                else:
                    staleness_encoded[k] = v

        context_options_dict: Dict[str, Any] = {
            "store_plan_stages": store_plan_stages,
        }
        context_options_dict.update(**(planner_options or {}))
        context_options_proto = {k: value_to_proto(v) for k, v in context_options_dict.items()}
        stub = self._query_stub
        request = online_query_pb2.OnlineQueryBulkRequest(
            inputs_feather=inputs_bytes,
            outputs=[online_query_pb2.OutputExpr(feature_fqn=o) for o in outputs],
            now=now_proto,
            staleness=staleness_encoded,
            context=online_query_pb2.OnlineQueryContext(
                environment=self._environment_id,
                tags=tags,
                required_resolver_tags=required_resolver_tags,
                correlation_id=correlation_id,
                query_name=query_name,
                query_name_version=query_name_version,
                options=context_options_proto,
            ),
            response_options=online_query_pb2.OnlineQueryResponseOptions(
                include_meta=include_meta,
                explain=online_query_pb2.ExplainOptions() if explain else None,
                encoding_options=online_query_pb2.FeatureEncodingOptions(
                    encode_structs_as_objects=encoding_options.encode_structs_as_objects if encoding_options else False
                ),
                metadata=meta,
            ),
            body_type=online_query_pb2.FEATHER_BODY_TYPE_RECORD_BATCHES,
        )
        response = stub.OnlineQueryBulk(request, timeout=request_timeout)
        return OnlineQueryConverter.online_query_bulk_response_decode(response)

    def create_service_token(
        self,
        name: str,
        permissions: list[Permission],
        customer_claims: dict[str, list[str]] | None = None,
    ) -> CreateServiceTokenResponse:
        """Create a service token with a given set of permissions and claims.

        Parameters
        ----------
        name
            The name of your service token.
        permissions
            The permissions that you want your token to have.
        customer_claims
            The customer claims that you want your token to have.
        Returns
        -------
        CreateServiceTokenResponse
            A service token response, including a `client_id` and `client_secret` with
            the specified permissions and customer claims.

        Examples
        --------
        >>> from chalk.client import Permission
        >>> client = ChalkGRPCClient(client_id='test', client_secret='test_secret')
        >>> client.create_service_token(permissions=[Permission.PERMISSION_QUERY_ONLINE])
        """
        return self._team_stub.CreateServiceToken(
            CreateServiceTokenRequest(
                name=name,
                permissions=permissions,
                customer_claims=None
                if customer_claims is None
                else [CustomClaim(key=key, values=values) for key, values in customer_claims.items()],
            )
        )
