import grpc
import asyncio
import service.proto.mafia_pb2 as mafia_pb2
import service.proto.mafia_pb2_grpc as mafia_pb2_grpc
import os

from random import randint
from defines import *
from collections import defaultdict


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

        self.still_alive = size
        self.mafia_number = 0
        self.civilian_number = 0
        self.officer_number = 0

        self.sync_point = asyncio.Condition()
        self.sync_counter = 0
        self.message_queue = list()
        self.roles_generator = list()

        self.publish_info = list()

        self.votekill = defaultdict(int)


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
            print("{} : {}".format(request.username, self.sessions[request.session_name].message_queue[iter]))
            iter += 1

    async def CreateSession(self, request, context):
        """
        :param request: mafia_pb2.CreateSessionRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """
        if request.name in self.sessions:
            return mafia_pb2.CreateSessionResponse(status=False, info="Session with this name already exists\n")
        if request.size < 4:
            return mafia_pb2.CreateSessionResponse(status=False, info="Session size is too small\n")
        self.sessions[request.name] = GameSession(request.name, request.size, request.owner)
        print("Session {} created".format(request.name))
        self.sessions[request.name].message_queue.append(mafia_pb2.EventsMonitorResponse(format=INFO, extra="You successfully joined to {}".format(request.name)))
        return mafia_pb2.CreateSessionResponse(status=True, info="Session was successfully created\n")

    async def JoinSession(self, request, context):
        """
        :param request: mafia_pb2.JoinSessionRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """
        if request.session_name not in self.sessions:
            return mafia_pb2.JoinSessionResponse(status=False, info="Session doesn't exists\n", role='')
        if request.username in self.sessions[request.session_name].members_list:
            return mafia_pb2.JoinSessionResponse(status=False, info="Player with such nickname already exists\n",
                                                 role='')
        if self.sessions[request.session_name].game_state != PREPARING:
            return mafia_pb2.JoinSessionResponse(status=False, info="Session already running\n", role='')

        current_session = self.sessions[request.session_name]

        current_session.members_list.append(request.username)
        current_session.message_queue.append(mafia_pb2.EventsMonitorResponse(format=JOIN, extra=request.username))
        current_session.external_roles[request.username] = UNKNOWN_ROLE

        if len(current_session.members_list) >= current_session.size:
            async with current_session.sync_point:

                # initializing roles generator
                # mafia
                current_session.mafia_number = 1 + current_session.size // 8
                current_session.officer_number = 1 + current_session.size // 8
                current_session.civilian_number = (current_session.size -
                                                   current_session.mafia_number -
                                                   current_session.officer_number)
                for i in range(current_session.mafia_number):
                    current_session.roles_generator.append(MAFIA_ROLE)
                for i in range(current_session.officer_number):
                    current_session.roles_generator.append(OFFICER_ROLE)
                for i in range(current_session.civilian_number):
                    current_session.roles_generator.append(CIVILIAN_ROLE)

                print(current_session.roles_generator)
                print(current_session.members_list)
                for username in current_session.members_list:
                    role_number = randint(0, len(current_session.roles_generator) - 1)
                    print("ROLES NUMBER: {}".format(role_number))
                    print("SIZE: {}".format(len(current_session.roles_generator)))
                    current_session.internal_roles[username] = current_session.roles_generator[role_number]
                    current_session.roles_generator.pop(role_number)

                current_session.sync_point.notify_all()
        else:
            async with current_session.sync_point:
                await current_session.sync_point.wait()
        print("Player {} has joined".format(request.username))

        return mafia_pb2.JoinSessionResponse(status=True, info="Join successful\n",
                                             role=current_session.internal_roles[request.username],
                                             user_list=current_session.external_roles)  # return role

    async def SwitchTime(self, request, context):
        """
        :param request: mafia_pb2.SwitchTimeRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """

        current_session = self.sessions[request.session_name]
        current_session.sync_counter += 1
        if current_session.sync_counter == current_session.still_alive:
            current_session.sync_counter = 0
            async with current_session.sync_point:
                if len(current_session.publish_info) != 0:
                    publish_user = current_session.publish_info[0]
                    publish_role = current_session.internal_roles[publish_user]
                    current_session.external_roles[publish_user] = publish_role
                    current_session.message_queue.append(mafia_pb2.EventsMonitorResponse(format=INFO,
                                                                                         extra="The officer found out: {} is {}!".format(
                                                                                             publish_user,
                                                                                             publish_role)))
                    current_session.publish_info = list()


                new_spirit = None
                new_spirit_role = None
                max_votes = 0

                for username, votes_number in current_session.votekill.items():
                    if votes_number > max_votes:
                        max_votes = votes_number
                        new_spirit = username

                current_session.votekill = defaultdict(int)

                if new_spirit:
                    new_spirit_role = current_session.internal_roles[new_spirit]

                    if new_spirit_role == MAFIA_ROLE:
                        current_session.mafia_number -= 1
                    elif new_spirit_role == CIVILIAN_ROLE:
                        current_session.civilian_number -= 1
                    elif new_spirit_role == OFFICER_ROLE:
                        current_session.officer_number -= 1

                    current_session.internal_roles[new_spirit] = SPIRIT_ROLE
                    current_session.external_roles[new_spirit] = SPIRIT_ROLE
                    current_session.still_alive -= 1


                if current_session.time_of_day == DAY:
                    current_session.message_queue.append(mafia_pb2.EventsMonitorResponse(format=INFO,
                                                                                         extra="The city falls asleep, the mafia wakes up..."))
                    current_session.time_of_day = NIGHT
                else:
                    current_session.message_queue.append(mafia_pb2.EventsMonitorResponse(format=INFO,
                                                                                         extra="The city wakes up..."))
                    current_session.time_of_day = DAY

                current_session.sync_point.notify_all()

                if new_spirit:
                    current_session.message_queue.append(mafia_pb2.EventsMonitorResponse(format=INFO,
                                                                                         extra="{} was executed, he/she was {}".format(new_spirit, new_spirit_role)))
                else:
                    current_session.message_queue.append(mafia_pb2.EventsMonitorResponse(format=INFO,
                                                                                         extra="No one was killed"))

        else:
            async with current_session.sync_point:
                await current_session.sync_point.wait()

        is_end_game = False
        end_game_message = ""
        if current_session.mafia_number == 0:
            is_end_game = True
            end_game_message = "Game over, civilians win!"
            current_session.message_queue.append(mafia_pb2.EventsMonitorResponse(format=END,
                                                                                 extra=end_game_message))
            print(current_session.mafia_number, current_session.civilian_number)
        elif current_session.mafia_number == current_session.civilian_number:
            is_end_game = True
            end_game_message = "Game over, mafia win!"
            current_session.message_queue.append(mafia_pb2.EventsMonitorResponse(format=END,
                                                                                 extra=end_game_message))
            print(current_session.mafia_number, current_session.civilian_number)



        return mafia_pb2.SwitchTimeResponse(role=current_session.internal_roles[request.username],
                                            is_end_game=is_end_game,
                                            end_game_message=end_game_message,
                                            user_list=current_session.external_roles)

    async def VoteKill(self, request, context):
        """
        :param request: mafia_pb2.VoteKillRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """
        current_session = self.sessions[request.session_name]
        current_session.votekill[request.victim] += 1
        return mafia_pb2.VoteKillResponse(status=True, info="")

    async def CheckRole(self, request, context):
        """
        :param request: mafia_pb2.CheckRoleRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """
        return mafia_pb2.CheckRoleResponse(role=self.sessions[request.session_name].internal_roles[request.suspect])

    async def PublishData(self, request, context):
        """
        :param request: mafia_pb2.PublishDataRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.CommonStatusResponse
        """
        self.sessions[request.session_name].publish_info.append(request.player)
        return mafia_pb2.PublishDataResponse(status=True, info='')

    async def GetInfo(self, request, context):
        """
        :param request: mafia_pb2.GetInfoRequest
        :param context: grpc.aio.ServicerContext
        :return: mafia_pb2.GetInfoResponse
        """

        return mafia_pb2.GetInfoResponse(user_list=self.sessions[request.session_name].external_roles)


async def serve(host, port) -> None:
    server = grpc.aio.server()
    mafia_pb2_grpc.add_MafiaCtlServicer_to_server(MafiaServer(), server)
    listen_addr = "{}:{}".format(host, port)
    server.add_insecure_port(listen_addr)
    print("Running server...")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(serve(os.environ['HOST'], os.environ['PORT']))
