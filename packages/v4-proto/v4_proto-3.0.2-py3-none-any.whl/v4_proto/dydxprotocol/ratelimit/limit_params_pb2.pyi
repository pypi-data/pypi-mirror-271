from v4_proto.gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LimitParams(_message.Message):
    __slots__ = ("denom", "limiters")
    DENOM_FIELD_NUMBER: _ClassVar[int]
    LIMITERS_FIELD_NUMBER: _ClassVar[int]
    denom: str
    limiters: _containers.RepeatedCompositeFieldContainer[Limiter]
    def __init__(self, denom: _Optional[str] = ..., limiters: _Optional[_Iterable[_Union[Limiter, _Mapping]]] = ...) -> None: ...

class Limiter(_message.Message):
    __slots__ = ("period_sec", "baseline_minimum", "baseline_tvl_ppm")
    PERIOD_SEC_FIELD_NUMBER: _ClassVar[int]
    BASELINE_MINIMUM_FIELD_NUMBER: _ClassVar[int]
    BASELINE_TVL_PPM_FIELD_NUMBER: _ClassVar[int]
    period_sec: int
    baseline_minimum: bytes
    baseline_tvl_ppm: int
    def __init__(self, period_sec: _Optional[int] = ..., baseline_minimum: _Optional[bytes] = ..., baseline_tvl_ppm: _Optional[int] = ...) -> None: ...
