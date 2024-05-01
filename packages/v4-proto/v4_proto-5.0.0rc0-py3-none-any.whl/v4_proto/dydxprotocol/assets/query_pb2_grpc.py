# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.dydxprotocol.assets import query_pb2 as dydxprotocol_dot_assets_dot_query__pb2

GRPC_GENERATED_VERSION = '1.63.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in dydxprotocol/assets/query_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class QueryStub(object):
    """Query defines the gRPC querier service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Asset = channel.unary_unary(
                '/dydxprotocol.assets.Query/Asset',
                request_serializer=dydxprotocol_dot_assets_dot_query__pb2.QueryAssetRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_assets_dot_query__pb2.QueryAssetResponse.FromString,
                _registered_method=True)
        self.AllAssets = channel.unary_unary(
                '/dydxprotocol.assets.Query/AllAssets',
                request_serializer=dydxprotocol_dot_assets_dot_query__pb2.QueryAllAssetsRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_assets_dot_query__pb2.QueryAllAssetsResponse.FromString,
                _registered_method=True)


class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def Asset(self, request, context):
        """Queries a Asset by id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AllAssets(self, request, context):
        """Queries a list of Asset items.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Asset': grpc.unary_unary_rpc_method_handler(
                    servicer.Asset,
                    request_deserializer=dydxprotocol_dot_assets_dot_query__pb2.QueryAssetRequest.FromString,
                    response_serializer=dydxprotocol_dot_assets_dot_query__pb2.QueryAssetResponse.SerializeToString,
            ),
            'AllAssets': grpc.unary_unary_rpc_method_handler(
                    servicer.AllAssets,
                    request_deserializer=dydxprotocol_dot_assets_dot_query__pb2.QueryAllAssetsRequest.FromString,
                    response_serializer=dydxprotocol_dot_assets_dot_query__pb2.QueryAllAssetsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dydxprotocol.assets.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query defines the gRPC querier service.
    """

    @staticmethod
    def Asset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/dydxprotocol.assets.Query/Asset',
            dydxprotocol_dot_assets_dot_query__pb2.QueryAssetRequest.SerializeToString,
            dydxprotocol_dot_assets_dot_query__pb2.QueryAssetResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AllAssets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/dydxprotocol.assets.Query/AllAssets',
            dydxprotocol_dot_assets_dot_query__pb2.QueryAllAssetsRequest.SerializeToString,
            dydxprotocol_dot_assets_dot_query__pb2.QueryAllAssetsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
