
import struct
from irsdk import (
  IRSDK,
  VAR_TYPE_MAP,
  YAML_CODE_PAGE,
)
from iracing.schema import json_schema_for_session, json_schema_for_telemetry


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

  def get_session_string(self):
    if not self.check_connection():
      return None

    session_binary = self.client._shared_mem[self.client._header.session_info_offset:self.client._header.session_info_len].rstrip(b'\x00').decode(YAML_CODE_PAGE)

    return session_binary
  
  def dump_telemetry(self):
    if not self.check_connection():
      return None

    telemetry = {}
    self.client.freeze_var_buffer_latest()

    # Get all the headers from the buffer
    for key in self.client._var_headers_dict:
      var_header = self.client._var_headers_dict[key]
      var_buf_latest = self.client._var_buffer_latest
      res = struct.unpack_from(
        VAR_TYPE_MAP[var_header.type] * var_header.count,
        var_buf_latest.get_memory(),
        var_buf_latest.buf_offset + var_header.offset)
      
      telemetry[key] = res[0] if var_header.count == 1 else list(res)

    self.client.unfreeze_var_buffer_latest()

    return telemetry

  def __update_schema(self):
    self.client.freeze_var_buffer_latest()

    telemetry_schema = json_schema_for_telemetry(self.client)
    session_schema = json_schema_for_session(self.client)

    self.client.unfreeze_var_buffer_latest()

    self.telemetry_schema = telemetry_schema.to_schema()
    self.session_schema = session_schema.to_schema()