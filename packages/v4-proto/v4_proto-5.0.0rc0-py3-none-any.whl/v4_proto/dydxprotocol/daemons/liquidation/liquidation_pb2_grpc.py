# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.dydxprotocol.daemons.liquidation import liquidation_pb2 as dydxprotocol_dot_daemons_dot_liquidation_dot_liquidation__pb2

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
        + f' but the generated code in dydxprotocol/daemons/liquidation/liquidation_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class LiquidationServiceStub(object):
    """LiquidationService defines the gRPC service used by liquidation daemon.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.LiquidateSubaccounts = channel.unary_unary(
                '/dydxprotocol.daemons.liquidation.LiquidationService/LiquidateSubaccounts',
                request_serializer=dydxprotocol_dot_daemons_dot_liquidation_dot_liquidation__pb2.LiquidateSubaccountsRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_daemons_dot_liquidation_dot_liquidation__pb2.LiquidateSubaccountsResponse.FromString,
                _registered_method=True)


class LiquidationServiceServicer(object):
    """LiquidationService defines the gRPC service used by liquidation daemon.
    """

    def LiquidateSubaccounts(self, request, context):
        """Sends a list of subaccount ids that are potentially liquidatable.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LiquidationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'LiquidateSubaccounts': grpc.unary_unary_rpc_method_handler(
                    servicer.LiquidateSubaccounts,
                    request_deserializer=dydxprotocol_dot_daemons_dot_liquidation_dot_liquidation__pb2.LiquidateSubaccountsRequest.FromString,
                    response_serializer=dydxprotocol_dot_daemons_dot_liquidation_dot_liquidation__pb2.LiquidateSubaccountsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dydxprotocol.daemons.liquidation.LiquidationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LiquidationService(object):
    """LiquidationService defines the gRPC service used by liquidation daemon.
    """

    @staticmethod
    def LiquidateSubaccounts(request,
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
            '/dydxprotocol.daemons.liquidation.LiquidationService/LiquidateSubaccounts',
            dydxprotocol_dot_daemons_dot_liquidation_dot_liquidation__pb2.LiquidateSubaccountsRequest.SerializeToString,
            dydxprotocol_dot_daemons_dot_liquidation_dot_liquidation__pb2.LiquidateSubaccountsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
