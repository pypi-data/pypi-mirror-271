# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/feegrant/v1beta1/feegrant.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from v4_proto.cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from v4_proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from v4_proto.amino import amino_pb2 as amino_dot_amino__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&cosmos/feegrant/v1beta1/feegrant.proto\x12\x17\x63osmos.feegrant.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19google/protobuf/any.proto\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x11\x61mino/amino.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/duration.proto\"\x87\x02\n\x0e\x42\x61sicAllowance\x12v\n\x0bspend_limit\x18\x01 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinBF\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x9a\xe7\xb0*\x0clegacy_coins\xa8\xe7\xb0*\x01\x12\x34\n\nexpiration\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\x90\xdf\x1f\x01:G\xca\xb4-%cosmos.feegrant.v1beta1.FeeAllowanceI\x8a\xe7\xb0*\x19\x63osmos-sdk/BasicAllowance\"\x99\x04\n\x11PeriodicAllowance\x12\x41\n\x05\x62\x61sic\x18\x01 \x01(\x0b\x32\'.cosmos.feegrant.v1beta1.BasicAllowanceB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12\x38\n\x06period\x18\x02 \x01(\x0b\x32\x19.google.protobuf.DurationB\r\xc8\xde\x1f\x00\x98\xdf\x1f\x01\xa8\xe7\xb0*\x01\x12}\n\x12period_spend_limit\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinBF\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x9a\xe7\xb0*\x0clegacy_coins\xa8\xe7\xb0*\x01\x12{\n\x10period_can_spend\x18\x04 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinBF\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x9a\xe7\xb0*\x0clegacy_coins\xa8\xe7\xb0*\x01\x12?\n\x0cperiod_reset\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\r\xc8\xde\x1f\x00\x90\xdf\x1f\x01\xa8\xe7\xb0*\x01:J\xca\xb4-%cosmos.feegrant.v1beta1.FeeAllowanceI\x8a\xe7\xb0*\x1c\x63osmos-sdk/PeriodicAllowance\"\xd5\x01\n\x13\x41llowedMsgAllowance\x12R\n\tallowance\x18\x01 \x01(\x0b\x32\x14.google.protobuf.AnyB)\xca\xb4-%cosmos.feegrant.v1beta1.FeeAllowanceI\x12\x18\n\x10\x61llowed_messages\x18\x02 \x03(\t:P\x88\xa0\x1f\x00\xca\xb4-%cosmos.feegrant.v1beta1.FeeAllowanceI\x8a\xe7\xb0*\x1e\x63osmos-sdk/AllowedMsgAllowance\"\xb1\x01\n\x05Grant\x12)\n\x07granter\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12)\n\x07grantee\x18\x02 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12R\n\tallowance\x18\x03 \x01(\x0b\x32\x14.google.protobuf.AnyB)\xca\xb4-%cosmos.feegrant.v1beta1.FeeAllowanceIB\x19Z\x17\x63osmossdk.io/x/feegrantb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.feegrant.v1beta1.feegrant_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\027cosmossdk.io/x/feegrant'
  _globals['_BASICALLOWANCE'].fields_by_name['spend_limit']._loaded_options = None
  _globals['_BASICALLOWANCE'].fields_by_name['spend_limit']._serialized_options = b'\310\336\037\000\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins\232\347\260*\014legacy_coins\250\347\260*\001'
  _globals['_BASICALLOWANCE'].fields_by_name['expiration']._loaded_options = None
  _globals['_BASICALLOWANCE'].fields_by_name['expiration']._serialized_options = b'\220\337\037\001'
  _globals['_BASICALLOWANCE']._loaded_options = None
  _globals['_BASICALLOWANCE']._serialized_options = b'\312\264-%cosmos.feegrant.v1beta1.FeeAllowanceI\212\347\260*\031cosmos-sdk/BasicAllowance'
  _globals['_PERIODICALLOWANCE'].fields_by_name['basic']._loaded_options = None
  _globals['_PERIODICALLOWANCE'].fields_by_name['basic']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _globals['_PERIODICALLOWANCE'].fields_by_name['period']._loaded_options = None
  _globals['_PERIODICALLOWANCE'].fields_by_name['period']._serialized_options = b'\310\336\037\000\230\337\037\001\250\347\260*\001'
  _globals['_PERIODICALLOWANCE'].fields_by_name['period_spend_limit']._loaded_options = None
  _globals['_PERIODICALLOWANCE'].fields_by_name['period_spend_limit']._serialized_options = b'\310\336\037\000\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins\232\347\260*\014legacy_coins\250\347\260*\001'
  _globals['_PERIODICALLOWANCE'].fields_by_name['period_can_spend']._loaded_options = None
  _globals['_PERIODICALLOWANCE'].fields_by_name['period_can_spend']._serialized_options = b'\310\336\037\000\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins\232\347\260*\014legacy_coins\250\347\260*\001'
  _globals['_PERIODICALLOWANCE'].fields_by_name['period_reset']._loaded_options = None
  _globals['_PERIODICALLOWANCE'].fields_by_name['period_reset']._serialized_options = b'\310\336\037\000\220\337\037\001\250\347\260*\001'
  _globals['_PERIODICALLOWANCE']._loaded_options = None
  _globals['_PERIODICALLOWANCE']._serialized_options = b'\312\264-%cosmos.feegrant.v1beta1.FeeAllowanceI\212\347\260*\034cosmos-sdk/PeriodicAllowance'
  _globals['_ALLOWEDMSGALLOWANCE'].fields_by_name['allowance']._loaded_options = None
  _globals['_ALLOWEDMSGALLOWANCE'].fields_by_name['allowance']._serialized_options = b'\312\264-%cosmos.feegrant.v1beta1.FeeAllowanceI'
  _globals['_ALLOWEDMSGALLOWANCE']._loaded_options = None
  _globals['_ALLOWEDMSGALLOWANCE']._serialized_options = b'\210\240\037\000\312\264-%cosmos.feegrant.v1beta1.FeeAllowanceI\212\347\260*\036cosmos-sdk/AllowedMsgAllowance'
  _globals['_GRANT'].fields_by_name['granter']._loaded_options = None
  _globals['_GRANT'].fields_by_name['granter']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_GRANT'].fields_by_name['grantee']._loaded_options = None
  _globals['_GRANT'].fields_by_name['grantee']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_GRANT'].fields_by_name['allowance']._loaded_options = None
  _globals['_GRANT'].fields_by_name['allowance']._serialized_options = b'\312\264-%cosmos.feegrant.v1beta1.FeeAllowanceI'
  _globals['_BASICALLOWANCE']._serialized_start=260
  _globals['_BASICALLOWANCE']._serialized_end=523
  _globals['_PERIODICALLOWANCE']._serialized_start=526
  _globals['_PERIODICALLOWANCE']._serialized_end=1063
  _globals['_ALLOWEDMSGALLOWANCE']._serialized_start=1066
  _globals['_ALLOWEDMSGALLOWANCE']._serialized_end=1279
  _globals['_GRANT']._serialized_start=1282
  _globals['_GRANT']._serialized_end=1459
# @@protoc_insertion_point(module_scope)
