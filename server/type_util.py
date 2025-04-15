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
