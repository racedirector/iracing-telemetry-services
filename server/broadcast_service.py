from irsdk import IRSDK
from server.proto import broadcast_pb2_grpc
from server.proto import broadcast_pb2
from server.iracing_service import IRacingService
from server.util import get_camera_state_from_request, get_replay_position_mode_from_request, get_replay_search_mode_from_request, get_replay_state_mode_from_request, get_chat_command_mode_from_request, get_pit_command_mode_from_request, get_telemetry_command_mode_from_request, get_ffb_command_mode_from_request, get_video_capture_mode_from_request

class BroadcastService(IRacingService, broadcast_pb2_grpc.BroadcastServicer):
  """Servicer that manages broadcast data."""

  def __init__(self, ir: IRSDK):
    super().__init__(ir)

  def GetAvailableCameras(self, request: broadcast_pb2.Empty, context):
    if self.check_is_connected(context):
      return broadcast_pb2.GetAvailableCamerasResponse(
        car_index=self.ir['CamCarIdx'],
        group=self.ir['CamGroupNumber'],
        camera=self.ir['CamCameraNumber'],
        camera_groups=[broadcast_pb2.CameraGroup(
          number=group['GroupNum'],
          name=group['GroupName'],
          cameras=[broadcast_pb2.CameraDetail(
            number=camera['CameraNum'],
            name=camera['CameraName'],
        ) for camera in group['Cameras']]) for group in self.ir['CameraInfo']['Groups']])

    return broadcast_pb2.GetAvailableCamerasResponse()

  def CameraSwitchPosition(self, request: broadcast_pb2.CameraSwitchPositionRequest, context):
    if self.check_is_connected(context):
      self.ir.cam_switch_pos(
        position=request.position,
        group=request.group,
        camera=request.camera
      )

      self.ir.freeze_var_buffer_latest()
      response = broadcast_pb2.CameraSwitchPositionResponse(
        car_index=self.ir['CamCarIdx'],
        group=self.ir['CamGroupNumber'],
        camera=self.ir['CamCameraNumber'],
      )
      self.ir.unfreeze_var_buffer_latest()

      return response

    return broadcast_pb2.CameraSwitchPositionResponse()
  
  def CameraSwitchNumber(self, request: broadcast_pb2.CameraSwitchNumberRequest, context):
    if self.check_is_connected(context):
      self.ir.cam_switch_num(
        car_number=request.car_number,
        group=request.group,
        camera=request.camera
      )

      self.ir.freeze_var_buffer_latest()
      response = broadcast_pb2.CameraSwitchPositionResponse(
        car_index=self.ir['CamCarIdx'],
        group=self.ir['CamGroupNumber'],
        camera=self.ir['CamCameraNumber'],
      )
      self.ir.unfreeze_var_buffer_latest()

      return response

    return broadcast_pb2.CameraSwitchNumberResponse()

  def CameraSetState(self, request: broadcast_pb2.CameraSetStateRequest, context):
    if self.check_is_connected(context):
      self.ir.cam_set_state(get_camera_state_from_request(request))

      self.ir.freeze_var_buffer_latest()
      response = broadcast_pb2.CameraSetStateResponse(
        state=self.ir['CamCameraState']
      )
      self.ir.unfreeze_var_buffer_latest()

      return response
    
    return broadcast_pb2.CameraSetStateResponse()
  
  def ReplaySetPlaySpeed(self, request: broadcast_pb2.ReplaySetPlaySpeedRequest, context):
    if self.check_is_connected(context):
      self.ir.replay_set_play_speed(
        speed=request.speed,
        slow_motion=request.is_slow_motion
      )

      self.ir.freeze_var_buffer_latest()
      response = broadcast_pb2.ReplaySetPlaySpeedResponse(
        speed=self.ir['ReplayPlaySpeed'],
        is_slow_motion=self.ir['ReplayPlaySlowMotion']
      )
      self.ir.unfreeze_var_buffer_latest()

      return response

    return broadcast_pb2.ReplaySetPlaySpeedResponse()
  
  def ReplaySetPlayPosition(self, request: broadcast_pb2.ReplaySetPlayPositionRequest, context):
    if self.check_is_connected(context):
      self.ir.replay_set_play_position(
        pos_mode=get_replay_position_mode_from_request(request),
        frame_num=request.frame
      )

      self.ir.freeze_var_buffer_latest()
      response = broadcast_pb2.ReplaySetPlayPositionResponse(
        frame=self.ir['ReplayFrameNum']
      )
      self.ir.unfreeze_var_buffer_latest()

      return response
    
    return broadcast_pb2.ReplaySetPlayPositionResponse()
  
  def ReplaySearch(self, request: broadcast_pb2.ReplaySearchRequest, context):
    if self.check_is_connected(context):
      self.ir.replay_search(
        search_mode=get_replay_search_mode_from_request(request),
      )

    return broadcast_pb2.ReplaySearchResponse()
  
  def ReplaySetState(self, request: broadcast_pb2.ReplaySetStateRequest, context):
    if self.check_is_connected(context):
      self.ir.replay_set_state(state_mode=get_replay_state_mode_from_request(request))

    return broadcast_pb2.ReplaySetStateResponse()
  
  def ReloadTextures(self, request: broadcast_pb2.ReloadTexturesRequest, context):
    if self.check_is_connected(context):
      if request.HasField('car_idx'):
        self.ir.reload_texture(request.car_idx)
      else:
        self.ir.reload_all_textures()

    return broadcast_pb2.ReloadTexturesResponse()
  
  def ChatCommand(self, request: broadcast_pb2.ChatCommandRequest, context):
    if self.check_is_connected(context):
      is_macro = request.mode == broadcast_pb2.ChatCommandMode.CHAT_COMMAND_MODE_MACRO
      if is_macro and request.HasField('macro'):
        self.ir.chat_command_macro(macro_num=request.macro)
      elif not is_macro:
        self.ir.chat_command(chat_command_mode=get_chat_command_mode_from_request(request))

    return broadcast_pb2.ChatCommandResponse()
  
  def PitCommand(self, request: broadcast_pb2.PitCommandRequest, context):
    if self.check_is_connected(context):
      self.ir.pit_command(
        pit_command_mode=get_pit_command_mode_from_request(request),
        var=request.value
      )

      self.ir.freeze_var_buffer_latest()
      response = broadcast_pb2.PitCommandResponse(
        service_flags=self.ir['PitSvFlags'],
        fuel=self.ir['PitSvFuel'],
        lf_pressure=self.ir['PitSvLFP'],
        rf_pressure=self.ir['PitSvRFP'],
        lr_pressure=self.ir['PitSvLRP'],
        rr_pressure=self.ir['PitSvRRP'],
        tire_compound=self.ir['PitSvTireCompound'],
      )
      self.ir.unfreeze_var_buffer_latest()
      
      return response
    
    return broadcast_pb2.PitCommandResponse()
  
  '''
  Iterate over the stream of pit commands and execute them one-by-one.
  Respond with a single PitCommandResponse after all commands have been executed.
  '''
  def PitCommandStream(self, request_iterator, context):
    if self.check_is_connected(context):
      for request in request_iterator:
        self.ir.pit_command(
          pit_command_mode=get_pit_command_mode_from_request(request),
          var=request.value
        )

      self.ir.freeze_var_buffer_latest()
      response = broadcast_pb2.PitCommandResponse(
        service_flags=self.ir['PitSvFlags'],
        fuel=self.ir['PitSvFuel'],
        lf_pressure=self.ir['PitSvLFP'],
        rf_pressure=self.ir['PitSvRFP'],
        lr_pressure=self.ir['PitSvLRP'],
        rr_pressure=self.ir['PitSvRRP'],
        tire_compound=self.ir['PitSvTireCompound'],
      )
      self.ir.unfreeze_var_buffer_latest()
      return response

    return broadcast_pb2.PitCommandResponse()

  def TelemetryCommand(self, request: broadcast_pb2.TelemetryCommandRequest, context):
    if self.check_is_connected(context):
      self.ir.telem_command(
        telem_command_mode=get_telemetry_command_mode_from_request(request),
      )

      self.ir.freeze_var_buffer_latest()
      response = broadcast_pb2.TelemetryCommandResponse(
        is_disk_logging_active=self.ir['IsDiskLoggingActive'],
        is_disk_logging_enabled=self.ir['IsDiskLoggingEnabled'],
      )
      self.ir.unfreeze_var_buffer_latest()

      return response

    return broadcast_pb2.TelemetryCommandResponse()
  
  def ForceFeedbackCommand(self, request: broadcast_pb2.ForceFeedbackCommandRequest, context):
    if self.check_is_connected(context):
      self.ir.ffb_command(
        ffb_command_mode=get_ffb_command_mode_from_request(request),
        value=request.value
      )

      self.ir.freeze_var_buffer_latest()
      response = broadcast_pb2.ForceFeedbackCommandResponse(
        max_force=self.ir['SteeringWheelMaxForceNm'],
      )
      self.ir.unfreeze_var_buffer_latest()
      return response
    
    return broadcast_pb2.ForceFeedbackCommandResponse()
  
  def ReplaySearchSessionTime(self, request: broadcast_pb2.ReplaySearchSessionTimeRequest, context):
    if self.check_is_connected(context):
      self.ir.replay_search_session_time(
        session_num=request.session_number,
        session_time_ms=request.session_time_ms
      )
    
    return broadcast_pb2.ReplaySearchSessionTimeResponse()
  
  def VideoCapture(self, request: broadcast_pb2.VideoCaptureRequest, context):
    if self.check_is_connected(context):
      self.ir.video_capture(
        video_capture_mode=get_video_capture_mode_from_request(request),
      )

    return broadcast_pb2.VideoCaptureResponse()
 