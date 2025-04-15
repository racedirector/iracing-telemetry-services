import grpc
from irsdk import IRSDK

class IRacingService:
  """Servicer that manages connection state to iRacing."""

  connected = False

  def __init__(self, ir: IRSDK):
    self.ir = ir

  def check_connection(self):
    if self.connected and not (self.ir.is_initialized and self.ir.is_connected):
      print("iRacing disconnected")
      self.connected = False
      self.ir.shutdown()
    elif not self.connected and self.ir.startup() and self.ir.is_initialized and self.ir.is_connected:
      print("iRacing connected")
      self.connected = True

    return self.connected

  def is_connected(self):
    return self.check_connection()
  
  def check_is_connected(self, context: grpc.ServicerContext):
      is_connected = self.is_connected()
      if not is_connected:
        context.set_details("Not connected to iRacing")
        context.set_code(grpc.StatusCode.INTERNAL)

      return is_connected
