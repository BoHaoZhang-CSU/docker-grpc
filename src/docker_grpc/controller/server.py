from __future__ import annotations

from concurrent import futures
from typing import Dict

import grpc
import serial

from docker_grpc.controller import controller_pb2, controller_pb2_grpc


COMMAND_MAP: Dict[int, str] = {
    controller_pb2.CommandType.LEFT: "left",
    controller_pb2.CommandType.RIGHT: "right",
    controller_pb2.CommandType.ANGLE: "angle",
    controller_pb2.CommandType.SPEED: "speed",
    controller_pb2.CommandType.STOP: "stop",
}

angle = 10
class DeviceController(controller_pb2_grpc.DeviceControllerServicer):
    """gRPC servicer bridging requests to an STM32 over serial."""

    def __init__(self, port: str = "COM36", baudrate: int = 115200) -> None:
        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
        except serial.SerialException:
            # Serial port is optional to allow running without hardware.
            self.serial = None

    def SendCommand(self, request: controller_pb2.CommandRequest, context: grpc.ServicerContext) -> controller_pb2.CommandResponse:  # noqa: N802
        cmd = COMMAND_MAP.get(request.command)
        if cmd == "right":
            self.serial.write("r_pwm(300);".encode("utf-8"))
        elif cmd == "left":
            self.serial.write("l_pwm(300);".encode("utf-8"))
        elif cmd == "stop":
            angle += 10
            self.serial.write(f"s_angle({angle});".encode("utf-8"))
            
        print("cmd:",cmd)
        if not cmd or self.serial is None:
            return controller_pb2.CommandResponse(value=0)

        # self.serial.write(cmd.encode("ascii"))
        self.serial.flush()
        line = self.serial.readline().decode("ascii").strip()
        print("recv:",line)
        try:
            _, value_str = line.split(":", 1)
            value = int(value_str)
        except ValueError:
            value = 0
        return controller_pb2.CommandResponse(value=value)


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    controller_pb2_grpc.add_DeviceControllerServicer_to_server(DeviceController(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":  # pragma: no cover
    serve()
