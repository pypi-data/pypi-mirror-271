from v4_proto.gogoproto import gogo_pb2 as _gogo_pb2
from v4_proto.google.api import annotations_pb2 as _annotations_pb2
from v4_proto.dydxprotocol.ratelimit import limit_params_pb2 as _limit_params_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListLimitParamsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListLimitParamsResponse(_message.Message):
    __slots__ = ("limit_params_list",)
    LIMIT_PARAMS_LIST_FIELD_NUMBER: _ClassVar[int]
    limit_params_list: _containers.RepeatedCompositeFieldContainer[_limit_params_pb2.LimitParams]
    def __init__(self, limit_params_list: _Optional[_Iterable[_Union[_limit_params_pb2.LimitParams, _Mapping]]] = ...) -> None: ...

class QueryCapacityByDenomRequest(_message.Message):
    __slots__ = ("denom",)
    DENOM_FIELD_NUMBER: _ClassVar[int]
    denom: str
    def __init__(self, denom: _Optional[str] = ...) -> None: ...

class CapacityResult(_message.Message):
    __slots__ = ("period_sec", "capacity")
    PERIOD_SEC_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    period_sec: int
    capacity: bytes
    def __init__(self, period_sec: _Optional[int] = ..., capacity: _Optional[bytes] = ...) -> None: ...

class QueryCapacityByDenomResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[CapacityResult]
    def __init__(self, results: _Optional[_Iterable[_Union[CapacityResult, _Mapping]]] = ...) -> None: ...
