import grpc
import asyncio
from pick import pick
import service.proto.mafia_pb2 as mafia_pb2
import service.proto.mafia_pb2_grpc as mafia_pb2_grpc

from defines import *

from copy import deepcopy
from random import randint


class GameCtl:
    def __init__(self, stub, channel):
        self.stub = stub
        self.channel = channel
        self.username = None
        self.session_name = None
        self.role = None
        self.time_of_day = DAY
        self.user_list = dict()
        self.publish_info = list()

    async def join_to_session(self):
        response = await self.stub.JoinSession(
            mafia_pb2.JoinSessionRequest(session_name=self.session_name, username=self.username)
        )
        if not response.status:
            print("Can't join to session! Reason: {}".format(response.info))
            return False
        self.role = response.role
        self.user_list = response.user_list
        return True

    async def create_session(self):
        session_size = int(input("Session size: "))
        response = await self.stub.CreateSession(
            mafia_pb2.CreateSessionRequest(name=self.session_name, size=session_size, owner=self.username))
        if not response.status:
            print("Can't create session! Reason: {}".format(response.info))
            return False
        return True

    async def start(self):
        self.username = input("Enter your username: ")
        while True:
            entry_mode, index = pick(ENTRY_MODES_LIST, 'Choose entry mode: ', indicator='[x]', default_index=0)
            self.session_name = input("Enter session name: ")
            if entry_mode == CREATE_ROOM:
                if not await self.create_session():
                    continue
                print("Session {} successfully created".format(self.session_name))
                print("Trying to join, waiting for users...")
                if not await self.join_to_session():
                    continue
                print("You successfully joined to {}".format(self.session_name))
                break
            if entry_mode == JOIN_ROOM:
                print("Trying to join, waiting for users...")
                if not await self.join_to_session():
                    continue
                break


async def gameplay(game_ctl):
    await asyncio.sleep(3)
    print("Your role: {}".format(game_ctl.role))

    game_mode, index = pick(GAME_MODE_LIST, "Choose game mode: ", indicator='[x]',
                         default_index=0)

    first_day_flag = True

    while True:
        if game_ctl.time_of_day == DAY:
            if first_day_flag:
                action_list = deepcopy(FIRST_DAY_ACTIONS)
            else:
                action_list = deepcopy(DAY_ACTIONS)

            while True:
                if game_mode == AUTOMATIC:
                    if first_day_flag:
                        break
                    vote_list = list()
                    for username, role in game_ctl.user_list.items():
                        if role != SPIRIT_ROLE and username != game_ctl.username:
                            if game_ctl.role == MAFIA_ROLE and role != MAFIA_ROLE or game_ctl.role != MAFIA_ROLE:
                                vote_list.append(username)

                    if len(vote_list) <= 1:
                        break

                    victim = vote_list[randint(0, len(vote_list) - 1)]

                    await game_ctl.stub.VoteKill(mafia_pb2.VoteKillRequest(session_name=game_ctl.session_name,
                                                                           victim=victim,
                                                                           username=game_ctl.username))
                    print("You voted for the execution of {}".format(victim))
                    break

                input("Press Enter key to choose an action...")

                action, _ = pick(action_list, 'Choose an action: ', indicator='[x]', default_index=0)
                if action == VOTEKILL:
                    action_list.remove(VOTEKILL)
                    vote_list = list()
                    for username, role in game_ctl.user_list.items():
                        if role != SPIRIT_ROLE and username != game_ctl.username:
                            if game_ctl.role == MAFIA_ROLE and role != MAFIA_ROLE or game_ctl.role != MAFIA_ROLE:
                                vote_list.append(username)

                    if len(vote_list) != 0:
                        victim, index = pick(vote_list, 'Choose a player to execute: ', indicator='[x]',
                                             default_index=0)
                        await game_ctl.stub.VoteKill(mafia_pb2.VoteKillRequest(session_name=game_ctl.session_name,
                                                                               victim=victim,
                                                                               username=game_ctl.username))
                        print("You voted for the execution of {}".format(victim))
                    else:
                        print("List of players for execution is empty!")
                if action == GET_INFO:
                    response = await game_ctl.stub.GetInfo(mafia_pb2.GetInfoRequest(session_name=game_ctl.session_name,
                                                                              username=game_ctl.username))
                    for username, role in response.user_list.items():
                        print("Player: {}, Role: {}".format(username, role))
                if action == END_DAY:
                    break
        elif game_ctl.time_of_day == NIGHT and game_ctl.role != CIVILIAN_ROLE:

            if game_ctl.role == MAFIA_ROLE:
                action_list = deepcopy(NIGHT_MAFIA_ACTIONS)
            elif game_ctl.role == OFFICER_ROLE:
                action_list = deepcopy(NIGHT_OFFICER_ACTIONS)
            while True:
                if game_mode == AUTOMATIC and game_ctl.role == MAFIA_ROLE:
                    vote_list = list()
                    for username, role in game_ctl.user_list.items():
                        if role != SPIRIT_ROLE and username != game_ctl.username:
                            if game_ctl.role == MAFIA_ROLE and role != MAFIA_ROLE:
                                vote_list.append(username)

                    if len(vote_list) <= 1:
                        break
                    victim = vote_list[randint(0, len(vote_list) - 1)]

                    await game_ctl.stub.VoteKill(mafia_pb2.VoteKillRequest(session_name=game_ctl.session_name,
                                                                           victim=victim,
                                                                           username=game_ctl.username))
                    print("You voted for the execution of {}".format(victim))
                    break

                if game_mode == AUTOMATIC and game_ctl.role == OFFICER_ROLE:
                    vote_list = list()
                    for username, role in game_ctl.user_list.items():
                        if role != SPIRIT_ROLE and username != game_ctl.username:
                            vote_list.append(username)
                    if len(vote_list) <= 1:
                        break
                    suspect = vote_list[randint(0, len(vote_list) - 1)]
                    response = await game_ctl.stub.CheckRole(
                        mafia_pb2.CheckRoleRequest(session_name=game_ctl.session_name,
                                                   suspect=suspect,
                                                   username=game_ctl.username))
                    print("You recognized {}'s role!, {} is {}!".format(suspect, suspect, response.role))
                    game_ctl.publish_info.append(suspect)
                    response = await game_ctl.stub.PublishData(
                        mafia_pb2.PublishDataRequest(session_name=game_ctl.session_name,
                                                     player=game_ctl.publish_info[0]))
                    break

                input("Press Enter key to choose an action...")
                action, _ = pick(action_list, 'Choose an action: ', indicator='[x]', default_index=0)
                if action == VOTEKILL:
                    action_list.remove(VOTEKILL)
                    vote_list = list()
                    for username, role in game_ctl.user_list.items():
                        if role != SPIRIT_ROLE and username != game_ctl.username:
                            vote_list.append(username)

                    if len(vote_list) != 0:
                        victim, index = pick(vote_list, 'Choose a player to execute: ', indicator='[x]',
                                             default_index=0)
                        await game_ctl.stub.VoteKill(mafia_pb2.VoteKillRequest(session_name=game_ctl.session_name,
                                                                               victim=victim,
                                                                               username=game_ctl.username))
                        print("You voted for the execution of {}".format(victim))
                    else:
                        print("List of players for execution is empty!")

                if action == CHECK_ROLE:
                    action_list.remove(CHECK_ROLE)
                    action_list.append(PUBLISH_DATA)
                    vote_list = list()
                    for username, role in game_ctl.user_list.items():
                        if role != SPIRIT_ROLE and username != game_ctl.username:
                            vote_list.append(username)

                    if len(vote_list) != 0:
                        suspect, index = pick(vote_list, 'Choose a player to execute: ', indicator='[x]',
                                              default_index=0)
                        response = await game_ctl.stub.CheckRole(
                            mafia_pb2.CheckRoleRequest(session_name=game_ctl.session_name,
                                                       suspect=suspect,
                                                       username=game_ctl.username))
                        print("{} is {}!".format(suspect, response.role))
                        game_ctl.publish_info.append(suspect)
                    else:
                        print("List ti check the roles is empty!")

                if action == PUBLISH_DATA:
                    response = await game_ctl.stub.PublishData(mafia_pb2.PublishDataRequest(session_name=game_ctl.session_name,
                                                                                            player=game_ctl.publish_info[0]))
                if action == GET_INFO:
                    response = await game_ctl.stub.GetInfo(mafia_pb2.GetInfoRequest(session_name=game_ctl.session_name,
                                                                              username=game_ctl.username))
                    for username, role in response.user_list.items():
                        print("Player: {}, Role: {}".format(username, role))
                if action == END_NIGHT:
                    break

        response = await game_ctl.stub.SwitchTime(
            mafia_pb2.SwitchTimeRequest(session_name=game_ctl.session_name, username=game_ctl.username))

        await asyncio.sleep(10)

        if response.is_end_game:
            print(response.end_game_message)
            await game_ctl.channel.close()
            exit(0)

        if response.role == SPIRIT_ROLE:
            print("You have been executed :(")
            if game_mode == AUTOMATIC:
                await game_ctl.channel.close()
                exit(0)
            input("Press Enter key to choose an action...")

            action, _ = pick(SPIRIT_ACTIONS, 'Choose an action: ', indicator='[x]', default_index=0)
            if action == EXIT:
                await game_ctl.channel.close()
                exit(0)
            if action == SUSPEND:
                game_ctl.role = SPIRIT_ROLE
            break
        else:
            print("{} has passed, you're still alive :)".format(game_ctl.time_of_day))

        game_ctl.user_list = response.user_list

        if game_ctl.time_of_day == DAY:
            game_ctl.time_of_day = NIGHT
        else:
            game_ctl.time_of_day = DAY

        first_day_flag = False
        game_ctl.publish_info = list()



async def message_handler(game_ctl):
    async for message in game_ctl.stub.EventsMonitor(
            mafia_pb2.EventsMonitorRequest(session_name=game_ctl.session_name, username=game_ctl.username)
    ):
        if message.format == INFO:
            print(message.extra)
        elif message.format == JOIN:
            print("{} has joined".format(message.extra))
        elif message.format == KILL:
            game_ctl.user_list[message.extra] = SPIRIT_ROLE
            print("{} was executed".format(message.extra))
        elif message.format == END and game_ctl.role == SPIRIT_ROLE:
            print(message.extra)
            await game_ctl.channel.close()
            exit(0)

async def run() -> None:
    try:
        channel = grpc.aio.insecure_channel('{}:{}'.format(HOST, PORT))
        stub = mafia_pb2_grpc.MafiaCtlStub(channel)

        game_ctl = GameCtl(stub, channel)
        await game_ctl.start()

        # main logic
        await asyncio.gather(
            gameplay(game_ctl),
            message_handler(game_ctl)
        )
    except SystemExit:
        pass


if __name__ == '__main__':
    asyncio.run(run())
