# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fintekkers/requests/security/query_security_request.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fintekkers.models.util import uuid_pb2 as fintekkers_dot_models_dot_util_dot_uuid__pb2
from fintekkers.models.util import local_timestamp_pb2 as fintekkers_dot_models_dot_util_dot_local__timestamp__pb2
from fintekkers.models.position import position_filter_pb2 as fintekkers_dot_models_dot_position_dot_position__filter__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9fintekkers/requests/security/query_security_request.proto\x12\x1c\x66intekkers.requests.security\x1a!fintekkers/models/util/uuid.proto\x1a,fintekkers/models/util/local_timestamp.proto\x1a\x30\x66intekkers/models/position/position_filter.proto\"\x80\x02\n\x19QuerySecurityRequestProto\x12\x14\n\x0cobject_class\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x30\n\x05uuIds\x18\x15 \x03(\x0b\x32!.fintekkers.models.util.UUIDProto\x12N\n\x15search_security_input\x18\x16 \x01(\x0b\x32/.fintekkers.models.position.PositionFilterProto\x12:\n\x05\x61s_of\x18\x17 \x01(\x0b\x32+.fintekkers.models.util.LocalTimestampProtoB\x1e\x42\x1aQuerySecurityRequestProtosP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fintekkers.requests.security.query_security_request_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'B\032QuerySecurityRequestProtosP\001'
  _QUERYSECURITYREQUESTPROTO._serialized_start=223
  _QUERYSECURITYREQUESTPROTO._serialized_end=479
# @@protoc_insertion_point(module_scope)
