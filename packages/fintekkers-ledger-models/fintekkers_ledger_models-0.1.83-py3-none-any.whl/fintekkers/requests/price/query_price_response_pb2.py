# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fintekkers/requests/price/query_price_response.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fintekkers.models.price import price_pb2 as fintekkers_dot_models_dot_price_dot_price__pb2
from fintekkers.requests.price import query_price_request_pb2 as fintekkers_dot_requests_dot_price_dot_query__price__request__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4fintekkers/requests/price/query_price_response.proto\x12\x19\x66intekkers.requests.price\x1a#fintekkers/models/price/price.proto\x1a\x33\x66intekkers/requests/price/query_price_request.proto\"\xcd\x01\n\x17QueryPriceResponseProto\x12\x14\n\x0cobject_class\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12N\n\x13query_price_request\x18\x14 \x01(\x0b\x32\x31.fintekkers.requests.price.QueryPriceRequestProto\x12;\n\x0eprice_response\x18\x1e \x03(\x0b\x32#.fintekkers.models.price.PriceProtoB\x1c\x42\x18QueryPriceResponseProtosP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fintekkers.requests.price.query_price_response_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'B\030QueryPriceResponseProtosP\001'
  _QUERYPRICERESPONSEPROTO._serialized_start=174
  _QUERYPRICERESPONSEPROTO._serialized_end=379
# @@protoc_insertion_point(module_scope)
