# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fintekkers/requests/transaction/query_transaction_response.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fintekkers.models.transaction import transaction_pb2 as fintekkers_dot_models_dot_transaction_dot_transaction__pb2
from fintekkers.requests.transaction import query_transaction_request_pb2 as fintekkers_dot_requests_dot_transaction_dot_query__transaction__request__pb2
from fintekkers.requests.util.errors import summary_pb2 as fintekkers_dot_requests_dot_util_dot_errors_dot_summary__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n@fintekkers/requests/transaction/query_transaction_response.proto\x12\x1f\x66intekkers.requests.transaction\x1a/fintekkers/models/transaction/transaction.proto\x1a?fintekkers/requests/transaction/query_transaction_request.proto\x1a-fintekkers/requests/util/errors/summary.proto\"\xc3\x02\n\x1dQueryTransactionResponseProto\x12\x14\n\x0cobject_class\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t\x12\x61\n\x1a\x63reate_transaction_request\x18\x14 \x01(\x0b\x32=.fintekkers.requests.transaction.QueryTransactionRequestProto\x12M\n\x14transaction_response\x18\x1e \x03(\x0b\x32/.fintekkers.models.transaction.TransactionProto\x12I\n\x12\x65rrors_or_warnings\x18( \x01(\x0b\x32-.fintekkers.requests.util.errors.SummaryProtoB\"B\x1eQueryTransactionResponseProtosP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fintekkers.requests.transaction.query_transaction_response_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'B\036QueryTransactionResponseProtosP\001'
  _QUERYTRANSACTIONRESPONSEPROTO._serialized_start=263
  _QUERYTRANSACTIONRESPONSEPROTO._serialized_end=586
# @@protoc_insertion_point(module_scope)
