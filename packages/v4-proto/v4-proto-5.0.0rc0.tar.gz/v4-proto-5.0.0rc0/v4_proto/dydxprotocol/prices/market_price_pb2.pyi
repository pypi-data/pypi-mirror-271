from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MarketPrice(_message.Message):
    __slots__ = ("id", "exponent", "price")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXPONENT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    id: int
    exponent: int
    price: int
    def __init__(self, id: _Optional[int] = ..., exponent: _Optional[int] = ..., price: _Optional[int] = ...) -> None: ...
