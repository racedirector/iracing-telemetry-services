from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetTelemetryTypesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTelemetryTypesResponse(_message.Message):
    __slots__ = ("types",)
    TYPES_FIELD_NUMBER: _ClassVar[int]
    types: _struct_pb2.Struct
    def __init__(self, types: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GetTelemetryJSONSchemaRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTelemetryJSONSchemaResponse(_message.Message):
    __slots__ = ("telemetry", "session")
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    telemetry: _struct_pb2.Struct
    session: _struct_pb2.Struct
    def __init__(self, telemetry: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., session: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class GetTelemetryJSONSchemaStringResponse(_message.Message):
    __slots__ = ("telemetry", "session")
    TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    SESSION_FIELD_NUMBER: _ClassVar[int]
    telemetry: str
    session: str
    def __init__(self, telemetry: _Optional[str] = ..., session: _Optional[str] = ...) -> None: ...
