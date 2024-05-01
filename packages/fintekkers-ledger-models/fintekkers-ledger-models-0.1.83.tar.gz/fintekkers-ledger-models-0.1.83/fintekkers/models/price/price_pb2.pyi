from fintekkers.models.util import decimal_value_pb2 as _decimal_value_pb2
from fintekkers.models.util import local_timestamp_pb2 as _local_timestamp_pb2
from fintekkers.models.util import uuid_pb2 as _uuid_pb2
from fintekkers.models.security import security_pb2 as _security_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PriceProto(_message.Message):
    __slots__ = ["as_of", "is_link", "object_class", "price", "security", "uuid", "valid_from", "valid_to", "version"]
    AS_OF_FIELD_NUMBER: _ClassVar[int]
    IS_LINK_FIELD_NUMBER: _ClassVar[int]
    OBJECT_CLASS_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    SECURITY_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    VALID_FROM_FIELD_NUMBER: _ClassVar[int]
    VALID_TO_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    as_of: _local_timestamp_pb2.LocalTimestampProto
    is_link: bool
    object_class: str
    price: _decimal_value_pb2.DecimalValueProto
    security: _security_pb2.SecurityProto
    uuid: _uuid_pb2.UUIDProto
    valid_from: _local_timestamp_pb2.LocalTimestampProto
    valid_to: _local_timestamp_pb2.LocalTimestampProto
    version: str
    def __init__(self, object_class: _Optional[str] = ..., version: _Optional[str] = ..., uuid: _Optional[_Union[_uuid_pb2.UUIDProto, _Mapping]] = ..., as_of: _Optional[_Union[_local_timestamp_pb2.LocalTimestampProto, _Mapping]] = ..., is_link: bool = ..., valid_from: _Optional[_Union[_local_timestamp_pb2.LocalTimestampProto, _Mapping]] = ..., valid_to: _Optional[_Union[_local_timestamp_pb2.LocalTimestampProto, _Mapping]] = ..., price: _Optional[_Union[_decimal_value_pb2.DecimalValueProto, _Mapping]] = ..., security: _Optional[_Union[_security_pb2.SecurityProto, _Mapping]] = ...) -> None: ...
