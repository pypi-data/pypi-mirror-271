# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.cosmos.bank.v1beta1 import query_pb2 as cosmos_dot_bank_dot_v1beta1_dot_query__pb2

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
        + f' but the generated code in cosmos/bank/v1beta1/query_pb2_grpc.py depends on'
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
        self.Balance = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/Balance',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryBalanceRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryBalanceResponse.FromString,
                _registered_method=True)
        self.AllBalances = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/AllBalances',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryAllBalancesRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryAllBalancesResponse.FromString,
                _registered_method=True)
        self.SpendableBalances = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/SpendableBalances',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalancesRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalancesResponse.FromString,
                _registered_method=True)
        self.SpendableBalanceByDenom = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/SpendableBalanceByDenom',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalanceByDenomRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalanceByDenomResponse.FromString,
                _registered_method=True)
        self.TotalSupply = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/TotalSupply',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryTotalSupplyRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryTotalSupplyResponse.FromString,
                _registered_method=True)
        self.SupplyOf = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/SupplyOf',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySupplyOfRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySupplyOfResponse.FromString,
                _registered_method=True)
        self.Params = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/Params',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString,
                _registered_method=True)
        self.DenomMetadata = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/DenomMetadata',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataResponse.FromString,
                _registered_method=True)
        self.DenomMetadataByQueryString = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/DenomMetadataByQueryString',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataByQueryStringRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataByQueryStringResponse.FromString,
                _registered_method=True)
        self.DenomsMetadata = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/DenomsMetadata',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomsMetadataRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomsMetadataResponse.FromString,
                _registered_method=True)
        self.DenomOwners = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/DenomOwners',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomOwnersRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomOwnersResponse.FromString,
                _registered_method=True)
        self.SendEnabled = channel.unary_unary(
                '/cosmos.bank.v1beta1.Query/SendEnabled',
                request_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySendEnabledRequest.SerializeToString,
                response_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySendEnabledResponse.FromString,
                _registered_method=True)


class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def Balance(self, request, context):
        """Balance queries the balance of a single coin for a single account.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AllBalances(self, request, context):
        """AllBalances queries the balance of all coins for a single account.

        When called from another module, this query might consume a high amount of
        gas if the pagination field is incorrectly set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SpendableBalances(self, request, context):
        """SpendableBalances queries the spendable balance of all coins for a single
        account.

        When called from another module, this query might consume a high amount of
        gas if the pagination field is incorrectly set.

        Since: cosmos-sdk 0.46
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SpendableBalanceByDenom(self, request, context):
        """SpendableBalanceByDenom queries the spendable balance of a single denom for
        a single account.

        When called from another module, this query might consume a high amount of
        gas if the pagination field is incorrectly set.

        Since: cosmos-sdk 0.47
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TotalSupply(self, request, context):
        """TotalSupply queries the total supply of all coins.

        When called from another module, this query might consume a high amount of
        gas if the pagination field is incorrectly set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SupplyOf(self, request, context):
        """SupplyOf queries the supply of a single coin.

        When called from another module, this query might consume a high amount of
        gas if the pagination field is incorrectly set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Params(self, request, context):
        """Params queries the parameters of x/bank module.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DenomMetadata(self, request, context):
        """DenomsMetadata queries the client metadata of a given coin denomination.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DenomMetadataByQueryString(self, request, context):
        """DenomsMetadata queries the client metadata of a given coin denomination.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DenomsMetadata(self, request, context):
        """DenomsMetadata queries the client metadata for all registered coin
        denominations.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DenomOwners(self, request, context):
        """DenomOwners queries for all account addresses that own a particular token
        denomination.

        When called from another module, this query might consume a high amount of
        gas if the pagination field is incorrectly set.

        Since: cosmos-sdk 0.46
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendEnabled(self, request, context):
        """SendEnabled queries for SendEnabled entries.

        This query only returns denominations that have specific SendEnabled settings.
        Any denomination that does not have a specific setting will use the default
        params.default_send_enabled, and will not be returned by this query.

        Since: cosmos-sdk 0.47
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Balance': grpc.unary_unary_rpc_method_handler(
                    servicer.Balance,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryBalanceRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryBalanceResponse.SerializeToString,
            ),
            'AllBalances': grpc.unary_unary_rpc_method_handler(
                    servicer.AllBalances,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryAllBalancesRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryAllBalancesResponse.SerializeToString,
            ),
            'SpendableBalances': grpc.unary_unary_rpc_method_handler(
                    servicer.SpendableBalances,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalancesRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalancesResponse.SerializeToString,
            ),
            'SpendableBalanceByDenom': grpc.unary_unary_rpc_method_handler(
                    servicer.SpendableBalanceByDenom,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalanceByDenomRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalanceByDenomResponse.SerializeToString,
            ),
            'TotalSupply': grpc.unary_unary_rpc_method_handler(
                    servicer.TotalSupply,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryTotalSupplyRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryTotalSupplyResponse.SerializeToString,
            ),
            'SupplyOf': grpc.unary_unary_rpc_method_handler(
                    servicer.SupplyOf,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySupplyOfRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySupplyOfResponse.SerializeToString,
            ),
            'Params': grpc.unary_unary_rpc_method_handler(
                    servicer.Params,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryParamsRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryParamsResponse.SerializeToString,
            ),
            'DenomMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.DenomMetadata,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataResponse.SerializeToString,
            ),
            'DenomMetadataByQueryString': grpc.unary_unary_rpc_method_handler(
                    servicer.DenomMetadataByQueryString,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataByQueryStringRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataByQueryStringResponse.SerializeToString,
            ),
            'DenomsMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.DenomsMetadata,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomsMetadataRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomsMetadataResponse.SerializeToString,
            ),
            'DenomOwners': grpc.unary_unary_rpc_method_handler(
                    servicer.DenomOwners,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomOwnersRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomOwnersResponse.SerializeToString,
            ),
            'SendEnabled': grpc.unary_unary_rpc_method_handler(
                    servicer.SendEnabled,
                    request_deserializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySendEnabledRequest.FromString,
                    response_serializer=cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySendEnabledResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cosmos.bank.v1beta1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query defines the gRPC querier service.
    """

    @staticmethod
    def Balance(request,
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
            '/cosmos.bank.v1beta1.Query/Balance',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryBalanceRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryBalanceResponse.FromString,
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
    def AllBalances(request,
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
            '/cosmos.bank.v1beta1.Query/AllBalances',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryAllBalancesRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryAllBalancesResponse.FromString,
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
    def SpendableBalances(request,
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
            '/cosmos.bank.v1beta1.Query/SpendableBalances',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalancesRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalancesResponse.FromString,
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
    def SpendableBalanceByDenom(request,
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
            '/cosmos.bank.v1beta1.Query/SpendableBalanceByDenom',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalanceByDenomRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySpendableBalanceByDenomResponse.FromString,
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
    def TotalSupply(request,
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
            '/cosmos.bank.v1beta1.Query/TotalSupply',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryTotalSupplyRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryTotalSupplyResponse.FromString,
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
    def SupplyOf(request,
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
            '/cosmos.bank.v1beta1.Query/SupplyOf',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySupplyOfRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySupplyOfResponse.FromString,
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
            '/cosmos.bank.v1beta1.Query/Params',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString,
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
    def DenomMetadata(request,
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
            '/cosmos.bank.v1beta1.Query/DenomMetadata',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataResponse.FromString,
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
    def DenomMetadataByQueryString(request,
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
            '/cosmos.bank.v1beta1.Query/DenomMetadataByQueryString',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataByQueryStringRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomMetadataByQueryStringResponse.FromString,
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
    def DenomsMetadata(request,
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
            '/cosmos.bank.v1beta1.Query/DenomsMetadata',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomsMetadataRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomsMetadataResponse.FromString,
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
    def DenomOwners(request,
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
            '/cosmos.bank.v1beta1.Query/DenomOwners',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomOwnersRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QueryDenomOwnersResponse.FromString,
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
    def SendEnabled(request,
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
            '/cosmos.bank.v1beta1.Query/SendEnabled',
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySendEnabledRequest.SerializeToString,
            cosmos_dot_bank_dot_v1beta1_dot_query__pb2.QuerySendEnabledResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
