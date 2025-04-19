import irsdk

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

# A map where the key is a telemetry key and the value
# is the value in ENUM_TYPE_CACHE for the key.
BITWISE_TELEMETRY_MAP = {
    'SessionFlags': 'Flags',
    'CarIdxSessionFlags': 'Flags',
    'CarIdxPaceFlags': 'PaceFlags',
    'CamCameraState': 'CameraState',
    'EngineWarnings': 'EngineWarnings',
    'PitSvFlags': 'PitServiceFlags',
}

ENUM_TELEMETRY_MAP = {
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

ENUM_TYPE_CACHE = {
    # Known bitwise flags in the iRacing SDK
    'EngineWarnings': get_class_attributes(irsdk.EngineWarnings, as_hex=True),
    'Flags': get_class_attributes(irsdk.Flags, as_hex=True),
    'CameraState': get_class_attributes(irsdk.CameraState, as_hex=True),
    'PitServiceFlags': get_class_attributes(irsdk.PitSvFlags, as_hex=True),
    'PaceFlags': get_class_attributes(irsdk.PaceFlags, as_hex=True),

    # Known enums in the iRacing SDK
    'TrackLocation': get_class_attributes(irsdk.TrkLoc),
    'TrackSurface': get_class_attributes(irsdk.TrkSurf),
    'SessionState': get_class_attributes(irsdk.SessionState),
    'PitServiceStatus': get_class_attributes(irsdk.PitSvStatus),
    'PaceMode': get_class_attributes(irsdk.PaceMode),
    'CarLeftRight': get_class_attributes(irsdk.CarLeftRight),
    'TrackWetness': get_class_attributes(irsdk.TrackWetness),
}

ENUM_CLASS_CACHE = {
      # Known bitwise flags in the iRacing SDK
    'EngineWarnings': irsdk.EngineWarnings,
    'Flags': irsdk.Flags,
    'CameraState': irsdk.CameraState,
    'PitServiceFlags': irsdk.PitSvFlags,
    'PaceFlags': irsdk.PaceFlags,
      # Known enums in the iRacing SDK
    'TrackLocation': irsdk.TrkLoc,
    'TrackSurface': irsdk.TrkSurf,
    'SessionState': irsdk.SessionState,
    'PitServiceStatus': irsdk.PitSvStatus,
    'PaceMode': irsdk.PaceMode,
    'CarLeftRight': irsdk.CarLeftRight,
    'TrackWetness': irsdk.TrackWetness,
}

def string_for_var(key, var_type):
  # Assert the var type exists in the VAR_TYPE_MAP
  if var_type not in irsdk.VAR_TYPE_MAP:
    raise ValueError(f"Invalid var type: {var_type}")
  
  # Return the string representation of the var type
  if var_type == 'c':
    return 'char'
  elif var_type == '?':
    return 'bool'
  elif var_type == 'i':
    return f'Ref<{ENUM_TELEMETRY_MAP[key]}>' if key in ENUM_TELEMETRY_MAP else 'int'
  elif var_type == 'f':
    return 'float'
  elif var_type == 'd':
    return 'double'
  elif var_type == 'I':
    return f'Ref<{BITWISE_TELEMETRY_MAP[key]}>' if key in BITWISE_TELEMETRY_MAP else 'bitwise'

# Returns JSON schema for a given type.
def json_for_type(type):
  return {
    "type": type
  }

# Returns a JSON schema format for a type with a fixed length.
def array_for_var(type, count, description=None):
  return {
    "type": "array",
    "items": json_for_type(type),
    "minItems": count,
    "maxItems": count,
  } | ({ "description": description } if description else {})

# Returns a JSON schema format for a reference with an optional description.
def array_for_ref(ref, count, description=None):
  return {
    "type": "array",
    "items": { "$ref": f"#/$defs/{ref}" },
    "minItems": count,
    "maxItems": count,
  } | ({ "description": description } if description else {})

# Get's the JSON schema for a variable given the type and count.
def json_schema_for_var(key, type, count):
  if type == 'c':
    return array_for_var("string", count) if count > 1 else json_for_type("string")
  if type == '?':
    return array_for_var("boolean", count) if count > 1 else json_for_type("boolean")
  if type == 'i':
    if key in ENUM_TELEMETRY_MAP:
      enum_type = ENUM_TELEMETRY_MAP[key]
      return array_for_ref(enum_type, count) if count > 1 else {
        "$ref": f"#/$defs/{enum_type}"
      }
    else:
      return array_for_var("integer", count) if count > 1 else json_for_type("integer")
  if type == 'f' or type == 'd':
    return array_for_var("number", count) if count > 1 else json_for_type("number")
  if type == 'I':
    if key in BITWISE_TELEMETRY_MAP:
      bitwise_type = BITWISE_TELEMETRY_MAP[key]
      description = f"Bitwise field for `{bitwise_type}`"
      return array_for_ref(bitwise_type, count, description) if count > 1 else {
        "type": 'integer',
        "description": description,
      }

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

# Returns a dict of IRSDK enum type names as the keys and the JSON schema of 
# the enum as values.
def json_schema_for_irsdk_enums():
  return { 
    key: json_schema_for_irsdk_enum(cls, as_hex=key in BITWISE_TELEMETRY_MAP)
    for key, cls in ENUM_CLASS_CACHE.items() 
  }
