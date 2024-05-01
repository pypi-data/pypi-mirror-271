# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/subaccounts/subaccount.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from v4_proto.dydxprotocol.subaccounts import asset_position_pb2 as dydxprotocol_dot_subaccounts_dot_asset__position__pb2
from v4_proto.dydxprotocol.subaccounts import perpetual_position_pb2 as dydxprotocol_dot_subaccounts_dot_perpetual__position__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)dydxprotocol/subaccounts/subaccount.proto\x12\x18\x64ydxprotocol.subaccounts\x1a\x19\x63osmos_proto/cosmos.proto\x1a-dydxprotocol/subaccounts/asset_position.proto\x1a\x31\x64ydxprotocol/subaccounts/perpetual_position.proto\"G\n\x0cSubaccountId\x12\'\n\x05owner\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12\x0e\n\x06number\x18\x02 \x01(\r\"\xe4\x01\n\nSubaccount\x12\x32\n\x02id\x18\x01 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountId\x12@\n\x0f\x61sset_positions\x18\x02 \x03(\x0b\x32\'.dydxprotocol.subaccounts.AssetPosition\x12H\n\x13perpetual_positions\x18\x03 \x03(\x0b\x32+.dydxprotocol.subaccounts.PerpetualPosition\x12\x16\n\x0emargin_enabled\x18\x04 \x01(\x08\x42?Z=github.com/dydxprotocol/v4-chain/protocol/x/subaccounts/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.subaccounts.subaccount_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z=github.com/dydxprotocol/v4-chain/protocol/x/subaccounts/types'
  _globals['_SUBACCOUNTID'].fields_by_name['owner']._loaded_options = None
  _globals['_SUBACCOUNTID'].fields_by_name['owner']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_SUBACCOUNTID']._serialized_start=196
  _globals['_SUBACCOUNTID']._serialized_end=267
  _globals['_SUBACCOUNT']._serialized_start=270
  _globals['_SUBACCOUNT']._serialized_end=498
# @@protoc_insertion_point(module_scope)
