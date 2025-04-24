import json
import yaml
from iracing.date_encoder import DateEncoder
from genson import SchemaBuilder
from irsdk import (
  IRSDK,
  VAR_TYPE_MAP,
  YAML_CODE_PAGE,
  EngineWarnings,
  Flags,
  CameraState,
  PitSvFlags,
  PaceFlags,
  TrkLoc,
  TrkSurf,
  SessionState,
  PitSvStatus,
  PaceMode,
  CarLeftRight,
  TrackWetness,
)

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

ENUM_CLASS_CACHE = {
    # Known bitwise flags in the iRacing SDK
    'EngineWarnings': EngineWarnings,
    'Flags': Flags,
    'CameraState': CameraState,
    'PitServiceFlags': PitSvFlags,
    'PaceFlags': PaceFlags,
    # Known enums in the iRacing SDK
    'TrackLocation': TrkLoc,
    'TrackSurface': TrkSurf,
    'SessionState': SessionState,
    'PitServiceStatus': PitSvStatus,
    'PaceMode': PaceMode,
    'CarLeftRight': CarLeftRight,
    'TrackWetness': TrackWetness,
}

def get_class_attributes(cls, as_hex=False):
    """
    Get all attributes of a class.
    
    Parameters:
        cls: The class to extract attributes from.
        as_hex: If True, converts attribute values to hexadecimal.
    
    Returns:
        A list of dictionaries containing attribute names and values.
    """
    return [
        dict({'name': attr, 'value': hex(getattr(cls, attr)) if as_hex else getattr(cls, attr)})
        for attr in dir(cls)
        if not attr.startswith('__') and not callable(getattr(cls, attr))
    ]

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

# Get's a JSON schema representation for an enum, optionally formatting as a 
# hex string.
def json_schema_for_irsdk_enum(enum_class, as_hex):
  attributes = get_class_attributes(enum_class, as_hex=as_hex)

  # Create an array of names and an array of values, sorted by values
  sorted_attributes = sorted(attributes, key=lambda attr: attr['value'])
  names, values = zip(*[(attr['name'], attr['value']) for attr in sorted_attributes])

  return {
    "type": "integer",
    "tsEnumNames": names,
    "enum": values
  }

def json_schema_for_telemetry(ir: IRSDK):
    schema = SchemaBuilder()
    schema.add_schema({
      "$schema": "http://json-schema.org/schema#",
      "title": "Telemetry",
      "description": "Telemetry from the iRacing Simulation.",
      "type": "object",
      "properties": {
        key: json_schema_for_var(key, VAR_TYPE_MAP[var_header.type], var_header.count)
        for key, var_header in ir._var_headers_dict.items()
      },
      "$defs": { 
        key: json_schema_for_irsdk_enum(cls, as_hex=key in BITWISE_MAP)
        for key, cls in ENUM_CLASS_CACHE.items() 
      },
      "additionalProperties": False,  
    })

    return schema

def json_schema_for_session(ir: IRSDK):
  session_binary = ir._shared_mem[ir._header.session_info_offset:ir._header.session_info_len].rstrip(b'\x00').decode(YAML_CODE_PAGE)
  # Convert the binary session info to a JSON dictionary
  session_yml = yaml.load(session_binary, Loader=YamlSafeLoader)
  session_json_string = json.dumps(session_yml, indent=2, default=DateEncoder)
  session_json = json.loads(session_json_string)

  schema = SchemaBuilder()
  schema.add_schema({
    "$schema": "http://json-schema.org/schema#",
    "title": "Session",
    "description": "The session string from the iRacing Simulation.",
    "type": "object",
    "additionalProperties": False,
  })

  schema.add_object(session_json)

  return schema