import json
from google.protobuf.struct_pb2 import Struct
from genson import SchemaBuilder
from irsdk import VAR_TYPE_MAP, YAML_CODE_PAGE
import yaml
from server.date_encoder import DateEncoder
from server.iracing_service import IRacingService
from server.proto import schema_pb2
from server.type_util import ENUM_TYPE_CACHE, json_schema_for_irsdk_enums, json_schema_for_var, string_for_var
try:
    from yaml.cyaml import CSafeLoader as YamlSafeLoader
except ImportError:
    from yaml import SafeLoader as YamlSafeLoader



class SchemaService(IRacingService):
  session_json_schema = {}
  telemetry_json_schema = {}

  def __init__(self, ir):
    super().__init__(ir)
    if ir.is_initialized and ir.is_connected:
      self.__update_schema()

  def __update_schema(self):
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

  # Override check_connection to check if a new connection was made.
  # If so, fetch a JSON Schema representation of all known properties
  # in the telemetry
  def check_connection(self):
    was_connected = self.connected
    is_connected = super().check_connection()

    if is_connected and not was_connected:
      self.__update_schema()
    elif not is_connected and was_connected:
      # iRacing disconnected, clear the schema
      self.telemetry_json_schema = None
      self.session_json_schema = None


    return is_connected

  def GetTelemetryJSONSchema(self, request, context):
    response = schema_pb2.GetTelemetryJSONSchemaResponse()
    if self.check_is_connected(context):
      telemetry_schema = Struct()
      telemetry_schema.update(self.telemetry_json_schema)
      response.telemetry = telemetry_schema

      session_schema = Struct()
      session_schema.update(self.session_json_schema)
      response.session = session_schema

    return response
    
  def GetTelemetryJSONSchemaString(self, request, context):
    response = schema_pb2.GetTelemetryJSONSchemaStringResponse()
    if self.check_is_connected(context):
      response.telemetry = json.dumps(self.telemetry_json_schema)
      response.session = json.dumps(self.session_json_schema)

    return response

  def GetTelemetryTypes(self, request: schema_pb2.GetTelemetryTypesRequest, context):
    response = schema_pb2.GetTelemetryTypesResponse()
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
