# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/circuit/v1/types.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1d\x63osmos/circuit/v1/types.proto\x12\x11\x63osmos.circuit.v1\"\xc0\x01\n\x0bPermissions\x12\x33\n\x05level\x18\x01 \x01(\x0e\x32$.cosmos.circuit.v1.Permissions.Level\x12\x17\n\x0flimit_type_urls\x18\x02 \x03(\t\"c\n\x05Level\x12\x1a\n\x16LEVEL_NONE_UNSPECIFIED\x10\x00\x12\x13\n\x0fLEVEL_SOME_MSGS\x10\x01\x12\x12\n\x0eLEVEL_ALL_MSGS\x10\x02\x12\x15\n\x11LEVEL_SUPER_ADMIN\x10\x03\"a\n\x19GenesisAccountPermissions\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x33\n\x0bpermissions\x18\x02 \x01(\x0b\x32\x1e.cosmos.circuit.v1.Permissions\"u\n\x0cGenesisState\x12I\n\x13\x61\x63\x63ount_permissions\x18\x01 \x03(\x0b\x32,.cosmos.circuit.v1.GenesisAccountPermissions\x12\x1a\n\x12\x64isabled_type_urls\x18\x02 \x03(\tB\x1eZ\x1c\x63osmossdk.io/x/circuit/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.circuit.v1.types_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\034cosmossdk.io/x/circuit/types'
  _globals['_PERMISSIONS']._serialized_start=53
  _globals['_PERMISSIONS']._serialized_end=245
  _globals['_PERMISSIONS_LEVEL']._serialized_start=146
  _globals['_PERMISSIONS_LEVEL']._serialized_end=245
  _globals['_GENESISACCOUNTPERMISSIONS']._serialized_start=247
  _globals['_GENESISACCOUNTPERMISSIONS']._serialized_end=344
  _globals['_GENESISSTATE']._serialized_start=346
  _globals['_GENESISSTATE']._serialized_end=463
# @@protoc_insertion_point(module_scope)
