# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.dydxprotocol.govplus import tx_pb2 as dydxprotocol_dot_govplus_dot_tx__pb2

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
        + f' but the generated code in dydxprotocol/govplus/tx_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class MsgStub(object):
    """Msg defines the Msg service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SlashValidator = channel.unary_unary(
                '/dydxprotocol.govplus.Msg/SlashValidator',
                request_serializer=dydxprotocol_dot_govplus_dot_tx__pb2.MsgSlashValidator.SerializeToString,
                response_deserializer=dydxprotocol_dot_govplus_dot_tx__pb2.MsgSlashValidatorResponse.FromString,
                _registered_method=True)


class MsgServicer(object):
    """Msg defines the Msg service.
    """

    def SlashValidator(self, request, context):
        """SlashValidator is exposed to allow slashing of a misbehaving validator via
        governance.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MsgServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SlashValidator': grpc.unary_unary_rpc_method_handler(
                    servicer.SlashValidator,
                    request_deserializer=dydxprotocol_dot_govplus_dot_tx__pb2.MsgSlashValidator.FromString,
                    response_serializer=dydxprotocol_dot_govplus_dot_tx__pb2.MsgSlashValidatorResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dydxprotocol.govplus.Msg', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Msg(object):
    """Msg defines the Msg service.
    """

    @staticmethod
    def SlashValidator(request,
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
            '/dydxprotocol.govplus.Msg/SlashValidator',
            dydxprotocol_dot_govplus_dot_tx__pb2.MsgSlashValidator.SerializeToString,
            dydxprotocol_dot_govplus_dot_tx__pb2.MsgSlashValidatorResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
