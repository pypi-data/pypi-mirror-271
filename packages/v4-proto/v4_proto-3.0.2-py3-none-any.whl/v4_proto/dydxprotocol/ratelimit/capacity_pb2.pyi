from v4_proto.gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DenomCapacity(_message.Message):
    __slots__ = ("denom", "capacity_list")
    DENOM_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_LIST_FIELD_NUMBER: _ClassVar[int]
    denom: str
    capacity_list: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, denom: _Optional[str] = ..., capacity_list: _Optional[_Iterable[bytes]] = ...) -> None: ...
