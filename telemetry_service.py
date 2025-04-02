import proto.telemetry_pb2_grpc as telemetry_pb2_grpc
import proto.telemetry_pb2 as telemetry_pb2
from time import sleep
from google.protobuf.struct_pb2 import Struct
from irsdk import IRSDK
from iracing_service import IRacingService

class TelemetryService(IRacingService, telemetry_pb2_grpc.TelemetryServicer):
  """Servicer that manages telemetry data."""

  def __init__(self, ir: IRSDK):
    super().__init__(ir)

  def GetTelemetry(self, request: telemetry_pb2.GetTelemetryRequest, context):
    response = telemetry_pb2.GetTelemetryResponse()
    if self.check_is_connected(context):
      self.ir.freeze_var_buffer_latest()
      telemetry = {key: self.ir[key] for key in request.keys}
      self.ir.unfreeze_var_buffer_latest()

      struct = Struct()
      struct.update(telemetry)
      response.telemetry = struct

    return response
  
  def SubscribeTelemetry(self, request: telemetry_pb2.TelemetrySubscriptionRequest, context):
    telemetry_cache = {}
    while self.check_is_connected(context):
      response = telemetry_pb2.GetTelemetryResponse()
      self.ir.freeze_var_buffer_latest()
      telemetry = {key: self.ir[key] for key in request.keys if key not in telemetry_cache or telemetry_cache[key] != self.ir[key]}
      self.ir.unfreeze_var_buffer_latest()

      if telemetry: 
        struct = Struct()
        struct.update(telemetry)
        response.telemetry = struct
        yield response
        telemetry_cache.update(telemetry)

      # Update the cache and sleep
      sleep(1 / request.fps)

    return telemetry_pb2.GetTelemetryResponse()
  
