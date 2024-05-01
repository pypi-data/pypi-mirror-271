# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from fintekkers.requests.position import query_position_request_pb2 as fintekkers_dot_requests_dot_position_dot_query__position__request__pb2
from fintekkers.requests.position import query_position_response_pb2 as fintekkers_dot_requests_dot_position_dot_query__position__response__pb2
from fintekkers.requests.util.errors import summary_pb2 as fintekkers_dot_requests_dot_util_dot_errors_dot_summary__pb2


class PositionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Search = channel.unary_stream(
                '/fintekkers.services.position_service.Position/Search',
                request_serializer=fintekkers_dot_requests_dot_position_dot_query__position__request__pb2.QueryPositionRequestProto.SerializeToString,
                response_deserializer=fintekkers_dot_requests_dot_position_dot_query__position__response__pb2.QueryPositionResponseProto.FromString,
                )
        self.ValidateQueryRequest = channel.unary_unary(
                '/fintekkers.services.position_service.Position/ValidateQueryRequest',
                request_serializer=fintekkers_dot_requests_dot_position_dot_query__position__request__pb2.QueryPositionRequestProto.SerializeToString,
                response_deserializer=fintekkers_dot_requests_dot_util_dot_errors_dot_summary__pb2.SummaryProto.FromString,
                )


class PositionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Search(self, request, context):
        """rpc GetByIds (position.QueryPositionRequestProto) returns (position.QueryPositionResponseProto);
        rpc ListIds (transaction.QueryTransactionRequestProto) returns (transaction.QueryTransactionResponseProto);
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidateQueryRequest(self, request, context):
        """rpc ValidateCreateOrUpdate (transaction.CreateTransactionRequestProto) returns (util.errors.SummaryProto);
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PositionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Search': grpc.unary_stream_rpc_method_handler(
                    servicer.Search,
                    request_deserializer=fintekkers_dot_requests_dot_position_dot_query__position__request__pb2.QueryPositionRequestProto.FromString,
                    response_serializer=fintekkers_dot_requests_dot_position_dot_query__position__response__pb2.QueryPositionResponseProto.SerializeToString,
            ),
            'ValidateQueryRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.ValidateQueryRequest,
                    request_deserializer=fintekkers_dot_requests_dot_position_dot_query__position__request__pb2.QueryPositionRequestProto.FromString,
                    response_serializer=fintekkers_dot_requests_dot_util_dot_errors_dot_summary__pb2.SummaryProto.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'fintekkers.services.position_service.Position', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Position(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Search(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/fintekkers.services.position_service.Position/Search',
            fintekkers_dot_requests_dot_position_dot_query__position__request__pb2.QueryPositionRequestProto.SerializeToString,
            fintekkers_dot_requests_dot_position_dot_query__position__response__pb2.QueryPositionResponseProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ValidateQueryRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fintekkers.services.position_service.Position/ValidateQueryRequest',
            fintekkers_dot_requests_dot_position_dot_query__position__request__pb2.QueryPositionRequestProto.SerializeToString,
            fintekkers_dot_requests_dot_util_dot_errors_dot_summary__pb2.SummaryProto.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
