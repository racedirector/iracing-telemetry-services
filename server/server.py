import grpc
from concurrent import futures
from grpc_reflection.v1alpha import reflection
from irsdk import IRSDK
from server.broadcast_service import BroadcastService
from server.schema_service import SchemaService
from server.telemetry_service import TelemetryService
from server.proto import broadcast_pb2_grpc
from server.proto import broadcast_pb2
from server.proto import telemetry_pb2_grpc
from server.proto import telemetry_pb2
from server.proto import schema_pb2_grpc
from server.proto import schema_pb2

class Server:
  iracing: IRSDK

  def __init__(self, port = 50051, server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)), iracing = IRSDK(), test_file=None):
    self.iracing = iracing
    
    broadcast_pb2_grpc.add_BroadcastServicer_to_server(BroadcastService(iracing), server)
    telemetry_pb2_grpc.add_TelemetryServicer_to_server(TelemetryService(iracing, test_file), server)
    schema_pb2_grpc.add_SchemaServicer_to_server(SchemaService(iracing), server)


    SERVICE_NAMES = (
      broadcast_pb2.DESCRIPTOR.services_by_name['Broadcast'].full_name,
      telemetry_pb2.DESCRIPTOR.services_by_name['Telemetry'].full_name,
      schema_pb2.DESCRIPTOR.services_by_name['Schema'].full_name,
      reflection.SERVICE_NAME,
    )

    reflection.enable_server_reflection(SERVICE_NAMES, server)

    self.server = server
    self.port = port

  def start(self):
    self.server.add_insecure_port(f'[::]:{self.port}')
    self.server.start()
    print(f"Server started on port {self.port}")
    self.server.wait_for_termination()
    
  def stop(self):
    self.iracing.shutdown()
    self.server.stop(0)
    print("Server stopped")

