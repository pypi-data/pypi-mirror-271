# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from v4_proto.cosmos.group.v1 import query_pb2 as cosmos_dot_group_dot_v1_dot_query__pb2

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
        + f' but the generated code in cosmos/group/v1/query_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class QueryStub(object):
    """Query is the cosmos.group.v1 Query service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GroupInfo = channel.unary_unary(
                '/cosmos.group.v1.Query/GroupInfo',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupInfoRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupInfoResponse.FromString,
                _registered_method=True)
        self.GroupPolicyInfo = channel.unary_unary(
                '/cosmos.group.v1.Query/GroupPolicyInfo',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPolicyInfoRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPolicyInfoResponse.FromString,
                _registered_method=True)
        self.GroupMembers = channel.unary_unary(
                '/cosmos.group.v1.Query/GroupMembers',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupMembersRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupMembersResponse.FromString,
                _registered_method=True)
        self.GroupsByAdmin = channel.unary_unary(
                '/cosmos.group.v1.Query/GroupsByAdmin',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByAdminRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByAdminResponse.FromString,
                _registered_method=True)
        self.GroupPoliciesByGroup = channel.unary_unary(
                '/cosmos.group.v1.Query/GroupPoliciesByGroup',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByGroupRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByGroupResponse.FromString,
                _registered_method=True)
        self.GroupPoliciesByAdmin = channel.unary_unary(
                '/cosmos.group.v1.Query/GroupPoliciesByAdmin',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByAdminRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByAdminResponse.FromString,
                _registered_method=True)
        self.Proposal = channel.unary_unary(
                '/cosmos.group.v1.Query/Proposal',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalResponse.FromString,
                _registered_method=True)
        self.ProposalsByGroupPolicy = channel.unary_unary(
                '/cosmos.group.v1.Query/ProposalsByGroupPolicy',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalsByGroupPolicyRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalsByGroupPolicyResponse.FromString,
                _registered_method=True)
        self.VoteByProposalVoter = channel.unary_unary(
                '/cosmos.group.v1.Query/VoteByProposalVoter',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVoteByProposalVoterRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVoteByProposalVoterResponse.FromString,
                _registered_method=True)
        self.VotesByProposal = channel.unary_unary(
                '/cosmos.group.v1.Query/VotesByProposal',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByProposalRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByProposalResponse.FromString,
                _registered_method=True)
        self.VotesByVoter = channel.unary_unary(
                '/cosmos.group.v1.Query/VotesByVoter',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByVoterRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByVoterResponse.FromString,
                _registered_method=True)
        self.GroupsByMember = channel.unary_unary(
                '/cosmos.group.v1.Query/GroupsByMember',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByMemberRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByMemberResponse.FromString,
                _registered_method=True)
        self.TallyResult = channel.unary_unary(
                '/cosmos.group.v1.Query/TallyResult',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryTallyResultRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryTallyResultResponse.FromString,
                _registered_method=True)
        self.Groups = channel.unary_unary(
                '/cosmos.group.v1.Query/Groups',
                request_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsRequest.SerializeToString,
                response_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsResponse.FromString,
                _registered_method=True)


class QueryServicer(object):
    """Query is the cosmos.group.v1 Query service.
    """

    def GroupInfo(self, request, context):
        """GroupInfo queries group info based on group id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupPolicyInfo(self, request, context):
        """GroupPolicyInfo queries group policy info based on account address of group policy.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupMembers(self, request, context):
        """GroupMembers queries members of a group by group id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupsByAdmin(self, request, context):
        """GroupsByAdmin queries groups by admin address.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupPoliciesByGroup(self, request, context):
        """GroupPoliciesByGroup queries group policies by group id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupPoliciesByAdmin(self, request, context):
        """GroupPoliciesByAdmin queries group policies by admin address.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Proposal(self, request, context):
        """Proposal queries a proposal based on proposal id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProposalsByGroupPolicy(self, request, context):
        """ProposalsByGroupPolicy queries proposals based on account address of group policy.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VoteByProposalVoter(self, request, context):
        """VoteByProposalVoter queries a vote by proposal id and voter.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VotesByProposal(self, request, context):
        """VotesByProposal queries a vote by proposal id.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VotesByVoter(self, request, context):
        """VotesByVoter queries a vote by voter.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GroupsByMember(self, request, context):
        """GroupsByMember queries groups by member address.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TallyResult(self, request, context):
        """TallyResult returns the tally result of a proposal. If the proposal is
        still in voting period, then this query computes the current tally state,
        which might not be final. On the other hand, if the proposal is final,
        then it simply returns the `final_tally_result` state stored in the
        proposal itself.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Groups(self, request, context):
        """Groups queries all groups in state.

        Since: cosmos-sdk 0.47.1
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GroupInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupInfo,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupInfoRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupInfoResponse.SerializeToString,
            ),
            'GroupPolicyInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupPolicyInfo,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPolicyInfoRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPolicyInfoResponse.SerializeToString,
            ),
            'GroupMembers': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupMembers,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupMembersRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupMembersResponse.SerializeToString,
            ),
            'GroupsByAdmin': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupsByAdmin,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByAdminRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByAdminResponse.SerializeToString,
            ),
            'GroupPoliciesByGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupPoliciesByGroup,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByGroupRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByGroupResponse.SerializeToString,
            ),
            'GroupPoliciesByAdmin': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupPoliciesByAdmin,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByAdminRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByAdminResponse.SerializeToString,
            ),
            'Proposal': grpc.unary_unary_rpc_method_handler(
                    servicer.Proposal,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalResponse.SerializeToString,
            ),
            'ProposalsByGroupPolicy': grpc.unary_unary_rpc_method_handler(
                    servicer.ProposalsByGroupPolicy,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalsByGroupPolicyRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalsByGroupPolicyResponse.SerializeToString,
            ),
            'VoteByProposalVoter': grpc.unary_unary_rpc_method_handler(
                    servicer.VoteByProposalVoter,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVoteByProposalVoterRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVoteByProposalVoterResponse.SerializeToString,
            ),
            'VotesByProposal': grpc.unary_unary_rpc_method_handler(
                    servicer.VotesByProposal,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByProposalRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByProposalResponse.SerializeToString,
            ),
            'VotesByVoter': grpc.unary_unary_rpc_method_handler(
                    servicer.VotesByVoter,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByVoterRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByVoterResponse.SerializeToString,
            ),
            'GroupsByMember': grpc.unary_unary_rpc_method_handler(
                    servicer.GroupsByMember,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByMemberRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByMemberResponse.SerializeToString,
            ),
            'TallyResult': grpc.unary_unary_rpc_method_handler(
                    servicer.TallyResult,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryTallyResultRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryTallyResultResponse.SerializeToString,
            ),
            'Groups': grpc.unary_unary_rpc_method_handler(
                    servicer.Groups,
                    request_deserializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsRequest.FromString,
                    response_serializer=cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cosmos.group.v1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query is the cosmos.group.v1 Query service.
    """

    @staticmethod
    def GroupInfo(request,
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
            '/cosmos.group.v1.Query/GroupInfo',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupInfoRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupInfoResponse.FromString,
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
    def GroupPolicyInfo(request,
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
            '/cosmos.group.v1.Query/GroupPolicyInfo',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPolicyInfoRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPolicyInfoResponse.FromString,
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
    def GroupMembers(request,
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
            '/cosmos.group.v1.Query/GroupMembers',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupMembersRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupMembersResponse.FromString,
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
    def GroupsByAdmin(request,
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
            '/cosmos.group.v1.Query/GroupsByAdmin',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByAdminRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByAdminResponse.FromString,
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
    def GroupPoliciesByGroup(request,
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
            '/cosmos.group.v1.Query/GroupPoliciesByGroup',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByGroupRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByGroupResponse.FromString,
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
    def GroupPoliciesByAdmin(request,
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
            '/cosmos.group.v1.Query/GroupPoliciesByAdmin',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByAdminRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupPoliciesByAdminResponse.FromString,
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
            '/cosmos.group.v1.Query/Proposal',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalResponse.FromString,
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
    def ProposalsByGroupPolicy(request,
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
            '/cosmos.group.v1.Query/ProposalsByGroupPolicy',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalsByGroupPolicyRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryProposalsByGroupPolicyResponse.FromString,
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
    def VoteByProposalVoter(request,
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
            '/cosmos.group.v1.Query/VoteByProposalVoter',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryVoteByProposalVoterRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryVoteByProposalVoterResponse.FromString,
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
    def VotesByProposal(request,
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
            '/cosmos.group.v1.Query/VotesByProposal',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByProposalRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByProposalResponse.FromString,
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
    def VotesByVoter(request,
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
            '/cosmos.group.v1.Query/VotesByVoter',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByVoterRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryVotesByVoterResponse.FromString,
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
    def GroupsByMember(request,
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
            '/cosmos.group.v1.Query/GroupsByMember',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByMemberRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsByMemberResponse.FromString,
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
            '/cosmos.group.v1.Query/TallyResult',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryTallyResultRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryTallyResultResponse.FromString,
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
    def Groups(request,
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
            '/cosmos.group.v1.Query/Groups',
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsRequest.SerializeToString,
            cosmos_dot_group_dot_v1_dot_query__pb2.QueryGroupsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
