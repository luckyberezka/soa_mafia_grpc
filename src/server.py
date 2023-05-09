import grpc
import asyncio
import service.proto.mafia_pb2 as mafia_pb2
import service.proto.mafia_pb2_grpc as mafia_pb2_grpc

from defines import *


class GameSession:
    def __init__(self, name, size, owner):
        self.name = name
        self.size = size
        self.owner = owner

        self.time_of_day = DAY
        self.game_state = PREPARING
        self.members_list = list()
        self.internal_roles = dict()
        self.external_roles = dict()

        self.sync_point = asyncio.Condition()
        self.message_queue = list()


def GetJoinMessage(username):
    message = mafia_pb2.EventsMonitorResponse()
    message.format = JOIN
    message.extra = "{} has joined".format(username)
    return message


class MafiaServer(mafia_pb2_grpc.MafiaCtlServicer):
    def __init__(self):
        self.sessions = dict()

    async def EventsMonitor(self, request, context):
        """
        :param request: mafia_pb2.EventsMonitorRequest
        :param context: grpc.aio.ServicerContext
        :return: stream mafia_pb2.EventsMonitorResponse
        """
        iter = 0
        while True:
            if iter >= len(self.sessions[request.session_name].message_queue):
                await asyncio.sleep(0)
                continue
            yield self.sessions[request.session_name].message_queue[iter]
            iter += 1

    async def CreateSession(self, request, context):
        """
        :param request: mafia_pb2.CreateSessionRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """
        if request.name in self.sessions:
            return mafia_pb2.CommonStatusResponse(status=False, info="Session with this name already exists\n")
        self.sessions[request.name] = GameSession(request.name, request.size, request.owner)
        print("Session {} created".format(request.name))
        return mafia_pb2.CommonStatusResponse(status=True, info="Session was successfully created\n")

    async def JoinSession(self, request, context):
        """
        :param request: mafia_pb2.JoinSessionRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """
        if request.session_name not in self.sessions:
            return mafia_pb2.CommonStatusResponse(status=False, info="Session doesn't exists\n")
        if request.username in self.sessions[request.session_name].members_list:
            return mafia_pb2.CommonStatusResponse(status=False, info="Player with such nickname already exists\n")
        if self.sessions[request.session_name].game_state != PREPARING:
            return mafia_pb2.CommonStatusResponse(status=False, info="Session already running\n")
        self.sessions[request.session_name].members_list.append(request.username)
        self.sessions[request.session_name].message_queue.append(GetJoinMessage(request.username))
        if len(self.sessions[request.session_name].members_list) >= self.sessions[request.session_name].size:
            async with self.sessions[request.session_name].sync_point:
                self.sessions[request.session_name].sync_point.notify_all()
            # roles, state
        else:
            async with self.sessions[request.session_name].sync_point:
                await self.sessions[request.session_name].sync_point.wait()
        print("Player {} has joined".format(request.username))
        return mafia_pb2.CommonStatusResponse(status=True, info="Join successful\n") # return role


    async def SwitchTime(self, request, context):
        """
        :param request: mafia_pb2.SwitchTimeRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """

    async def VoteKill(self, request, context):
        """
        :param request: mafia_pb2.VoteKillRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """

    async def CheckRole(self, request, context):
        """
        :param request: mafia_pb2.CheckRoleRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """

    async def PublishData(self, request, context):
        """
        :param request: mafia_pb2.PublishDataRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """

    async def GetInfo(self, request, context):
        """
        :param request: mafia_pb2.GetInfoRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.GetInfoResponse
        """


async def serve(host, port) -> None:
    server = grpc.aio.server()
    mafia_pb2_grpc.add_MafiaCtlServicer_to_server(MafiaServer(), server)
    listen_addr = "{}:{}".format(host, port)
    server.add_insecure_port(listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve(HOST, PORT))
