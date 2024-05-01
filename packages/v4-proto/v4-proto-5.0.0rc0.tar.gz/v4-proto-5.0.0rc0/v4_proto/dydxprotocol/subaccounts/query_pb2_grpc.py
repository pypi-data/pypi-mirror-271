# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.dydxprotocol.subaccounts import query_pb2 as dydxprotocol_dot_subaccounts_dot_query__pb2

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
        + f' but the generated code in dydxprotocol/subaccounts/query_pb2_grpc.py depends on'
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
        self.Subaccount = channel.unary_unary(
                '/dydxprotocol.subaccounts.Query/Subaccount',
                request_serializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryGetSubaccountRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QuerySubaccountResponse.FromString,
                _registered_method=True)
        self.SubaccountAll = channel.unary_unary(
                '/dydxprotocol.subaccounts.Query/SubaccountAll',
                request_serializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryAllSubaccountRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QuerySubaccountAllResponse.FromString,
                _registered_method=True)
        self.GetWithdrawalAndTransfersBlockedInfo = channel.unary_unary(
                '/dydxprotocol.subaccounts.Query/GetWithdrawalAndTransfersBlockedInfo',
                request_serializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryGetWithdrawalAndTransfersBlockedInfoRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryGetWithdrawalAndTransfersBlockedInfoResponse.FromString,
                _registered_method=True)
        self.CollateralPoolAddress = channel.unary_unary(
                '/dydxprotocol.subaccounts.Query/CollateralPoolAddress',
                request_serializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryCollateralPoolAddressRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryCollateralPoolAddressResponse.FromString,
                _registered_method=True)


class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def Subaccount(self, request, context):
        """Queries a Subaccount by id
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubaccountAll(self, request, context):
        """Queries a list of Subaccount items.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetWithdrawalAndTransfersBlockedInfo(self, request, context):
        """Queries information about whether withdrawal and transfers are blocked, and
        if so which block they are re-enabled on.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CollateralPoolAddress(self, request, context):
        """Queries the collateral pool account address for a perpetual id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Subaccount': grpc.unary_unary_rpc_method_handler(
                    servicer.Subaccount,
                    request_deserializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryGetSubaccountRequest.FromString,
                    response_serializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QuerySubaccountResponse.SerializeToString,
            ),
            'SubaccountAll': grpc.unary_unary_rpc_method_handler(
                    servicer.SubaccountAll,
                    request_deserializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryAllSubaccountRequest.FromString,
                    response_serializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QuerySubaccountAllResponse.SerializeToString,
            ),
            'GetWithdrawalAndTransfersBlockedInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetWithdrawalAndTransfersBlockedInfo,
                    request_deserializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryGetWithdrawalAndTransfersBlockedInfoRequest.FromString,
                    response_serializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryGetWithdrawalAndTransfersBlockedInfoResponse.SerializeToString,
            ),
            'CollateralPoolAddress': grpc.unary_unary_rpc_method_handler(
                    servicer.CollateralPoolAddress,
                    request_deserializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryCollateralPoolAddressRequest.FromString,
                    response_serializer=dydxprotocol_dot_subaccounts_dot_query__pb2.QueryCollateralPoolAddressResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dydxprotocol.subaccounts.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query defines the gRPC querier service.
    """

    @staticmethod
    def Subaccount(request,
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
            '/dydxprotocol.subaccounts.Query/Subaccount',
            dydxprotocol_dot_subaccounts_dot_query__pb2.QueryGetSubaccountRequest.SerializeToString,
            dydxprotocol_dot_subaccounts_dot_query__pb2.QuerySubaccountResponse.FromString,
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
    def SubaccountAll(request,
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
            '/dydxprotocol.subaccounts.Query/SubaccountAll',
            dydxprotocol_dot_subaccounts_dot_query__pb2.QueryAllSubaccountRequest.SerializeToString,
            dydxprotocol_dot_subaccounts_dot_query__pb2.QuerySubaccountAllResponse.FromString,
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
    def GetWithdrawalAndTransfersBlockedInfo(request,
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
            '/dydxprotocol.subaccounts.Query/GetWithdrawalAndTransfersBlockedInfo',
            dydxprotocol_dot_subaccounts_dot_query__pb2.QueryGetWithdrawalAndTransfersBlockedInfoRequest.SerializeToString,
            dydxprotocol_dot_subaccounts_dot_query__pb2.QueryGetWithdrawalAndTransfersBlockedInfoResponse.FromString,
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
    def CollateralPoolAddress(request,
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
            '/dydxprotocol.subaccounts.Query/CollateralPoolAddress',
            dydxprotocol_dot_subaccounts_dot_query__pb2.QueryCollateralPoolAddressRequest.SerializeToString,
            dydxprotocol_dot_subaccounts_dot_query__pb2.QueryCollateralPoolAddressResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
