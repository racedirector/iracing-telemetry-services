from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from google.protobuf.empty_pb2 import Empty as Empty

DESCRIPTOR: _descriptor.FileDescriptor

class TelemetrySubscriptionRequest(_message.Message):
    __slots__ = ("fps", "keys")
    FPS_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    fps: int
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fps: _Optional[int] = ..., keys: _Optional[_Iterable[str]] = ...) -> None: ...

class GetTelemetryRequest(_message.Message):
    __slots__ = ("keys",)
    KEYS_FIELD_NUMBER: _ClassVar[int]
    keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, keys: _Optional[_Iterable[str]] = ...) -> None: ...

class GetTelemetryResponse(_message.Message):
    __slots__ = ("telemetry",)
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    telemetry: _struct_pb2.Struct
    def __init__(self, telemetry: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
