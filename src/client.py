import grpc
import asyncio
from pick import pick
import service.proto.mafia_pb2 as mafia_pb2
import service.proto.mafia_pb2_grpc as mafia_pb2_grpc

from defines import *


async def gameplay(stub, entry_mode, session_name, username):
    # connect to session
    response = await stub.JoinSession(mafia_pb2.JoinSessionRequest(session_name=session_name, username=username))

    print("JOIN RESPONSE: {}".format(response.info))


async def message_handler(stub, session_name, username):
    async for message in stub.EventsMonitor(
            mafia_pb2.EventsMonitorRequest(session_name=session_name, username=username)
    ):
        print(message.extra)


async def run() -> None:
    async with grpc.aio.insecure_channel('{}:{}'.format(HOST, PORT)) as channel:
        stub = mafia_pb2_grpc.MafiaCtlStub(channel)

        # initial user info
        username = input("Enter your name: ")

        title = 'Choose entry mode: '
        entry_mode, index = pick(ENTRY_MODES_LIST, title, indicator='[x]', default_index=0)

        print("Entry mode is selected: {}".format(entry_mode))

        session_name = input("Enter session name: ")

        # creating new room if required
        if entry_mode == CREATE_ROOM:
            session_size = int(input("Session size: "))
            response = await stub.CreateSession(
                mafia_pb2.CreateSessionRequest(name=session_name, size=session_size, owner=username))

        # main logic
        await asyncio.gather(
            gameplay(stub, entry_mode, session_name, username),
            message_handler(stub, session_name, username)
        )


if __name__ == '__main__':
    asyncio.run(run())
