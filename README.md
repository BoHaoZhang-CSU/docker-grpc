# docker-grpc

This repository contains a minimal **gRPC** "Hello World" example.

The service is defined in [`helloworld.proto`](src/docker_grpc/helloworld/helloworld.proto) and
Python types are generated with `grpcio-tools`. Type stubs (`.pyi`) were
produced using `mypy-grpc-tools`.

## Running the example

Start the server:

```bash
PYTHONPATH=src python -m docker_grpc.helloworld.server
```

In another terminal run the client:

```bash
PYTHONPATH=src python -m docker_grpc.helloworld.client
```

The client will print the greeting returned by the server.
