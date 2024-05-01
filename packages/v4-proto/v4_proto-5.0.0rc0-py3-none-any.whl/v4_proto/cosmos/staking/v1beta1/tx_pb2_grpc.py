# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.cosmos.staking.v1beta1 import tx_pb2 as cosmos_dot_staking_dot_v1beta1_dot_tx__pb2

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
        + f' but the generated code in cosmos/staking/v1beta1/tx_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class MsgStub(object):
    """Msg defines the staking Msg service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateValidator = channel.unary_unary(
                '/cosmos.staking.v1beta1.Msg/CreateValidator',
                request_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCreateValidator.SerializeToString,
                response_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCreateValidatorResponse.FromString,
                _registered_method=True)
        self.EditValidator = channel.unary_unary(
                '/cosmos.staking.v1beta1.Msg/EditValidator',
                request_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgEditValidator.SerializeToString,
                response_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgEditValidatorResponse.FromString,
                _registered_method=True)
        self.Delegate = channel.unary_unary(
                '/cosmos.staking.v1beta1.Msg/Delegate',
                request_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgDelegate.SerializeToString,
                response_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgDelegateResponse.FromString,
                _registered_method=True)
        self.BeginRedelegate = channel.unary_unary(
                '/cosmos.staking.v1beta1.Msg/BeginRedelegate',
                request_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgBeginRedelegate.SerializeToString,
                response_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgBeginRedelegateResponse.FromString,
                _registered_method=True)
        self.Undelegate = channel.unary_unary(
                '/cosmos.staking.v1beta1.Msg/Undelegate',
                request_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUndelegate.SerializeToString,
                response_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUndelegateResponse.FromString,
                _registered_method=True)
        self.CancelUnbondingDelegation = channel.unary_unary(
                '/cosmos.staking.v1beta1.Msg/CancelUnbondingDelegation',
                request_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCancelUnbondingDelegation.SerializeToString,
                response_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCancelUnbondingDelegationResponse.FromString,
                _registered_method=True)
        self.UpdateParams = channel.unary_unary(
                '/cosmos.staking.v1beta1.Msg/UpdateParams',
                request_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUpdateParams.SerializeToString,
                response_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUpdateParamsResponse.FromString,
                _registered_method=True)


class MsgServicer(object):
    """Msg defines the staking Msg service.
    """

    def CreateValidator(self, request, context):
        """CreateValidator defines a method for creating a new validator.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EditValidator(self, request, context):
        """EditValidator defines a method for editing an existing validator.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delegate(self, request, context):
        """Delegate defines a method for performing a delegation of coins
        from a delegator to a validator.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BeginRedelegate(self, request, context):
        """BeginRedelegate defines a method for performing a redelegation
        of coins from a delegator and source validator to a destination validator.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Undelegate(self, request, context):
        """Undelegate defines a method for performing an undelegation from a
        delegate and a validator.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelUnbondingDelegation(self, request, context):
        """CancelUnbondingDelegation defines a method for performing canceling the unbonding delegation
        and delegate back to previous validator.

        Since: cosmos-sdk 0.46
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateParams(self, request, context):
        """UpdateParams defines an operation for updating the x/staking module
        parameters.
        Since: cosmos-sdk 0.47
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MsgServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateValidator': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateValidator,
                    request_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCreateValidator.FromString,
                    response_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCreateValidatorResponse.SerializeToString,
            ),
            'EditValidator': grpc.unary_unary_rpc_method_handler(
                    servicer.EditValidator,
                    request_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgEditValidator.FromString,
                    response_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgEditValidatorResponse.SerializeToString,
            ),
            'Delegate': grpc.unary_unary_rpc_method_handler(
                    servicer.Delegate,
                    request_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgDelegate.FromString,
                    response_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgDelegateResponse.SerializeToString,
            ),
            'BeginRedelegate': grpc.unary_unary_rpc_method_handler(
                    servicer.BeginRedelegate,
                    request_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgBeginRedelegate.FromString,
                    response_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgBeginRedelegateResponse.SerializeToString,
            ),
            'Undelegate': grpc.unary_unary_rpc_method_handler(
                    servicer.Undelegate,
                    request_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUndelegate.FromString,
                    response_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUndelegateResponse.SerializeToString,
            ),
            'CancelUnbondingDelegation': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelUnbondingDelegation,
                    request_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCancelUnbondingDelegation.FromString,
                    response_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCancelUnbondingDelegationResponse.SerializeToString,
            ),
            'UpdateParams': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateParams,
                    request_deserializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUpdateParams.FromString,
                    response_serializer=cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUpdateParamsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cosmos.staking.v1beta1.Msg', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Msg(object):
    """Msg defines the staking Msg service.
    """

    @staticmethod
    def CreateValidator(request,
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
            '/cosmos.staking.v1beta1.Msg/CreateValidator',
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCreateValidator.SerializeToString,
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCreateValidatorResponse.FromString,
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
    def EditValidator(request,
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
            '/cosmos.staking.v1beta1.Msg/EditValidator',
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgEditValidator.SerializeToString,
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgEditValidatorResponse.FromString,
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
    def Delegate(request,
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
            '/cosmos.staking.v1beta1.Msg/Delegate',
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgDelegate.SerializeToString,
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgDelegateResponse.FromString,
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
    def BeginRedelegate(request,
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
            '/cosmos.staking.v1beta1.Msg/BeginRedelegate',
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgBeginRedelegate.SerializeToString,
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgBeginRedelegateResponse.FromString,
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
    def Undelegate(request,
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
            '/cosmos.staking.v1beta1.Msg/Undelegate',
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUndelegate.SerializeToString,
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUndelegateResponse.FromString,
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
    def CancelUnbondingDelegation(request,
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
            '/cosmos.staking.v1beta1.Msg/CancelUnbondingDelegation',
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCancelUnbondingDelegation.SerializeToString,
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgCancelUnbondingDelegationResponse.FromString,
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
    def UpdateParams(request,
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
            '/cosmos.staking.v1beta1.Msg/UpdateParams',
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUpdateParams.SerializeToString,
            cosmos_dot_staking_dot_v1beta1_dot_tx__pb2.MsgUpdateParamsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
