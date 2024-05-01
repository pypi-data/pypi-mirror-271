# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.dydxprotocol.vault import query_pb2 as dydxprotocol_dot_vault_dot_query__pb2

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
        + f' but the generated code in dydxprotocol/vault/query_pb2_grpc.py depends on'
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
        self.Params = channel.unary_unary(
                '/dydxprotocol.vault.Query/Params',
                request_serializer=dydxprotocol_dot_vault_dot_query__pb2.QueryParamsRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_vault_dot_query__pb2.QueryParamsResponse.FromString,
                _registered_method=True)
        self.Vault = channel.unary_unary(
                '/dydxprotocol.vault.Query/Vault',
                request_serializer=dydxprotocol_dot_vault_dot_query__pb2.QueryVaultRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_vault_dot_query__pb2.QueryVaultResponse.FromString,
                _registered_method=True)
        self.AllVaults = channel.unary_unary(
                '/dydxprotocol.vault.Query/AllVaults',
                request_serializer=dydxprotocol_dot_vault_dot_query__pb2.QueryAllVaultsRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_vault_dot_query__pb2.QueryAllVaultsResponse.FromString,
                _registered_method=True)
        self.OwnerShares = channel.unary_unary(
                '/dydxprotocol.vault.Query/OwnerShares',
                request_serializer=dydxprotocol_dot_vault_dot_query__pb2.QueryOwnerSharesRequest.SerializeToString,
                response_deserializer=dydxprotocol_dot_vault_dot_query__pb2.QueryOwnerSharesResponse.FromString,
                _registered_method=True)


class QueryServicer(object):
    """Query defines the gRPC querier service.
    """

    def Params(self, request, context):
        """Queries the Params.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Vault(self, request, context):
        """Queries a Vault by type and number.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AllVaults(self, request, context):
        """Queries all vaults.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def OwnerShares(self, request, context):
        """Queries owner shares of a vault.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Params': grpc.unary_unary_rpc_method_handler(
                    servicer.Params,
                    request_deserializer=dydxprotocol_dot_vault_dot_query__pb2.QueryParamsRequest.FromString,
                    response_serializer=dydxprotocol_dot_vault_dot_query__pb2.QueryParamsResponse.SerializeToString,
            ),
            'Vault': grpc.unary_unary_rpc_method_handler(
                    servicer.Vault,
                    request_deserializer=dydxprotocol_dot_vault_dot_query__pb2.QueryVaultRequest.FromString,
                    response_serializer=dydxprotocol_dot_vault_dot_query__pb2.QueryVaultResponse.SerializeToString,
            ),
            'AllVaults': grpc.unary_unary_rpc_method_handler(
                    servicer.AllVaults,
                    request_deserializer=dydxprotocol_dot_vault_dot_query__pb2.QueryAllVaultsRequest.FromString,
                    response_serializer=dydxprotocol_dot_vault_dot_query__pb2.QueryAllVaultsResponse.SerializeToString,
            ),
            'OwnerShares': grpc.unary_unary_rpc_method_handler(
                    servicer.OwnerShares,
                    request_deserializer=dydxprotocol_dot_vault_dot_query__pb2.QueryOwnerSharesRequest.FromString,
                    response_serializer=dydxprotocol_dot_vault_dot_query__pb2.QueryOwnerSharesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'dydxprotocol.vault.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query defines the gRPC querier service.
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
            '/dydxprotocol.vault.Query/Params',
            dydxprotocol_dot_vault_dot_query__pb2.QueryParamsRequest.SerializeToString,
            dydxprotocol_dot_vault_dot_query__pb2.QueryParamsResponse.FromString,
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
    def Vault(request,
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
            '/dydxprotocol.vault.Query/Vault',
            dydxprotocol_dot_vault_dot_query__pb2.QueryVaultRequest.SerializeToString,
            dydxprotocol_dot_vault_dot_query__pb2.QueryVaultResponse.FromString,
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
    def AllVaults(request,
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
            '/dydxprotocol.vault.Query/AllVaults',
            dydxprotocol_dot_vault_dot_query__pb2.QueryAllVaultsRequest.SerializeToString,
            dydxprotocol_dot_vault_dot_query__pb2.QueryAllVaultsResponse.FromString,
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
    def OwnerShares(request,
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
            '/dydxprotocol.vault.Query/OwnerShares',
            dydxprotocol_dot_vault_dot_query__pb2.QueryOwnerSharesRequest.SerializeToString,
            dydxprotocol_dot_vault_dot_query__pb2.QueryOwnerSharesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
