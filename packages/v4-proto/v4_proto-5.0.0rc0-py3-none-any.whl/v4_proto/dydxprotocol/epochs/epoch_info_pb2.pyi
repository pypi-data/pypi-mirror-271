from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EpochInfo(_message.Message):
    __slots__ = ("name", "next_tick", "duration", "current_epoch", "current_epoch_start_block", "is_initialized", "fast_forward_next_tick")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NEXT_TICK_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    CURRENT_EPOCH_FIELD_NUMBER: _ClassVar[int]
    CURRENT_EPOCH_START_BLOCK_FIELD_NUMBER: _ClassVar[int]
    IS_INITIALIZED_FIELD_NUMBER: _ClassVar[int]
    FAST_FORWARD_NEXT_TICK_FIELD_NUMBER: _ClassVar[int]
    name: str
    next_tick: int
    duration: int
    current_epoch: int
    current_epoch_start_block: int
    is_initialized: bool
    fast_forward_next_tick: bool
    def __init__(self, name: _Optional[str] = ..., next_tick: _Optional[int] = ..., duration: _Optional[int] = ..., current_epoch: _Optional[int] = ..., current_epoch_start_block: _Optional[int] = ..., is_initialized: bool = ..., fast_forward_next_tick: bool = ...) -> None: ...
