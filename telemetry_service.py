import grpc
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
  
  def SubscribeTelemetry(self, request: telemetry_pb2.TelemetrySubscriptionRequest, context: grpc.ServicerContext):
    fps = request.fps
    if fps <= 0:
      context.set_details("FPS must be greater than 0")
      context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
      return telemetry_pb2.GetTelemetryResponse()
    if fps > 60:
      context.set_details("FPS must be less than or equal to 60")
      context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
      return telemetry_pb2.GetTelemetryResponse()
    if not request.keys:
      context.set_details("Keys must not be empty")
      context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
      return telemetry_pb2.GetTelemetryResponse()

    telemetry_cache = {}
    while self.check_is_connected(context):
      self.ir.freeze_var_buffer_latest()
      telemetry = {key: self.ir[key] for key in request.keys if key not in telemetry_cache or telemetry_cache[key] != self.ir[key]}
      self.ir.unfreeze_var_buffer_latest()

      if telemetry: 
        struct = Struct()
        struct.update(telemetry)
        yield telemetry_pb2.GetTelemetryResponse(telemetry=struct)
        telemetry_cache.update(telemetry)

      # Update the cache and sleep
      sleep(1 / fps)

    return telemetry_pb2.GetTelemetryResponse()
  
