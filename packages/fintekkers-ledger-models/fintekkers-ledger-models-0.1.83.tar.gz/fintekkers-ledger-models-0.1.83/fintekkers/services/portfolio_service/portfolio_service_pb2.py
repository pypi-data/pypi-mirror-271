# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fintekkers/services/portfolio-service/portfolio_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fintekkers.requests.portfolio import create_portfolio_request_pb2 as fintekkers_dot_requests_dot_portfolio_dot_create__portfolio__request__pb2
from fintekkers.requests.portfolio import create_portfolio_response_pb2 as fintekkers_dot_requests_dot_portfolio_dot_create__portfolio__response__pb2
from fintekkers.requests.portfolio import query_portfolio_request_pb2 as fintekkers_dot_requests_dot_portfolio_dot_query__portfolio__request__pb2
from fintekkers.requests.portfolio import query_portfolio_response_pb2 as fintekkers_dot_requests_dot_portfolio_dot_query__portfolio__response__pb2
from fintekkers.requests.util.errors import summary_pb2 as fintekkers_dot_requests_dot_util_dot_errors_dot_summary__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=fintekkers/services/portfolio-service/portfolio_service.proto\x12%fintekkers.services.portfolio_service\x1a<fintekkers/requests/portfolio/create_portfolio_request.proto\x1a=fintekkers/requests/portfolio/create_portfolio_response.proto\x1a;fintekkers/requests/portfolio/query_portfolio_request.proto\x1a<fintekkers/requests/portfolio/query_portfolio_response.proto\x1a-fintekkers/requests/util/errors/summary.proto2\xab\x06\n\tPortfolio\x12\x89\x01\n\x0e\x43reateOrUpdate\x12:.fintekkers.requests.portfolio.CreatePortfolioRequestProto\x1a;.fintekkers.requests.portfolio.CreatePortfolioResponseProto\x12\x81\x01\n\x08GetByIds\x12\x39.fintekkers.requests.portfolio.QueryPortfolioRequestProto\x1a:.fintekkers.requests.portfolio.QueryPortfolioResponseProto\x12\x81\x01\n\x06Search\x12\x39.fintekkers.requests.portfolio.QueryPortfolioRequestProto\x1a:.fintekkers.requests.portfolio.QueryPortfolioResponseProto0\x01\x12\x80\x01\n\x07ListIds\x12\x39.fintekkers.requests.portfolio.QueryPortfolioRequestProto\x1a:.fintekkers.requests.portfolio.QueryPortfolioResponseProto\x12\x83\x01\n\x16ValidateCreateOrUpdate\x12:.fintekkers.requests.portfolio.CreatePortfolioRequestProto\x1a-.fintekkers.requests.util.errors.SummaryProto\x12\x80\x01\n\x14ValidateQueryRequest\x12\x39.fintekkers.requests.portfolio.QueryPortfolioRequestProto\x1a-.fintekkers.requests.util.errors.SummaryProtoB\x06\x88\x01\x01\x90\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fintekkers.services.portfolio_service.portfolio_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\210\001\001\220\001\001'
  _PORTFOLIO._serialized_start=400
  _PORTFOLIO._serialized_end=1211
_builder.BuildServices(DESCRIPTOR, 'fintekkers.services.portfolio_service.portfolio_service_pb2', globals())
# @@protoc_insertion_point(module_scope)
