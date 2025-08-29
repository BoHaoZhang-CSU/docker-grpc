from __future__ import annotations

import grpc
import typer

from docker_grpc.controller import controller_pb2, controller_pb2_grpc

COMMAND_MAP = {
    "left": controller_pb2.CommandType.LEFT,
    "right": controller_pb2.CommandType.RIGHT,
    "angle": controller_pb2.CommandType.ANGLE,
    "speed": controller_pb2.CommandType.SPEED,
    "stop": controller_pb2.CommandType.STOP,
}

app = typer.Typer()


def run(command: str) -> None:
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = controller_pb2_grpc.DeviceControllerStub(channel)
        request = controller_pb2.CommandRequest(command=COMMAND_MAP[command])
        response = stub.SendCommand(request)
    print(f"{command} value: {response.value}")


@app.command()
def main(command: str = typer.Argument(..., help="Command to send")) -> None:
    if command not in COMMAND_MAP:
        typer.echo(f"Invalid command: {command}")
        typer.echo("Valid commands: left, right, angle, speed, stop")
        raise typer.Exit(1)
    run(command)


if __name__ == "__main__":  # pragma: no cover
    app()
