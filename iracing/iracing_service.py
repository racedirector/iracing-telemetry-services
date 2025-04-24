import json
import yaml
from genson import SchemaBuilder
from irsdk import IRSDK, VAR_TYPE_MAP, YAML_CODE_PAGE
from iracing.date_encoder import DateEncoder
try:
    from yaml.cyaml import CSafeLoader as YamlSafeLoader
except ImportError:
    from yaml import SafeLoader as YamlSafeLoader

BITWISE_MAP = {
    'SessionFlags': 'Flags',
    'CarIdxSessionFlags': 'Flags',
    'CarIdxPaceFlags': 'PaceFlags',
    'CamCameraState': 'CameraState',
    'EngineWarnings': 'EngineWarnings',
    'PitSvFlags': 'PitServiceFlags',
}

ENUM_MAP = {
    'PlayerTrackSurface': 'TrackLocation',
    'PlayerTrackSurfaceMaterial': 'TrackSurface',
    'CarIdxTrackSurface': 'TrackLocation',
    'CarIdxTrackSurfaceMaterial': 'TrackSurface',
    'PlayerCarPitSvStatus': 'PitServiceStatus',
    'PaceMode': 'PaceMode',
    'TrackWetness': 'TrackWetness',
    'SessionState': 'SessionState',
    "CarLeftRight": "CarLeftRight",
}

def json_for_type(type, description=None):
  return {
    "type": type,
  } | ({ "description": description } if description else {})

def ref_for_type(type, description=None):
  return {
    "$ref": f"#/$defs/{type}",
  } | ({ "description": description } if description else {})

def array_for_item(item, count, description=None):
  return {
    "type": "array",
    "items": item,
    "minItems": count,
    "maxItems": count,
  } | ({ "description": description } if description else {})


def json_schema_for_var(key, type, count):
  if type == 'c':
    schema = json_for_type("string")
    return array_for_item(schema, count) if count > 1 else schema
  if type == '?':
    schema = json_for_type("boolean")
    return array_for_item(schema, count) if count > 1 else schema
  if type == 'i':
    if key in ENUM_MAP:
      enum_type = ENUM_MAP[key]
      schema = ref_for_type(enum_type)
      return array_for_item(schema, count) if count > 1 else schema
    else:
      schema = json_for_type("integer")
      return array_for_item(schema, count) if count > 1 else schema
  if type == 'f' or type == 'd':
    schema = json_for_type("number")
    return array_for_item(schema, count) if count > 1 else schema
  if type == 'I':
    if key in BITWISE_MAP:
      bitwise_type = BITWISE_MAP[key]
      description = f"Bitwise representation of {bitwise_type}"
      schema = json_for_type("integer")
      return array_for_item(schema, count, description) if count > 1 else schema
  pass

class IRacingService:
  client: IRSDK
  connected = False

  # String representation of the telemetry JSON schema.
  telemetry_schema = None
  # String representation of the session JSON schema.
  session_schema = None

  def __init__(self, ir: IRSDK = IRSDK(), test_file=None, dump_path=None):
    self.client = ir
    self.test_file = test_file
    self.dump_path = dump_path

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.client.shutdown()
    self.client = None
    self.connected = False
    self.telemetry_schema = None
    self.session_schema = None
    self.test_file = None
    self.dump_path = None


  def check_connection(self):
    if self.connected and not (self.client.is_initialized and self.client.is_connected):
      print("iRacing disconnected")
      self.connected = False
      self.client.shutdown()
    elif not self.connected and self.client.startup(test_file=self.test_file, dump_to=self.dump_path) and self.client.is_initialized and self.client.is_connected:
      print("iRacing connected")
      self.connected = True
      self.__update_schema()

    return self.connected
  
  def get_telemetry(self, keys: list[str], condition = lambda key: True) -> dict:
    telemetry = {}
    if not self.check_connection():
      return telemetry

    self.client.freeze_var_buffer_latest()
    telemetry = { 
      key: self.client[key]
      for key in keys
      if condition(key)
    }
    self.client.unfreeze_var_buffer_latest()

    return telemetry

  def __update_schema(self):
    json_schema = {}
    self.client.freeze_var_buffer_latest()

    session_binary = self.client._shared_mem[self.client._header.session_info_offset:self.client._header.session_info_len].rstrip(b'\x00').decode(YAML_CODE_PAGE)

    for key in self.client._var_headers_dict:
      var_header = self.client._var_headers_dict[key]
      var_type = VAR_TYPE_MAP[var_header.type]
      var_count = var_header.count
      json_schema[key] = json_schema_for_var(key, var_type, var_count)

    self.client.unfreeze_var_buffer_latest()

    telemetry_schema = SchemaBuilder()
    telemetry_schema.add_schema({
      "$schema": "http://json-schema.org/schema#",
      "title": "Telemetry",
      "description": "Telemetry from the iRacing Simulation.",
      "type": "object",
      "properties": json_schema,
      # "$defs": json_schema_for_irsdk_enums(),
      "additionalProperties": False,  
    })

    self.telemetry_schema = telemetry_schema.to_schema()

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
      "additionalProperties": False,
    })
    session_schema.add_object(session_json)

    self.session_schema = session_schema.to_schema()