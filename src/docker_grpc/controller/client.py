from __future__ import annotations

import sys

import grpc

from docker_grpc.controller import controller_pb2, controller_pb2_grpc

COMMAND_MAP = {
    "left": controller_pb2.CommandType.LEFT,
    "right": controller_pb2.CommandType.RIGHT,
    "angle": controller_pb2.CommandType.ANGLE,
    "speed": controller_pb2.CommandType.SPEED,
    "stop": controller_pb2.CommandType.STOP,
}


def run(command: str) -> None:
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = controller_pb2_grpc.DeviceControllerStub(channel)
        request = controller_pb2.CommandRequest(command=COMMAND_MAP[command])
        response = stub.SendCommand(request)
    print(f"{command} value: {response.value}")


if __name__ == "__main__":  # pragma: no cover
    if len(sys.argv) != 2 or sys.argv[1] not in COMMAND_MAP:
        print("Usage: python client.py [left|right|angle|speed|stop]")
        sys.exit(1)
    run(sys.argv[1])
