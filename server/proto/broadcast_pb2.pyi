from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from google.protobuf.empty_pb2 import Empty as Empty

DESCRIPTOR: _descriptor.FileDescriptor

class TelemetryCommandMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TELEMETRY_COMMAND_MODE_UNKNOWN: _ClassVar[TelemetryCommandMode]
    TELEMETRY_COMMAND_MODE_STOP: _ClassVar[TelemetryCommandMode]
    TELEMETRY_COMMAND_MODE_START: _ClassVar[TelemetryCommandMode]
    TELEMETRY_COMMAND_MODE_RESTART: _ClassVar[TelemetryCommandMode]

class ChatCommandMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHAT_COMMAND_MODE_UNKNOWN: _ClassVar[ChatCommandMode]
    CHAT_COMMAND_MODE_MACRO: _ClassVar[ChatCommandMode]
    CHAT_COMMAND_MODE_BEGIN_CHAT: _ClassVar[ChatCommandMode]
    CHAT_COMMAND_MODE_REPLY: _ClassVar[ChatCommandMode]
    CHAT_COMMAND_MODE_CANCEL: _ClassVar[ChatCommandMode]

class CameraState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CAMERA_STATE_UNKNOWN: _ClassVar[CameraState]
    CAMERA_STATE_CAMERA_TOOL_ACTIVE: _ClassVar[CameraState]
    CAMERA_STATE_UI_HIDDEN: _ClassVar[CameraState]
    CAMERA_STATE_USE_AUTO_SHOT_SELECTION: _ClassVar[CameraState]
    CAMERA_STATE_USE_TEMPORARY_EDITS: _ClassVar[CameraState]
    CAMERA_STATE_USE_KEY_ACCELERATION: _ClassVar[CameraState]
    CAMERA_STATE_USE_KEY10X_ACCELERATION: _ClassVar[CameraState]
    CAMERA_STATE_USE_MOUSE_AIM_MODE: _ClassVar[CameraState]

class ReplayPositionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPLAY_POSITION_MODE_UNKNOWN: _ClassVar[ReplayPositionMode]
    REPLAY_POSITION_MODE_BEGIN: _ClassVar[ReplayPositionMode]
    REPLAY_POSITION_MODE_CURRENT: _ClassVar[ReplayPositionMode]
    REPLAY_POSITION_MODE_END: _ClassVar[ReplayPositionMode]

class ReplaySearchMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPLAY_SEARCH_MODE_UNKNOWN: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_TO_START: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_TO_END: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_PREVIOUS_SESSION: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_NEXT_SESSION: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_PREVIOUS_LAP: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_NEXT_LAP: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_PREVIOUS_FRAME: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_NEXT_FRAME: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_PREVIOUS_INCIDENT: _ClassVar[ReplaySearchMode]
    REPLAY_SEARCH_MODE_NEXT_INCIDENT: _ClassVar[ReplaySearchMode]

class PitCommandMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PIT_COMMAND_MODE_UNKNOWN: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_CLEAR: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_TEAR_OFF: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_FUEL: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_LF_TIRE: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_RF_TIRE: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_LR_TIRE: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_RR_TIRE: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_CLEAR_TIRES: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_FAST_REPAIR: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_CLEAR_TEAR_OFF: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_CLEAR_FAST_REPAIR: _ClassVar[PitCommandMode]
    PIT_COMMAND_MODE_CLEAR_FUEL: _ClassVar[PitCommandMode]

class ReplayStateMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REPLAY_STATE_MODE_UNKNOWN: _ClassVar[ReplayStateMode]
    REPLAY_STATE_MODE_ERASE_TAPE: _ClassVar[ReplayStateMode]

class VideoCaptureMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    VIDEO_CAPTURE_MODE_UNKNOWN: _ClassVar[VideoCaptureMode]
    VIDEO_CAPTURE_MODE_SCREENSHOT: _ClassVar[VideoCaptureMode]
    VIDEO_CAPTURE_MODE_START: _ClassVar[VideoCaptureMode]
    VIDEO_CAPTURE_MODE_STOP: _ClassVar[VideoCaptureMode]
    VIDEO_CAPTURE_MODE_TOGGLE: _ClassVar[VideoCaptureMode]
    VIDEO_CAPTURE_MODE_SHOW_TIMER: _ClassVar[VideoCaptureMode]
    VIDEO_CAPTURE_MODE_HIDE_TIMER: _ClassVar[VideoCaptureMode]

class ForceFeedbackCommandMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FORCE_FEEDBACK_COMMAND_MODE_UNKNOWN: _ClassVar[ForceFeedbackCommandMode]
    FORCE_FEEDBACK_COMMAND_MODE_MAX_FORCE: _ClassVar[ForceFeedbackCommandMode]
TELEMETRY_COMMAND_MODE_UNKNOWN: TelemetryCommandMode
TELEMETRY_COMMAND_MODE_STOP: TelemetryCommandMode
TELEMETRY_COMMAND_MODE_START: TelemetryCommandMode
TELEMETRY_COMMAND_MODE_RESTART: TelemetryCommandMode
CHAT_COMMAND_MODE_UNKNOWN: ChatCommandMode
CHAT_COMMAND_MODE_MACRO: ChatCommandMode
CHAT_COMMAND_MODE_BEGIN_CHAT: ChatCommandMode
CHAT_COMMAND_MODE_REPLY: ChatCommandMode
CHAT_COMMAND_MODE_CANCEL: ChatCommandMode
CAMERA_STATE_UNKNOWN: CameraState
CAMERA_STATE_CAMERA_TOOL_ACTIVE: CameraState
CAMERA_STATE_UI_HIDDEN: CameraState
CAMERA_STATE_USE_AUTO_SHOT_SELECTION: CameraState
CAMERA_STATE_USE_TEMPORARY_EDITS: CameraState
CAMERA_STATE_USE_KEY_ACCELERATION: CameraState
CAMERA_STATE_USE_KEY10X_ACCELERATION: CameraState
CAMERA_STATE_USE_MOUSE_AIM_MODE: CameraState
REPLAY_POSITION_MODE_UNKNOWN: ReplayPositionMode
REPLAY_POSITION_MODE_BEGIN: ReplayPositionMode
REPLAY_POSITION_MODE_CURRENT: ReplayPositionMode
REPLAY_POSITION_MODE_END: ReplayPositionMode
REPLAY_SEARCH_MODE_UNKNOWN: ReplaySearchMode
REPLAY_SEARCH_MODE_TO_START: ReplaySearchMode
REPLAY_SEARCH_MODE_TO_END: ReplaySearchMode
REPLAY_SEARCH_MODE_PREVIOUS_SESSION: ReplaySearchMode
REPLAY_SEARCH_MODE_NEXT_SESSION: ReplaySearchMode
REPLAY_SEARCH_MODE_PREVIOUS_LAP: ReplaySearchMode
REPLAY_SEARCH_MODE_NEXT_LAP: ReplaySearchMode
REPLAY_SEARCH_MODE_PREVIOUS_FRAME: ReplaySearchMode
REPLAY_SEARCH_MODE_NEXT_FRAME: ReplaySearchMode
REPLAY_SEARCH_MODE_PREVIOUS_INCIDENT: ReplaySearchMode
REPLAY_SEARCH_MODE_NEXT_INCIDENT: ReplaySearchMode
PIT_COMMAND_MODE_UNKNOWN: PitCommandMode
PIT_COMMAND_MODE_CLEAR: PitCommandMode
PIT_COMMAND_MODE_TEAR_OFF: PitCommandMode
PIT_COMMAND_MODE_FUEL: PitCommandMode
PIT_COMMAND_MODE_LF_TIRE: PitCommandMode
PIT_COMMAND_MODE_RF_TIRE: PitCommandMode
PIT_COMMAND_MODE_LR_TIRE: PitCommandMode
PIT_COMMAND_MODE_RR_TIRE: PitCommandMode
PIT_COMMAND_MODE_CLEAR_TIRES: PitCommandMode
PIT_COMMAND_MODE_FAST_REPAIR: PitCommandMode
PIT_COMMAND_MODE_CLEAR_TEAR_OFF: PitCommandMode
PIT_COMMAND_MODE_CLEAR_FAST_REPAIR: PitCommandMode
PIT_COMMAND_MODE_CLEAR_FUEL: PitCommandMode
REPLAY_STATE_MODE_UNKNOWN: ReplayStateMode
REPLAY_STATE_MODE_ERASE_TAPE: ReplayStateMode
VIDEO_CAPTURE_MODE_UNKNOWN: VideoCaptureMode
VIDEO_CAPTURE_MODE_SCREENSHOT: VideoCaptureMode
VIDEO_CAPTURE_MODE_START: VideoCaptureMode
VIDEO_CAPTURE_MODE_STOP: VideoCaptureMode
VIDEO_CAPTURE_MODE_TOGGLE: VideoCaptureMode
VIDEO_CAPTURE_MODE_SHOW_TIMER: VideoCaptureMode
VIDEO_CAPTURE_MODE_HIDE_TIMER: VideoCaptureMode
FORCE_FEEDBACK_COMMAND_MODE_UNKNOWN: ForceFeedbackCommandMode
FORCE_FEEDBACK_COMMAND_MODE_MAX_FORCE: ForceFeedbackCommandMode

class CameraSwitchPositionRequest(_message.Message):
    __slots__ = ("position", "group", "camera")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    position: int
    group: int
    camera: int
    def __init__(self, position: _Optional[int] = ..., group: _Optional[int] = ..., camera: _Optional[int] = ...) -> None: ...

class CameraSwitchPositionResponse(_message.Message):
    __slots__ = ("car_index", "group", "camera")
    CAR_INDEX_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    car_index: int
    group: int
    camera: int
    def __init__(self, car_index: _Optional[int] = ..., group: _Optional[int] = ..., camera: _Optional[int] = ...) -> None: ...

class CameraSwitchNumberRequest(_message.Message):
    __slots__ = ("car_number", "group", "camera")
    CAR_NUMBER_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    car_number: str
    group: int
    camera: int
    def __init__(self, car_number: _Optional[str] = ..., group: _Optional[int] = ..., camera: _Optional[int] = ...) -> None: ...

class CameraSwitchNumberResponse(_message.Message):
    __slots__ = ("car_index", "group", "camera")
    CAR_INDEX_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    car_index: int
    group: int
    camera: int
    def __init__(self, car_index: _Optional[int] = ..., group: _Optional[int] = ..., camera: _Optional[int] = ...) -> None: ...

class CameraSetStateRequest(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: CameraState
    def __init__(self, state: _Optional[_Union[CameraState, str]] = ...) -> None: ...

class CameraSetStateResponse(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: CameraState
    def __init__(self, state: _Optional[_Union[CameraState, str]] = ...) -> None: ...

class ReplaySetPlaySpeedRequest(_message.Message):
    __slots__ = ("speed", "is_slow_motion")
    SPEED_FIELD_NUMBER: _ClassVar[int]
    IS_SLOW_MOTION_FIELD_NUMBER: _ClassVar[int]
    speed: int
    is_slow_motion: bool
    def __init__(self, speed: _Optional[int] = ..., is_slow_motion: bool = ...) -> None: ...

class ReplaySetPlaySpeedResponse(_message.Message):
    __slots__ = ("speed", "is_slow_motion")
    SPEED_FIELD_NUMBER: _ClassVar[int]
    IS_SLOW_MOTION_FIELD_NUMBER: _ClassVar[int]
    speed: int
    is_slow_motion: bool
    def __init__(self, speed: _Optional[int] = ..., is_slow_motion: bool = ...) -> None: ...

class ReplaySetPlayPositionRequest(_message.Message):
    __slots__ = ("mode", "frame")
    MODE_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    mode: ReplayPositionMode
    frame: int
    def __init__(self, mode: _Optional[_Union[ReplayPositionMode, str]] = ..., frame: _Optional[int] = ...) -> None: ...

class ReplaySetPlayPositionResponse(_message.Message):
    __slots__ = ("frame",)
    FRAME_FIELD_NUMBER: _ClassVar[int]
    frame: int
    def __init__(self, frame: _Optional[int] = ...) -> None: ...

class ReplaySearchRequest(_message.Message):
    __slots__ = ("mode",)
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: ReplaySearchMode
    def __init__(self, mode: _Optional[_Union[ReplaySearchMode, str]] = ...) -> None: ...

class ReplaySearchResponse(_message.Message):
    __slots__ = ("frame", "session_number", "session_time")
    FRAME_FIELD_NUMBER: _ClassVar[int]
    SESSION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SESSION_TIME_FIELD_NUMBER: _ClassVar[int]
    frame: int
    session_number: int
    session_time: float
    def __init__(self, frame: _Optional[int] = ..., session_number: _Optional[int] = ..., session_time: _Optional[float] = ...) -> None: ...

class ReplaySetStateRequest(_message.Message):
    __slots__ = ("state",)
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: ReplayStateMode
    def __init__(self, state: _Optional[_Union[ReplayStateMode, str]] = ...) -> None: ...

class ReplaySetStateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ReloadTexturesRequest(_message.Message):
    __slots__ = ("car_idx",)
    CAR_IDX_FIELD_NUMBER: _ClassVar[int]
    car_idx: int
    def __init__(self, car_idx: _Optional[int] = ...) -> None: ...

class ReloadTexturesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ChatCommandRequest(_message.Message):
    __slots__ = ("mode", "macro")
    MODE_FIELD_NUMBER: _ClassVar[int]
    MACRO_FIELD_NUMBER: _ClassVar[int]
    mode: ChatCommandMode
    macro: int
    def __init__(self, mode: _Optional[_Union[ChatCommandMode, str]] = ..., macro: _Optional[int] = ...) -> None: ...

class ChatCommandResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PitCommandRequest(_message.Message):
    __slots__ = ("mode", "value")
    MODE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    mode: PitCommandMode
    value: float
    def __init__(self, mode: _Optional[_Union[PitCommandMode, str]] = ..., value: _Optional[float] = ...) -> None: ...

class PitCommandResponse(_message.Message):
    __slots__ = ("service_flags", "fuel", "lf_pressure", "rf_pressure", "lr_pressure", "rr_pressure", "tire_compound")
    SERVICE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    FUEL_FIELD_NUMBER: _ClassVar[int]
    LF_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    RF_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    LR_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    RR_PRESSURE_FIELD_NUMBER: _ClassVar[int]
    TIRE_COMPOUND_FIELD_NUMBER: _ClassVar[int]
    service_flags: int
    fuel: float
    lf_pressure: float
    rf_pressure: float
    lr_pressure: float
    rr_pressure: float
    tire_compound: int
    def __init__(self, service_flags: _Optional[int] = ..., fuel: _Optional[float] = ..., lf_pressure: _Optional[float] = ..., rf_pressure: _Optional[float] = ..., lr_pressure: _Optional[float] = ..., rr_pressure: _Optional[float] = ..., tire_compound: _Optional[int] = ...) -> None: ...

class TelemetryCommandRequest(_message.Message):
    __slots__ = ("mode",)
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: TelemetryCommandMode
    def __init__(self, mode: _Optional[_Union[TelemetryCommandMode, str]] = ...) -> None: ...

class TelemetryCommandResponse(_message.Message):
    __slots__ = ("is_disk_logging_enabled", "is_disk_logging_active")
    IS_DISK_LOGGING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_DISK_LOGGING_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    is_disk_logging_enabled: bool
    is_disk_logging_active: bool
    def __init__(self, is_disk_logging_enabled: bool = ..., is_disk_logging_active: bool = ...) -> None: ...

class ForceFeedbackCommandRequest(_message.Message):
    __slots__ = ("mode", "value")
    MODE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    mode: ForceFeedbackCommandMode
    value: float
    def __init__(self, mode: _Optional[_Union[ForceFeedbackCommandMode, str]] = ..., value: _Optional[float] = ...) -> None: ...

class ForceFeedbackCommandResponse(_message.Message):
    __slots__ = ("max_force",)
    MAX_FORCE_FIELD_NUMBER: _ClassVar[int]
    max_force: float
    def __init__(self, max_force: _Optional[float] = ...) -> None: ...

class ReplaySearchSessionTimeRequest(_message.Message):
    __slots__ = ("session_number", "session_time_ms")
    SESSION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SESSION_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    session_number: int
    session_time_ms: float
    def __init__(self, session_number: _Optional[int] = ..., session_time_ms: _Optional[float] = ...) -> None: ...

class ReplaySearchSessionTimeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class VideoCaptureRequest(_message.Message):
    __slots__ = ("mode",)
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: VideoCaptureMode
    def __init__(self, mode: _Optional[_Union[VideoCaptureMode, str]] = ...) -> None: ...

class VideoCaptureResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CameraDetail(_message.Message):
    __slots__ = ("number", "name")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    number: int
    name: str
    def __init__(self, number: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class CameraGroup(_message.Message):
    __slots__ = ("number", "name", "cameras")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAMERAS_FIELD_NUMBER: _ClassVar[int]
    number: int
    name: str
    cameras: _containers.RepeatedCompositeFieldContainer[CameraDetail]
    def __init__(self, number: _Optional[int] = ..., name: _Optional[str] = ..., cameras: _Optional[_Iterable[_Union[CameraDetail, _Mapping]]] = ...) -> None: ...

class GetAvailableCamerasResponse(_message.Message):
    __slots__ = ("camera_groups", "car_index", "group", "camera")
    CAMERA_GROUPS_FIELD_NUMBER: _ClassVar[int]
    CAR_INDEX_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    CAMERA_FIELD_NUMBER: _ClassVar[int]
    camera_groups: _containers.RepeatedCompositeFieldContainer[CameraGroup]
    car_index: int
    group: int
    camera: int
    def __init__(self, camera_groups: _Optional[_Iterable[_Union[CameraGroup, _Mapping]]] = ..., car_index: _Optional[int] = ..., group: _Optional[int] = ..., camera: _Optional[int] = ...) -> None: ...
