# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/vest/genesis.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.dydxprotocol.vest import vest_entry_pb2 as dydxprotocol_dot_vest_dot_vest__entry__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x64ydxprotocol/vest/genesis.proto\x12\x11\x64ydxprotocol.vest\x1a\x14gogoproto/gogo.proto\x1a\"dydxprotocol/vest/vest_entry.proto\"H\n\x0cGenesisState\x12\x38\n\x0cvest_entries\x18\x01 \x03(\x0b\x32\x1c.dydxprotocol.vest.VestEntryB\x04\xc8\xde\x1f\x00\x42\x38Z6github.com/dydxprotocol/v4-chain/protocol/x/vest/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.vest.genesis_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z6github.com/dydxprotocol/v4-chain/protocol/x/vest/types'
  _globals['_GENESISSTATE'].fields_by_name['vest_entries']._loaded_options = None
  _globals['_GENESISSTATE'].fields_by_name['vest_entries']._serialized_options = b'\310\336\037\000'
  _globals['_GENESISSTATE']._serialized_start=112
  _globals['_GENESISSTATE']._serialized_end=184
# @@protoc_insertion_point(module_scope)
