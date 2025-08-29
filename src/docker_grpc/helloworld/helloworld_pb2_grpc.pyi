from __future__ import annotations
import grpc
from .helloworld_pb2 import HelloRequest, HelloReply
from typing import Any, Optional

class GreeterStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    def SayHello(
        self,
        request: HelloRequest,
        timeout: Optional[float] = ...,
        metadata: Any = ...,
        credentials: Any = ...,
        wait_for_ready: Optional[bool] = ...,
        compression: Optional[grpc.Compression] = ...,
    ) -> HelloReply: ...

class GreeterServicer:
    def SayHello(self, request: HelloRequest, context: grpc.ServicerContext) -> HelloReply: ...

def add_GreeterServicer_to_server(servicer: GreeterServicer, server: grpc.Server) -> None: ...
