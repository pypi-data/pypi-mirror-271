from fintekkers.models.security import security_pb2 as _security_pb2
from fintekkers.models.position import position_pb2 as _position_pb2
from fintekkers.models.price import price_pb2 as _price_pb2
from fintekkers.requests.util import operation_pb2 as _operation_pb2
from fintekkers.models.position import measure_pb2 as _measure_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ValuationRequestProto(_message.Message):
    __slots__ = ["measures", "object_class", "operation_type", "position_input", "price_input", "security_input", "version"]
    MEASURES_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CLASS_FIELD_NUMBER: _ClassVar[int]
    OPERATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSITION_INPUT_FIELD_NUMBER: _ClassVar[int]
    PRICE_INPUT_FIELD_NUMBER: _ClassVar[int]
    SECURITY_INPUT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    measures: _containers.RepeatedScalarFieldContainer[_measure_pb2.MeasureProto]
    object_class: str
    operation_type: _operation_pb2.RequestOperationTypeProto
    position_input: _position_pb2.PositionProto
    price_input: _price_pb2.PriceProto
    security_input: _security_pb2.SecurityProto
    version: str
    def __init__(self, object_class: _Optional[str] = ..., version: _Optional[str] = ..., operation_type: _Optional[_Union[_operation_pb2.RequestOperationTypeProto, str]] = ..., measures: _Optional[_Iterable[_Union[_measure_pb2.MeasureProto, str]]] = ..., security_input: _Optional[_Union[_security_pb2.SecurityProto, _Mapping]] = ..., position_input: _Optional[_Union[_position_pb2.PositionProto, _Mapping]] = ..., price_input: _Optional[_Union[_price_pb2.PriceProto, _Mapping]] = ...) -> None: ...
