from __future__ import annotations
from google.protobuf.message import Message

class HelloRequest(Message):
    name: str

class HelloReply(Message):
    message: str
