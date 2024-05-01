# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.cosmos.gov.v1beta1 import query_pb2 as cosmos_dot_gov_dot_v1beta1_dot_query__pb2

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
        + f' but the generated code in cosmos/gov/v1beta1/query_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class QueryStub(object):
    """Query defines the gRPC querier service for gov module
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Proposal = channel.unary_unary(
                '/cosmos.gov.v1beta1.Query/Proposal',
                request_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalRequest.SerializeToString,
                response_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalResponse.FromString,
                _registered_method=True)
        self.Proposals = channel.unary_unary(
                '/cosmos.gov.v1beta1.Query/Proposals',
                request_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalsRequest.SerializeToString,
                response_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalsResponse.FromString,
                _registered_method=True)
        self.Vote = channel.unary_unary(
                '/cosmos.gov.v1beta1.Query/Vote',
                request_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVoteRequest.SerializeToString,
                response_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVoteResponse.FromString,
                _registered_method=True)
        self.Votes = channel.unary_unary(
                '/cosmos.gov.v1beta1.Query/Votes',
                request_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVotesRequest.SerializeToString,
                response_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVotesResponse.FromString,
                _registered_method=True)
        self.Params = channel.unary_unary(
                '/cosmos.gov.v1beta1.Query/Params',
                request_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString,
                response_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString,
                _registered_method=True)
        self.Deposit = channel.unary_unary(
                '/cosmos.gov.v1beta1.Query/Deposit',
                request_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositRequest.SerializeToString,
                response_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositResponse.FromString,
                _registered_method=True)
        self.Deposits = channel.unary_unary(
                '/cosmos.gov.v1beta1.Query/Deposits',
                request_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositsRequest.SerializeToString,
                response_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositsResponse.FromString,
                _registered_method=True)
        self.TallyResult = channel.unary_unary(
                '/cosmos.gov.v1beta1.Query/TallyResult',
                request_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryTallyResultRequest.SerializeToString,
                response_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryTallyResultResponse.FromString,
                _registered_method=True)


class QueryServicer(object):
    """Query defines the gRPC querier service for gov module
    """

    def Proposal(self, request, context):
        """Proposal queries proposal details based on ProposalID.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Proposals(self, request, context):
        """Proposals queries all proposals based on given status.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Vote(self, request, context):
        """Vote queries voted information based on proposalID, voterAddr.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Votes(self, request, context):
        """Votes queries votes of a given proposal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Params(self, request, context):
        """Params queries all parameters of the gov module.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Deposit(self, request, context):
        """Deposit queries single deposit information based on proposalID, depositor address.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Deposits(self, request, context):
        """Deposits queries all deposits of a single proposal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TallyResult(self, request, context):
        """TallyResult queries the tally of a proposal vote.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Proposal': grpc.unary_unary_rpc_method_handler(
                    servicer.Proposal,
                    request_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalRequest.FromString,
                    response_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalResponse.SerializeToString,
            ),
            'Proposals': grpc.unary_unary_rpc_method_handler(
                    servicer.Proposals,
                    request_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalsRequest.FromString,
                    response_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalsResponse.SerializeToString,
            ),
            'Vote': grpc.unary_unary_rpc_method_handler(
                    servicer.Vote,
                    request_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVoteRequest.FromString,
                    response_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVoteResponse.SerializeToString,
            ),
            'Votes': grpc.unary_unary_rpc_method_handler(
                    servicer.Votes,
                    request_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVotesRequest.FromString,
                    response_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVotesResponse.SerializeToString,
            ),
            'Params': grpc.unary_unary_rpc_method_handler(
                    servicer.Params,
                    request_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryParamsRequest.FromString,
                    response_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryParamsResponse.SerializeToString,
            ),
            'Deposit': grpc.unary_unary_rpc_method_handler(
                    servicer.Deposit,
                    request_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositRequest.FromString,
                    response_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositResponse.SerializeToString,
            ),
            'Deposits': grpc.unary_unary_rpc_method_handler(
                    servicer.Deposits,
                    request_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositsRequest.FromString,
                    response_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositsResponse.SerializeToString,
            ),
            'TallyResult': grpc.unary_unary_rpc_method_handler(
                    servicer.TallyResult,
                    request_deserializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryTallyResultRequest.FromString,
                    response_serializer=cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryTallyResultResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cosmos.gov.v1beta1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query defines the gRPC querier service for gov module
    """

    @staticmethod
    def Proposal(request,
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
            '/cosmos.gov.v1beta1.Query/Proposal',
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalRequest.SerializeToString,
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalResponse.FromString,
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
    def Proposals(request,
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
            '/cosmos.gov.v1beta1.Query/Proposals',
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalsRequest.SerializeToString,
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryProposalsResponse.FromString,
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
    def Vote(request,
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
            '/cosmos.gov.v1beta1.Query/Vote',
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVoteRequest.SerializeToString,
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVoteResponse.FromString,
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
    def Votes(request,
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
            '/cosmos.gov.v1beta1.Query/Votes',
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVotesRequest.SerializeToString,
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryVotesResponse.FromString,
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
            '/cosmos.gov.v1beta1.Query/Params',
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryParamsRequest.SerializeToString,
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryParamsResponse.FromString,
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
    def Deposit(request,
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
            '/cosmos.gov.v1beta1.Query/Deposit',
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositRequest.SerializeToString,
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositResponse.FromString,
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
    def Deposits(request,
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
            '/cosmos.gov.v1beta1.Query/Deposits',
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositsRequest.SerializeToString,
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryDepositsResponse.FromString,
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
    def TallyResult(request,
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
            '/cosmos.gov.v1beta1.Query/TallyResult',
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryTallyResultRequest.SerializeToString,
            cosmos_dot_gov_dot_v1beta1_dot_query__pb2.QueryTallyResultResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
