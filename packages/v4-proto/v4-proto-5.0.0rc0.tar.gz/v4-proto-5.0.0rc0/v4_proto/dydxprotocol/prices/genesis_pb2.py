# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/prices/genesis.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.dydxprotocol.prices import market_param_pb2 as dydxprotocol_dot_prices_dot_market__param__pb2
from v4_proto.dydxprotocol.prices import market_price_pb2 as dydxprotocol_dot_prices_dot_market__price__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!dydxprotocol/prices/genesis.proto\x12\x13\x64ydxprotocol.prices\x1a\x14gogoproto/gogo.proto\x1a&dydxprotocol/prices/market_param.proto\x1a&dydxprotocol/prices/market_price.proto\"\x8c\x01\n\x0cGenesisState\x12=\n\rmarket_params\x18\x01 \x03(\x0b\x32 .dydxprotocol.prices.MarketParamB\x04\xc8\xde\x1f\x00\x12=\n\rmarket_prices\x18\x02 \x03(\x0b\x32 .dydxprotocol.prices.MarketPriceB\x04\xc8\xde\x1f\x00\x42:Z8github.com/dydxprotocol/v4-chain/protocol/x/prices/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.prices.genesis_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z8github.com/dydxprotocol/v4-chain/protocol/x/prices/types'
  _globals['_GENESISSTATE'].fields_by_name['market_params']._loaded_options = None
  _globals['_GENESISSTATE'].fields_by_name['market_params']._serialized_options = b'\310\336\037\000'
  _globals['_GENESISSTATE'].fields_by_name['market_prices']._loaded_options = None
  _globals['_GENESISSTATE'].fields_by_name['market_prices']._serialized_options = b'\310\336\037\000'
  _globals['_GENESISSTATE']._serialized_start=161
  _globals['_GENESISSTATE']._serialized_end=301
# @@protoc_insertion_point(module_scope)
