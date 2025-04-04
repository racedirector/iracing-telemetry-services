from server.proto import broadcast_pb2
from irsdk import CameraState, RpyPosMode, RpyStateMode, RpySrchMode, ChatCommandMode, PitCommandMode, TelemCommandMode, FFBCommandMode, VideoCaptureMode

def get_camera_state_from_request(request: broadcast_pb2.CameraSetStateRequest) -> CameraState:
  match request.state:
    case broadcast_pb2.CameraState.CAMERA_STATE_UNKNOWN | broadcast_pb2.CameraState.CAMERA_STATE_CAMERA_TOOL_ACTIVE:
      return CameraState.cam_tool_active
    case broadcast_pb2.CameraState.CAMERA_STATE_UI_HIDDEN:
      return CameraState.ui_hidden
    case broadcast_pb2.CameraState.CAMERA_STATE_USE_AUTO_SHOT_SELECTION:
      return CameraState.use_auto_shot_selection
    case broadcast_pb2.CameraState.CAMERA_STATE_USE_TEMPORARY_EDITS:
      return CameraState.use_temporary_edits
    case broadcast_pb2.CameraState.CAMERA_STATE_USE_KEY_ACCELERATION:
      return CameraState.use_key_acceleration
    case broadcast_pb2.CameraState.CAMERA_STATE_USE_KEY10X_ACCELERATION:
      return CameraState.use_key10x_acceleration
    case broadcast_pb2.CameraState.CAMERA_STATE_USE_MOUSE_AIM_MODE:
      return CameraState.use_mouse_aim_mode
    case _:
      raise ValueError(f"Unknown camera state: {request.state}")
    
def get_replay_position_mode_from_request(request: broadcast_pb2.ReplaySetPlayPositionRequest) -> RpyPosMode:
  match request.mode:
    case broadcast_pb2.ReplayPositionMode.REPLAY_POSITION_MODE_UNKNOWN | broadcast_pb2.ReplayPositionMode.REPLAY_POSITION_MODE_BEGIN:
      return RpyPosMode.begin
    case broadcast_pb2.ReplayPositionMode.REPLAY_POSITION_MODE_CURRENT:
      return RpyPosMode.current
    case broadcast_pb2.ReplayPositionMode.REPLAY_POSITION_MODE_END:
      return RpyPosMode.end
    case _:
      raise ValueError(f"Unknown replay position mode: {request.mode}")

def get_replay_state_mode_from_request(request: broadcast_pb2.ReplaySetStateRequest):
  match request.state:
    case broadcast_pb2.ReplayStateMode.REPLAY_STATE_MODE_UNKNOWN | broadcast_pb2.ReplayStateMode.REPLAY_STATE_MODE_ERASE_TAPE:
      return RpyStateMode.erase_tape
    case _:
      raise ValueError(f"Unknown replay state mode: {request.state}")

def get_replay_search_mode_from_request(request: broadcast_pb2.ReplaySearchRequest):
  match request.mode:
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_UNKNOWN | broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_TO_START:
      return RpySrchMode.to_start
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_TO_END:
      return RpySrchMode.to_end
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_PREVIOUS_SESSION:
      return RpySrchMode.prev_session
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_NEXT_SESSION:
      return RpySrchMode.next_session
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_PREVIOUS_LAP:
      return RpySrchMode.prev_lap
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_NEXT_LAP:
      return RpySrchMode.next_lap
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_PREVIOUS_FRAME:
      return RpySrchMode.prev_frame
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_NEXT_FRAME:
      return RpySrchMode.next_frame
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_PREVIOUS_INCIDENT:
      return RpySrchMode.prev_incident
    case broadcast_pb2.ReplaySearchMode.REPLAY_SEARCH_MODE_NEXT_INCIDENT:
      return RpySrchMode.next_incident
    case _:
      raise ValueError(f"Unknown replay search mode: {request.mode}")

def get_chat_command_mode_from_request(request: broadcast_pb2.ChatCommandRequest):
  match request.mode:
    case broadcast_pb2.ChatCommandMode.CHAT_COMMAND_MODE_UNKNOWN | broadcast_pb2.ChatCommandMode.CHAT_COMMAND_MODE_MACRO:
      return ChatCommandMode.macro
    case broadcast_pb2.ChatCommandMode.CHAT_COMMAND_MODE_BEGIN_CHAT:
      return ChatCommandMode.begin_chat
    case broadcast_pb2.ChatCommandMode.CHAT_COMMAND_MODE_REPLY:
      return ChatCommandMode.reply
    case broadcast_pb2.ChatCommandMode.CHAT_COMMAND_MODE_CANCEL:
      return ChatCommandMode.cancel
    case _:
      raise ValueError(f"Unknown chat command mode: {request.mode}")

def get_pit_command_mode_from_request(request: broadcast_pb2.PitCommandRequest):
  match request.mode:
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_UNKNOWN | broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_CLEAR:
      return PitCommandMode.clear
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_TEAR_OFF:
      return PitCommandMode.ws
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_FUEL:
      return PitCommandMode.fuel
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_LF_TIRE:
      return PitCommandMode.lf
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_RF_TIRE:
      return PitCommandMode.rf
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_LR_TIRE:
      return PitCommandMode.lr
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_RR_TIRE:
      return PitCommandMode.rr
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_CLEAR_TIRES:
      return PitCommandMode.clear_tires
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_FAST_REPAIR:
      return PitCommandMode.fr
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_CLEAR_TEAR_OFF:
      return PitCommandMode.clear_ws
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_CLEAR_FAST_REPAIR:
      return PitCommandMode.clear_fr
    case broadcast_pb2.PitCommandMode.PIT_COMMAND_MODE_CLEAR_FUEL:
      return PitCommandMode.clear_fuel
    case _:
      raise ValueError(f"Unknown pit command mode: {request.mode}")

def get_telemetry_command_mode_from_request(request: broadcast_pb2.TelemetryCommandRequest):
  match request.mode:
    case broadcast_pb2.TelemetryCommandMode.TELEMETRY_COMMAND_MODE_UNKNOWN | broadcast_pb2.TelemetryCommandMode.TELEMETRY_COMMAND_MODE_STOP:
      return TelemCommandMode.stop
    case broadcast_pb2.TelemetryCommandMode.TELEMETRY_COMMAND_MODE_START:
      return TelemCommandMode.start
    case broadcast_pb2.TelemetryCommandMode.TELEMETRY_COMMAND_MODE_RESTART:
      return TelemCommandMode.restart
    case _:
      raise ValueError(f"Unknown telemetry command mode: {request.mode}")

def get_ffb_command_mode_from_request(request: broadcast_pb2.ForceFeedbackCommandRequest):
  return FFBCommandMode.ffb_command_max_force

def get_video_capture_mode_from_request(request: broadcast_pb2.VideoCaptureRequest):
  match request.mode:
    case broadcast_pb2.VideoCaptureMode.VIDEO_CAPTURE_MODE_UNKNOWN | broadcast_pb2.VideoCaptureMode.VIDEO_CAPTURE_MODE_SCREENSHOT:
      return VideoCaptureMode.trigger_screen_shot
    case broadcast_pb2.VideoCaptureMode.VIDEO_CAPTURE_MODE_START:
      return VideoCaptureMode.start_video_capture
    case broadcast_pb2.VideoCaptureMode.VIDEO_CAPTURE_MODE_STOP:
      return VideoCaptureMode.end_video_capture
    case broadcast_pb2.VideoCaptureMode.VIDEO_CAPTURE_MODE_TOGGLE:
      return VideoCaptureMode.toggle_video_capture
    case broadcast_pb2.VideoCaptureMode.VIDEO_CAPTURE_MODE_SHOW_TIMER:
      return VideoCaptureMode.show_video_timer
    case broadcast_pb2.VideoCaptureMode.VIDEO_CAPTURE_MODE_HIDE_TIMER:
      return VideoCaptureMode.hide_video_timer
    case _:
      raise ValueError(f"Unknown video capture mode: {request.mode}")
