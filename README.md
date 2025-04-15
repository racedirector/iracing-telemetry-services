# iracing-telemetry-grpc

A gRPC server for iRacing telemetry data. Uses `pyirsdk` under the hood.

Allows for messaging to the iRacing simulation, and querying for telmetry data.

## Running the server

Clone the repo and install the dependencies:

```bash
make install
```

Run the server:

```bash
make run
```

## Services

### Telemetry Service

Service for retrieving telemetry data from iRacing.

### Broadcast Service

Service for sending "broadcast messages" to the iRacing simulation.

## Development

Make changes to the `proto` files in the `proto` directory and run:

```bash
make protoc
```

To generate the gRPC code.

It's recommended to use postman to test the gRPC server. ~~You can use the `postman` directory to import the collection and environment.~~ (Coming soon). The server supports reflection, so you can use any gRPC client to test the server. The `grpcurl` tool is also a good option for testing gRPC servers from the command line.

## Build .exe

Generate a pyinstaller spec file and then build the .exe:

```bash
make spec
pyinstaller telemetry-server.spec
```

Check the `dist` directory for the generated .exe file.

## Docker

Docker implementation is intended to bundle the server with an `envoy` proxy server
to enable gRPC-web support. This allows for easy integration with web applications. The implmentation is not yet complete.
