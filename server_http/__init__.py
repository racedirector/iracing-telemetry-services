from io import StringIO
from iracing.iracing_service import IRacingService

class CaptureOnCloseBuffer:
    def __init__(self):
        self._buffer = StringIO()
        self._content = None

    def write(self, data):
        self._buffer.write(data)
    
    def close(self):
        self._buffer.seek(0)
        self._content = self._buffer.read()
        self._buffer.close()

    def getvalue(self):
        if self._content is not None:
            return self._content
        else:
            self._buffer.seek(0)
            return self._buffer.read()

'''
Mock the `open` function to avoid file I/O from irsdk for things like
dumping all telemetry data.
'''
def make_mock_open(buffer):
    def mock_open(*args, **kwargs):
        return buffer
    return mock_open