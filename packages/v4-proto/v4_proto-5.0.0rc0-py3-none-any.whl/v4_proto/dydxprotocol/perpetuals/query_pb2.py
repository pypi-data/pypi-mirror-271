# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/perpetuals/query.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from v4_proto.cosmos.base.query.v1beta1 import pagination_pb2 as cosmos_dot_base_dot_query_dot_v1beta1_dot_pagination__pb2
from v4_proto.dydxprotocol.perpetuals import params_pb2 as dydxprotocol_dot_perpetuals_dot_params__pb2
from v4_proto.dydxprotocol.perpetuals import perpetual_pb2 as dydxprotocol_dot_perpetuals_dot_perpetual__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#dydxprotocol/perpetuals/query.proto\x12\x17\x64ydxprotocol.perpetuals\x1a\x14gogoproto/gogo.proto\x1a\x1cgoogle/api/annotations.proto\x1a*cosmos/base/query/v1beta1/pagination.proto\x1a$dydxprotocol/perpetuals/params.proto\x1a\'dydxprotocol/perpetuals/perpetual.proto\"#\n\x15QueryPerpetualRequest\x12\n\n\x02id\x18\x01 \x01(\r\"U\n\x16QueryPerpetualResponse\x12;\n\tperpetual\x18\x01 \x01(\x0b\x32\".dydxprotocol.perpetuals.PerpetualB\x04\xc8\xde\x1f\x00\"W\n\x19QueryAllPerpetualsRequest\x12:\n\npagination\x18\x01 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequest\"\x96\x01\n\x1aQueryAllPerpetualsResponse\x12;\n\tperpetual\x18\x01 \x03(\x0b\x32\".dydxprotocol.perpetuals.PerpetualB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponse\"[\n\x1dQueryAllLiquidityTiersRequest\x12:\n\npagination\x18\x01 \x01(\x0b\x32&.cosmos.base.query.v1beta1.PageRequest\"\xa4\x01\n\x1eQueryAllLiquidityTiersResponse\x12\x45\n\x0fliquidity_tiers\x18\x01 \x03(\x0b\x32&.dydxprotocol.perpetuals.LiquidityTierB\x04\xc8\xde\x1f\x00\x12;\n\npagination\x18\x02 \x01(\x0b\x32\'.cosmos.base.query.v1beta1.PageResponse\"\x1a\n\x18QueryPremiumVotesRequest\"_\n\x19QueryPremiumVotesResponse\x12\x42\n\rpremium_votes\x18\x01 \x01(\x0b\x32%.dydxprotocol.perpetuals.PremiumStoreB\x04\xc8\xde\x1f\x00\"\x1c\n\x1aQueryPremiumSamplesRequest\"c\n\x1bQueryPremiumSamplesResponse\x12\x44\n\x0fpremium_samples\x18\x01 \x01(\x0b\x32%.dydxprotocol.perpetuals.PremiumStoreB\x04\xc8\xde\x1f\x00\"\x14\n\x12QueryParamsRequest\"L\n\x13QueryParamsResponse\x12\x35\n\x06params\x18\x01 \x01(\x0b\x32\x1f.dydxprotocol.perpetuals.ParamsB\x04\xc8\xde\x1f\x00\x32\xee\x07\n\x05Query\x12\x9d\x01\n\tPerpetual\x12..dydxprotocol.perpetuals.QueryPerpetualRequest\x1a/.dydxprotocol.perpetuals.QueryPerpetualResponse\"/\x82\xd3\xe4\x93\x02)\x12\'/dydxprotocol/perpetuals/perpetual/{id}\x12\xa4\x01\n\rAllPerpetuals\x12\x32.dydxprotocol.perpetuals.QueryAllPerpetualsRequest\x1a\x33.dydxprotocol.perpetuals.QueryAllPerpetualsResponse\"*\x82\xd3\xe4\x93\x02$\x12\"/dydxprotocol/perpetuals/perpetual\x12\xb6\x01\n\x11\x41llLiquidityTiers\x12\x36.dydxprotocol.perpetuals.QueryAllLiquidityTiersRequest\x1a\x37.dydxprotocol.perpetuals.QueryAllLiquidityTiersResponse\"0\x82\xd3\xe4\x93\x02*\x12(/dydxprotocol/perpetuals/liquidity_tiers\x12\xa5\x01\n\x0cPremiumVotes\x12\x31.dydxprotocol.perpetuals.QueryPremiumVotesRequest\x1a\x32.dydxprotocol.perpetuals.QueryPremiumVotesResponse\".\x82\xd3\xe4\x93\x02(\x12&/dydxprotocol/perpetuals/premium_votes\x12\xad\x01\n\x0ePremiumSamples\x12\x33.dydxprotocol.perpetuals.QueryPremiumSamplesRequest\x1a\x34.dydxprotocol.perpetuals.QueryPremiumSamplesResponse\"0\x82\xd3\xe4\x93\x02*\x12(/dydxprotocol/perpetuals/premium_samples\x12\x8c\x01\n\x06Params\x12+.dydxprotocol.perpetuals.QueryParamsRequest\x1a,.dydxprotocol.perpetuals.QueryParamsResponse\"\'\x82\xd3\xe4\x93\x02!\x12\x1f/dydxprotocol/perpetuals/paramsB>Z<github.com/dydxprotocol/v4-chain/protocol/x/perpetuals/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.perpetuals.query_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z<github.com/dydxprotocol/v4-chain/protocol/x/perpetuals/types'
  _globals['_QUERYPERPETUALRESPONSE'].fields_by_name['perpetual']._loaded_options = None
  _globals['_QUERYPERPETUALRESPONSE'].fields_by_name['perpetual']._serialized_options = b'\310\336\037\000'
  _globals['_QUERYALLPERPETUALSRESPONSE'].fields_by_name['perpetual']._loaded_options = None
  _globals['_QUERYALLPERPETUALSRESPONSE'].fields_by_name['perpetual']._serialized_options = b'\310\336\037\000'
  _globals['_QUERYALLLIQUIDITYTIERSRESPONSE'].fields_by_name['liquidity_tiers']._loaded_options = None
  _globals['_QUERYALLLIQUIDITYTIERSRESPONSE'].fields_by_name['liquidity_tiers']._serialized_options = b'\310\336\037\000'
  _globals['_QUERYPREMIUMVOTESRESPONSE'].fields_by_name['premium_votes']._loaded_options = None
  _globals['_QUERYPREMIUMVOTESRESPONSE'].fields_by_name['premium_votes']._serialized_options = b'\310\336\037\000'
  _globals['_QUERYPREMIUMSAMPLESRESPONSE'].fields_by_name['premium_samples']._loaded_options = None
  _globals['_QUERYPREMIUMSAMPLESRESPONSE'].fields_by_name['premium_samples']._serialized_options = b'\310\336\037\000'
  _globals['_QUERYPARAMSRESPONSE'].fields_by_name['params']._loaded_options = None
  _globals['_QUERYPARAMSRESPONSE'].fields_by_name['params']._serialized_options = b'\310\336\037\000'
  _globals['_QUERY'].methods_by_name['Perpetual']._loaded_options = None
  _globals['_QUERY'].methods_by_name['Perpetual']._serialized_options = b'\202\323\344\223\002)\022\'/dydxprotocol/perpetuals/perpetual/{id}'
  _globals['_QUERY'].methods_by_name['AllPerpetuals']._loaded_options = None
  _globals['_QUERY'].methods_by_name['AllPerpetuals']._serialized_options = b'\202\323\344\223\002$\022\"/dydxprotocol/perpetuals/perpetual'
  _globals['_QUERY'].methods_by_name['AllLiquidityTiers']._loaded_options = None
  _globals['_QUERY'].methods_by_name['AllLiquidityTiers']._serialized_options = b'\202\323\344\223\002*\022(/dydxprotocol/perpetuals/liquidity_tiers'
  _globals['_QUERY'].methods_by_name['PremiumVotes']._loaded_options = None
  _globals['_QUERY'].methods_by_name['PremiumVotes']._serialized_options = b'\202\323\344\223\002(\022&/dydxprotocol/perpetuals/premium_votes'
  _globals['_QUERY'].methods_by_name['PremiumSamples']._loaded_options = None
  _globals['_QUERY'].methods_by_name['PremiumSamples']._serialized_options = b'\202\323\344\223\002*\022(/dydxprotocol/perpetuals/premium_samples'
  _globals['_QUERY'].methods_by_name['Params']._loaded_options = None
  _globals['_QUERY'].methods_by_name['Params']._serialized_options = b'\202\323\344\223\002!\022\037/dydxprotocol/perpetuals/params'
  _globals['_QUERYPERPETUALREQUEST']._serialized_start=239
  _globals['_QUERYPERPETUALREQUEST']._serialized_end=274
  _globals['_QUERYPERPETUALRESPONSE']._serialized_start=276
  _globals['_QUERYPERPETUALRESPONSE']._serialized_end=361
  _globals['_QUERYALLPERPETUALSREQUEST']._serialized_start=363
  _globals['_QUERYALLPERPETUALSREQUEST']._serialized_end=450
  _globals['_QUERYALLPERPETUALSRESPONSE']._serialized_start=453
  _globals['_QUERYALLPERPETUALSRESPONSE']._serialized_end=603
  _globals['_QUERYALLLIQUIDITYTIERSREQUEST']._serialized_start=605
  _globals['_QUERYALLLIQUIDITYTIERSREQUEST']._serialized_end=696
  _globals['_QUERYALLLIQUIDITYTIERSRESPONSE']._serialized_start=699
  _globals['_QUERYALLLIQUIDITYTIERSRESPONSE']._serialized_end=863
  _globals['_QUERYPREMIUMVOTESREQUEST']._serialized_start=865
  _globals['_QUERYPREMIUMVOTESREQUEST']._serialized_end=891
  _globals['_QUERYPREMIUMVOTESRESPONSE']._serialized_start=893
  _globals['_QUERYPREMIUMVOTESRESPONSE']._serialized_end=988
  _globals['_QUERYPREMIUMSAMPLESREQUEST']._serialized_start=990
  _globals['_QUERYPREMIUMSAMPLESREQUEST']._serialized_end=1018
  _globals['_QUERYPREMIUMSAMPLESRESPONSE']._serialized_start=1020
  _globals['_QUERYPREMIUMSAMPLESRESPONSE']._serialized_end=1119
  _globals['_QUERYPARAMSREQUEST']._serialized_start=1121
  _globals['_QUERYPARAMSREQUEST']._serialized_end=1141
  _globals['_QUERYPARAMSRESPONSE']._serialized_start=1143
  _globals['_QUERYPARAMSRESPONSE']._serialized_end=1219
  _globals['_QUERY']._serialized_start=1222
  _globals['_QUERY']._serialized_end=2228
# @@protoc_insertion_point(module_scope)
