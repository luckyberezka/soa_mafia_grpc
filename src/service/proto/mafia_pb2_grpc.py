# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from service.proto import mafia_pb2 as service_dot_proto_dot_mafia__pb2


class MafiaCtlStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.VoteKill = channel.unary_unary(
                '/mafia.MafiaCtl/VoteKill',
                request_serializer=service_dot_proto_dot_mafia__pb2.VoteKillRequest.SerializeToString,
                response_deserializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
                )
        self.CheckRole = channel.unary_unary(
                '/mafia.MafiaCtl/CheckRole',
                request_serializer=service_dot_proto_dot_mafia__pb2.CheckRoleRequest.SerializeToString,
                response_deserializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
                )
        self.PublishData = channel.unary_unary(
                '/mafia.MafiaCtl/PublishData',
                request_serializer=service_dot_proto_dot_mafia__pb2.PublishDataRequest.SerializeToString,
                response_deserializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
                )
        self.GetInfo = channel.unary_unary(
                '/mafia.MafiaCtl/GetInfo',
                request_serializer=service_dot_proto_dot_mafia__pb2.GetInfoRequest.SerializeToString,
                response_deserializer=service_dot_proto_dot_mafia__pb2.GetInfoResponse.FromString,
                )
        self.SwitchTime = channel.unary_unary(
                '/mafia.MafiaCtl/SwitchTime',
                request_serializer=service_dot_proto_dot_mafia__pb2.SwitchTimeResponse.SerializeToString,
                response_deserializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
                )
        self.CreateSession = channel.unary_unary(
                '/mafia.MafiaCtl/CreateSession',
                request_serializer=service_dot_proto_dot_mafia__pb2.CreateSessionRequest.SerializeToString,
                response_deserializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
                )
        self.JoinSession = channel.unary_unary(
                '/mafia.MafiaCtl/JoinSession',
                request_serializer=service_dot_proto_dot_mafia__pb2.JoinSessionRequest.SerializeToString,
                response_deserializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
                )
        self.EventsMonitor = channel.unary_stream(
                '/mafia.MafiaCtl/EventsMonitor',
                request_serializer=service_dot_proto_dot_mafia__pb2.EventsMonitorRequest.SerializeToString,
                response_deserializer=service_dot_proto_dot_mafia__pb2.EventsMonitorResponse.FromString,
                )


class MafiaCtlServicer(object):
    """Missing associated documentation comment in .proto file."""

    def VoteKill(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckRole(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PublishData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SwitchTime(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateSession(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def JoinSession(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EventsMonitor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MafiaCtlServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'VoteKill': grpc.unary_unary_rpc_method_handler(
                    servicer.VoteKill,
                    request_deserializer=service_dot_proto_dot_mafia__pb2.VoteKillRequest.FromString,
                    response_serializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.SerializeToString,
            ),
            'CheckRole': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckRole,
                    request_deserializer=service_dot_proto_dot_mafia__pb2.CheckRoleRequest.FromString,
                    response_serializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.SerializeToString,
            ),
            'PublishData': grpc.unary_unary_rpc_method_handler(
                    servicer.PublishData,
                    request_deserializer=service_dot_proto_dot_mafia__pb2.PublishDataRequest.FromString,
                    response_serializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.SerializeToString,
            ),
            'GetInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetInfo,
                    request_deserializer=service_dot_proto_dot_mafia__pb2.GetInfoRequest.FromString,
                    response_serializer=service_dot_proto_dot_mafia__pb2.GetInfoResponse.SerializeToString,
            ),
            'SwitchTime': grpc.unary_unary_rpc_method_handler(
                    servicer.SwitchTime,
                    request_deserializer=service_dot_proto_dot_mafia__pb2.SwitchTimeResponse.FromString,
                    response_serializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.SerializeToString,
            ),
            'CreateSession': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateSession,
                    request_deserializer=service_dot_proto_dot_mafia__pb2.CreateSessionRequest.FromString,
                    response_serializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.SerializeToString,
            ),
            'JoinSession': grpc.unary_unary_rpc_method_handler(
                    servicer.JoinSession,
                    request_deserializer=service_dot_proto_dot_mafia__pb2.JoinSessionRequest.FromString,
                    response_serializer=service_dot_proto_dot_mafia__pb2.CommonStatusResponse.SerializeToString,
            ),
            'EventsMonitor': grpc.unary_stream_rpc_method_handler(
                    servicer.EventsMonitor,
                    request_deserializer=service_dot_proto_dot_mafia__pb2.EventsMonitorRequest.FromString,
                    response_serializer=service_dot_proto_dot_mafia__pb2.EventsMonitorResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mafia.MafiaCtl', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MafiaCtl(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def VoteKill(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaCtl/VoteKill',
            service_dot_proto_dot_mafia__pb2.VoteKillRequest.SerializeToString,
            service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaCtl/CheckRole',
            service_dot_proto_dot_mafia__pb2.CheckRoleRequest.SerializeToString,
            service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PublishData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaCtl/PublishData',
            service_dot_proto_dot_mafia__pb2.PublishDataRequest.SerializeToString,
            service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaCtl/GetInfo',
            service_dot_proto_dot_mafia__pb2.GetInfoRequest.SerializeToString,
            service_dot_proto_dot_mafia__pb2.GetInfoResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SwitchTime(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaCtl/SwitchTime',
            service_dot_proto_dot_mafia__pb2.SwitchTimeResponse.SerializeToString,
            service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateSession(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaCtl/CreateSession',
            service_dot_proto_dot_mafia__pb2.CreateSessionRequest.SerializeToString,
            service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def JoinSession(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mafia.MafiaCtl/JoinSession',
            service_dot_proto_dot_mafia__pb2.JoinSessionRequest.SerializeToString,
            service_dot_proto_dot_mafia__pb2.CommonStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EventsMonitor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mafia.MafiaCtl/EventsMonitor',
            service_dot_proto_dot_mafia__pb2.EventsMonitorRequest.SerializeToString,
            service_dot_proto_dot_mafia__pb2.EventsMonitorResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
