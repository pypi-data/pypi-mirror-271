# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.cosmos.slashing.v1beta1 import query_pb2 as cosmos_dot_slashing_dot_v1beta1_dot_query__pb2

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
        + f' but the generated code in cosmos/slashing/v1beta1/query_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class QueryStub(object):
    """Query provides defines the gRPC querier service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Params = channel.unary_unary(
                '/cosmos.slashing.v1beta1.Query/Params',
                request_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString,
                response_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString,
                _registered_method=True)
        self.SigningInfo = channel.unary_unary(
                '/cosmos.slashing.v1beta1.Query/SigningInfo',
                request_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoRequest.SerializeToString,
                response_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoResponse.FromString,
                _registered_method=True)
        self.SigningInfos = channel.unary_unary(
                '/cosmos.slashing.v1beta1.Query/SigningInfos',
                request_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosRequest.SerializeToString,
                response_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosResponse.FromString,
                _registered_method=True)


class QueryServicer(object):
    """Query provides defines the gRPC querier service
    """

    def Params(self, request, context):
        """Params queries the parameters of slashing module
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SigningInfo(self, request, context):
        """SigningInfo queries the signing info of given cons address
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SigningInfos(self, request, context):
        """SigningInfos queries signing info of all validators
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Params': grpc.unary_unary_rpc_method_handler(
                    servicer.Params,
                    request_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsRequest.FromString,
                    response_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsResponse.SerializeToString,
            ),
            'SigningInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.SigningInfo,
                    request_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoRequest.FromString,
                    response_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoResponse.SerializeToString,
            ),
            'SigningInfos': grpc.unary_unary_rpc_method_handler(
                    servicer.SigningInfos,
                    request_deserializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosRequest.FromString,
                    response_serializer=cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cosmos.slashing.v1beta1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query provides defines the gRPC querier service
    """

    @staticmethod
    def Params(request,
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
            '/cosmos.slashing.v1beta1.Query/Params',
            cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString,
            cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString,
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
    def SigningInfo(request,
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
            '/cosmos.slashing.v1beta1.Query/SigningInfo',
            cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoRequest.SerializeToString,
            cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfoResponse.FromString,
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
    def SigningInfos(request,
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
            '/cosmos.slashing.v1beta1.Query/SigningInfos',
            cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosRequest.SerializeToString,
            cosmos_dot_slashing_dot_v1beta1_dot_query__pb2.QuerySigningInfosResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
