import grpc

from . import helloworld_pb2, helloworld_pb2_grpc


def run() -> None:
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="world"))
    print(f"Greeter client received: {response.message}")


if __name__ == "__main__":  # pragma: no cover
    run()
