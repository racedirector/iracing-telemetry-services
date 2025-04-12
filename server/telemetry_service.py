import grpc
import struct
from server.proto import telemetry_pb2_grpc
from server.proto import telemetry_pb2
from time import sleep
from google.protobuf.struct_pb2 import Struct
from irsdk import IRSDK, VAR_TYPE_MAP
from server.iracing_service import IRacingService
from typing import Iterable

class TelemetryService(IRacingService, telemetry_pb2_grpc.TelemetryServicer):
  """Servicer that manages telemetry data."""

  def __init__(self, ir: IRSDK):
    super().__init__(ir)

  def DumpTelemetry(self, request, context):
    if self.check_is_connected(context):
      print("Dumping telemetry data...")
      session_info_cache = {}
      telemetry_cache = {}
      self.ir.freeze_var_buffer_latest()

      # Get all the headers from the buffer
      for key in self.ir._var_headers_dict:
        var_header = self.ir._var_headers_dict[key]
        var_buf_latest = self.ir._var_buffer_latest
        res = struct.unpack_from(
          VAR_TYPE_MAP[var_header.type] * var_header.count,
          var_buf_latest.get_memory(),
          var_buf_latest.buf_offset + var_header.offset)
        
        telemetry_cache[key] = res[0] if var_header.count == 1 else list(res)

      session_info_cache = self.ir.__session_info_dict

      self.ir.unfreeze_var_buffer_latest()

      print("SessionInfo:", session_info_cache)
      print("Telemetry:", telemetry_cache)
      struct = Struct()
      struct.update(session_info_cache)
      struct.update(telemetry_cache)

      return telemetry_pb2.GetTelemetryResponse(telemetry=struct)

  def GetTelemetry(self, request: telemetry_pb2.GetTelemetryRequest, context: grpc.ServicerContext) -> telemetry_pb2.GetTelemetryResponse:
    response = telemetry_pb2.GetTelemetryResponse()
    if self.check_is_connected(context):
      self.ir.freeze_var_buffer_latest()
      telemetry = {key: self.ir[key] for key in request.keys}
      self.ir.unfreeze_var_buffer_latest()

      struct = Struct()
      struct.update(telemetry)
      response.telemetry = struct

    return response
  
  def RequestTelemetryStream(self, request_iterator: Iterable[telemetry_pb2.GetTelemetryRequest], context: grpc.ServicerContext) -> Iterable[telemetry_pb2.GetTelemetryResponse]:
    return super().RequestTelemetryStream(request_iterator, context)
  
  def SubscribeTelemetryStream(self, request: telemetry_pb2.TelemetrySubscriptionRequest, context: grpc.ServicerContext) -> Iterable[telemetry_pb2.GetTelemetryResponse]:
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

    '''
    For a telemetry subscription, we create a new instance of pyirsdk
    so the buffers can be frozen and unfrozen without affecting the main instance.
    This is important because the main instance is used for other purposes
    and we don't want to interfere with its operation.
    '''
    stream_ir = IRSDK()
    if not stream_ir.startup():
      context.set_details("Failed to connect to iRacing")
      context.set_code(grpc.StatusCode.UNAVAILABLE)
      return telemetry_pb2.GetTelemetryResponse()
    
    # Shutdown the connection to iRacing when the stream is closed.
    context.add_callback(stream_ir.shutdown)

    telemetry_cache = {}
    while stream_ir.is_connected and stream_ir.is_initialized:
      stream_ir.freeze_var_buffer_latest()
      telemetry = {key: stream_ir[key] for key in request.keys if key not in telemetry_cache or telemetry_cache[key] != stream_ir[key]}
      stream_ir.unfreeze_var_buffer_latest()

      if telemetry: 
        struct = Struct()
        struct.update(telemetry)
        yield telemetry_pb2.GetTelemetryResponse(telemetry=struct)
        telemetry_cache.update(telemetry)

      # Update the cache and sleep
      sleep(1 / fps)

    context.set_details("iRacing disconnected")
    return telemetry_pb2.GetTelemetryResponse()
  
