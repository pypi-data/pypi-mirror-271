# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fintekkers/models/position/position_util.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from fintekkers.models.position import field_pb2 as fintekkers_dot_models_dot_position_dot_field__pb2
from fintekkers.models.position import measure_pb2 as fintekkers_dot_models_dot_position_dot_measure__pb2
from fintekkers.models.util import decimal_value_pb2 as fintekkers_dot_models_dot_util_dot_decimal__value__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.fintekkers/models/position/position_util.proto\x12\x1a\x66intekkers.models.position\x1a\x19google/protobuf/any.proto\x1a&fintekkers/models/position/field.proto\x1a(fintekkers/models/position/measure.proto\x1a*fintekkers/models/util/decimal_value.proto\"\x96\x01\n\x0fMeasureMapEntry\x12\x39\n\x07measure\x18\x01 \x01(\x0e\x32(.fintekkers.models.position.MeasureProto\x12H\n\x15measure_decimal_value\x18\x02 \x01(\x0b\x32).fintekkers.models.util.DecimalValueProto\"\x84\x02\n\rFieldMapEntry\x12\x35\n\x05\x66ield\x18\x01 \x01(\x0e\x32&.fintekkers.models.position.FieldProto\x12\x32\n\x12\x66ield_value_packed\x18\x04 \x01(\x0b\x32\x14.google.protobuf.AnyH\x00\x12\x14\n\nenum_value\x18\x05 \x01(\x05H\x00\x12\x16\n\x0cstring_value\x18\x06 \x01(\tH\x00\x12\x44\n\x08operator\x18\x14 \x01(\x0e\x32\x32.fintekkers.models.position.PositionFilterOperatorB\x14\n\x12\x46ieldMapValueOneOf*\x9a\x01\n\x16PositionFilterOperator\x12\x14\n\x10UNKNOWN_OPERATOR\x10\x00\x12\n\n\x06\x45QUALS\x10\x01\x12\x0e\n\nNOT_EQUALS\x10\x02\x12\r\n\tLESS_THAN\x10\x03\x12\x17\n\x13LESS_THAN_OR_EQUALS\x10\x04\x12\r\n\tMORE_THAN\x10\x05\x12\x17\n\x13MORE_THAN_OR_EQUALS\x10\x06\x42\x16\x42\x12PositionUtilProtosP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fintekkers.models.position.position_util_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'B\022PositionUtilProtosP\001'
  _POSITIONFILTEROPERATOR._serialized_start=648
  _POSITIONFILTEROPERATOR._serialized_end=802
  _MEASUREMAPENTRY._serialized_start=232
  _MEASUREMAPENTRY._serialized_end=382
  _FIELDMAPENTRY._serialized_start=385
  _FIELDMAPENTRY._serialized_end=645
# @@protoc_insertion_point(module_scope)
