from concurrent import futures
import logging
import os, sys

proto_dir = os.path.join(os.path.dirname(__file__), 'proto')
sys.path.insert(0, proto_dir)

from dotenv import load_dotenv
import grpc
from grpc_reflection.v1alpha import reflection
from irsdk import IRSDK
from broadcast_service import BroadcastService
from telemetry_service import TelemetryService
import proto.broadcast_pb2_grpc as broadcast_pb2_grpc
import proto.broadcast_pb2 as broadcast_pb2
import proto.telemetry_pb2_grpc as telemetry_pb2_grpc
import proto.telemetry_pb2 as telemetry_pb2

load_dotenv()

class Environment:
  '''Environment variables for the server configuration.'''
  host = os.getenv("HOST")
  port = os.getenv("PORT")

  @classmethod
  def api_url(cls):
    return cls.host + ":" + cls.port
  

class Server:
  ir = IRSDK()
  port = Environment.port

  def __init__(self, server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))):
    broadcast_pb2_grpc.add_ServerServicer_to_server(BroadcastService(self.ir), server)
    telemetry_pb2_grpc.add_TelemetryServicer_to_server(TelemetryService(self.ir), server)

    SERVICE_NAMES = (
      broadcast_pb2.DESCRIPTOR.services_by_name['Server'].full_name,
      telemetry_pb2.DESCRIPTOR.services_by_name['Telemetry'].full_name,
      reflection.SERVICE_NAME,
    )

    reflection.enable_server_reflection(SERVICE_NAMES, server)

    self.server = server

  def start(self):
    self.server.add_insecure_port('[::]:' + self.port)
    self.server.start()
    print(f"Server started on port {self.port}")
    self.server.wait_for_termination()
    
  def stop(self):
    self.ir.shutdown()
    self.server.stop(0)
    print("Server stopped")

if __name__ == '__main__':
  logging.basicConfig()
  server = Server()

  try:
    server.start()
  except KeyboardInterrupt:
    server.stop()