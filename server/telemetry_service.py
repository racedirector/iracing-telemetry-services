import datetime
import grpc
import json
import struct
import yaml
from google.protobuf.struct_pb2 import Struct
from irsdk import IRSDK, VAR_TYPE_MAP, YAML_CODE_PAGE
from server.iracing_service import IRacingService
from server.proto import telemetry_pb2
from server.proto import telemetry_pb2_grpc
from server.type_util import ENUM_TYPE_CACHE, json_schema_for_irsdk_enums, string_for_var, json_schema_for_var
from time import sleep
from typing import Iterable
from yaml.reader import Reader as YamlReader
from genson import SchemaBuilder

try:
    from yaml.cyaml import CSafeLoader as YamlSafeLoader
except ImportError:
    from yaml import SafeLoader as YamlSafeLoader

def DateEncoder(obj):
    """JSON encoder for datetime objects."""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()

class TelemetryService(IRacingService, telemetry_pb2_grpc.TelemetryServicer):
  """Servicer that manages telemetry data."""

  session_json_schema = {}
  telemetry_json_schema = {}

  def __init__(self, ir: IRSDK):
    super().__init__(ir)

  # Override check_connection to check if a new connection was made.
  # If so, fetch a JSON Schema representation of all known properties
  # in the telemetry
  def check_connection(self):
    was_connected = self.connected
    is_connected = super().check_connection()

    if is_connected and not was_connected:
      properties = {}

      # Freeze the buffer for reading...
      self.ir.freeze_var_buffer_latest()

      # Get the Session string binary.
      session_binary = self.ir._shared_mem[self.ir._header.session_info_offset:self.ir._header.session_info_len].rstrip(b'\x00').decode(YAML_CODE_PAGE)

      # Get all known keys from the iRacing header.
      for key in self.ir._var_headers_dict:
          var_header = self.ir._var_headers_dict[key]
          var_type = VAR_TYPE_MAP[var_header.type]
          var_count = var_header.count

          # Get a JSON Schema representation of the key based on the type and count.
          properties[key] = json_schema_for_var(key, var_type, var_count)

      # Unfreeze the buffer to continue parsing
      self.ir.unfreeze_var_buffer_latest()

      # Convert the binary session info to a JSON dictionary
      session_yml = yaml.load(session_binary, Loader=YamlSafeLoader)
      session_json_string = json.dumps(session_yml, indent=2, default=DateEncoder)
      session_json = json.loads(session_json_string)
      
      session_schema = SchemaBuilder()
      session_schema.add_schema({
        "$schema": "http://json-schema.org/schema#",
        "title": "Session",
        "description": "The session string from the iRacing Simulation.",
        "type": "object",
      })

      session_schema.add_object(session_json)

      self.session_json_schema = session_schema.to_schema()

      telemetry_schema = SchemaBuilder()
      telemetry_schema.add_schema({
        "$schema": "http://json-schema.org/schema#",
        "title": "Telemetry",
        "description": "Telemetry from the iRacing Simulation.",
        "type": "object",
        "properties": properties,
        "$defs": json_schema_for_irsdk_enums()
      })

      self.telemetry_json_schema = telemetry_schema.to_schema()
    elif not is_connected and was_connected:
      # iRacing disconnected, clear the schema
      self.telemetry_json_schema = None
      self.session_json_schema = None


    return is_connected

  def GetTelemetryJSONSchema(self, request, context):
    response = telemetry_pb2.GetTelemetryJSONSchemaResponse()
    if self.check_is_connected(context):
      telemetry_schema = Struct()
      telemetry_schema.update(self.telemetry_json_schema)
      response.telemetry = telemetry_schema

      session_schema = Struct()
      session_schema.update(self.session_json_schema)
      response.session = session_schema

    return response
    
  def GetTelemetryJSONSchemaString(self, request, context):
    response = telemetry_pb2.GetTelemetryJSONSchemaStringResponse()
    if self.check_is_connected(context):
      response.telemetry = json.dumps(self.telemetry_json_schema)
      response.session = json.dumps(self.session_json_schema)

    return response

  def GetTelemetryTypes(self, request: telemetry_pb2.GetTelemetryTypesRequest, context):
    response = telemetry_pb2.GetTelemetryTypesResponse()
    # Check if the connection is valid
    if self.check_is_connected(context):
      telemetry_type_cache = {}
      self.ir.freeze_var_buffer_latest()

      # For each variable header in the buffer, get the type and count
      # and store it in the cache
      for key in self.ir._var_headers_dict:
        var_header = self.ir._var_headers_dict[key]
        var_type = VAR_TYPE_MAP[var_header.type]
        var_count = var_header.count
        type_string = string_for_var(key, var_type)
        telemetry_type_cache[key] = f'Array<{type_string}>[{var_count}]' if var_count > 1 else type_string

      # Unfreeze the buffer
      self.ir.unfreeze_var_buffer_latest()

      response_data = Struct()
      response_data.update({
        'types': telemetry_type_cache,
        'version': self.ir._header.version if self.connected else 0,
        '$refs': ENUM_TYPE_CACHE
      })

      response.types = response_data

    return response

  def DumpTelemetry(self, request, context):
    response = telemetry_pb2.GetTelemetryResponse()
    if self.check_is_connected(context):
      response_data = Struct()
      telemetry_cache = {}

      self.ir.freeze_var_buffer_latest()
      session_binary = self.ir._shared_mem[self.ir._header.session_info_offset:self.ir._header.session_info_len].rstrip(b'\x00').decode(YAML_CODE_PAGE)
      
      # Get all the headers from the buffer
      for key in self.ir._var_headers_dict:
        var_header = self.ir._var_headers_dict[key]
        var_buf_latest = self.ir._var_buffer_latest
        res = struct.unpack_from(
          VAR_TYPE_MAP[var_header.type] * var_header.count,
          var_buf_latest.get_memory(),
          var_buf_latest.buf_offset + var_header.offset)
        
        telemetry_cache[key] = res[0] if var_header.count == 1 else list(res)

      self.ir.unfreeze_var_buffer_latest()

      # Convert the binary session info to a JSON dictionary
      session_yml = yaml.load(session_binary, Loader=YamlSafeLoader)
      session_json_string = json.dumps(session_yml, indent=2, default=DateEncoder)
      session_json = json.loads(session_json_string)

      # Update the response
      response_data.update(session_json)
      response_data.update(telemetry_cache)
      response.telemetry = response_data
    
    return response

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
  
