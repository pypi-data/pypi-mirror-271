# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/perpetuals/genesis.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.dydxprotocol.perpetuals import perpetual_pb2 as dydxprotocol_dot_perpetuals_dot_perpetual__pb2
from v4_proto.dydxprotocol.perpetuals import params_pb2 as dydxprotocol_dot_perpetuals_dot_params__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%dydxprotocol/perpetuals/genesis.proto\x12\x17\x64ydxprotocol.perpetuals\x1a\x14gogoproto/gogo.proto\x1a\'dydxprotocol/perpetuals/perpetual.proto\x1a$dydxprotocol/perpetuals/params.proto\"\xca\x01\n\x0cGenesisState\x12<\n\nperpetuals\x18\x01 \x03(\x0b\x32\".dydxprotocol.perpetuals.PerpetualB\x04\xc8\xde\x1f\x00\x12\x45\n\x0fliquidity_tiers\x18\x02 \x03(\x0b\x32&.dydxprotocol.perpetuals.LiquidityTierB\x04\xc8\xde\x1f\x00\x12\x35\n\x06params\x18\x03 \x01(\x0b\x32\x1f.dydxprotocol.perpetuals.ParamsB\x04\xc8\xde\x1f\x00\x42>Z<github.com/dydxprotocol/v4-chain/protocol/x/perpetuals/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.perpetuals.genesis_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z<github.com/dydxprotocol/v4-chain/protocol/x/perpetuals/types'
  _globals['_GENESISSTATE'].fields_by_name['perpetuals']._loaded_options = None
  _globals['_GENESISSTATE'].fields_by_name['perpetuals']._serialized_options = b'\310\336\037\000'
  _globals['_GENESISSTATE'].fields_by_name['liquidity_tiers']._loaded_options = None
  _globals['_GENESISSTATE'].fields_by_name['liquidity_tiers']._serialized_options = b'\310\336\037\000'
  _globals['_GENESISSTATE'].fields_by_name['params']._loaded_options = None
  _globals['_GENESISSTATE'].fields_by_name['params']._serialized_options = b'\310\336\037\000'
  _globals['_GENESISSTATE']._serialized_start=168
  _globals['_GENESISSTATE']._serialized_end=370
# @@protoc_insertion_point(module_scope)
