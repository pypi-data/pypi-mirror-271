# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/base/v1beta1/coin.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from v4_proto.amino import amino_pb2 as amino_dot_amino__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x63osmos/base/v1beta1/coin.proto\x12\x13\x63osmos.base.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x11\x61mino/amino.proto\"]\n\x04\x43oin\x12\r\n\x05\x64\x65nom\x18\x01 \x01(\t\x12@\n\x06\x61mount\x18\x02 \x01(\tB0\xc8\xde\x1f\x00\xda\xde\x1f\x15\x63osmossdk.io/math.Int\xd2\xb4-\ncosmos.Int\xa8\xe7\xb0*\x01:\x04\xe8\xa0\x1f\x01\"a\n\x07\x44\x65\x63\x43oin\x12\r\n\x05\x64\x65nom\x18\x01 \x01(\t\x12\x41\n\x06\x61mount\x18\x02 \x01(\tB1\xc8\xde\x1f\x00\xda\xde\x1f\x1b\x63osmossdk.io/math.LegacyDec\xd2\xb4-\ncosmos.Dec:\x04\xe8\xa0\x1f\x01\"D\n\x08IntProto\x12\x38\n\x03int\x18\x01 \x01(\tB+\xc8\xde\x1f\x00\xda\xde\x1f\x15\x63osmossdk.io/math.Int\xd2\xb4-\ncosmos.Int\"J\n\x08\x44\x65\x63Proto\x12>\n\x03\x64\x65\x63\x18\x01 \x01(\tB1\xc8\xde\x1f\x00\xda\xde\x1f\x1b\x63osmossdk.io/math.LegacyDec\xd2\xb4-\ncosmos.DecB,Z\"github.com/cosmos/cosmos-sdk/types\xd8\xe1\x1e\x00\x80\xe2\x1e\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.base.v1beta1.coin_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\"github.com/cosmos/cosmos-sdk/types\330\341\036\000\200\342\036\000'
  _globals['_COIN'].fields_by_name['amount']._loaded_options = None
  _globals['_COIN'].fields_by_name['amount']._serialized_options = b'\310\336\037\000\332\336\037\025cosmossdk.io/math.Int\322\264-\ncosmos.Int\250\347\260*\001'
  _globals['_COIN']._loaded_options = None
  _globals['_COIN']._serialized_options = b'\350\240\037\001'
  _globals['_DECCOIN'].fields_by_name['amount']._loaded_options = None
  _globals['_DECCOIN'].fields_by_name['amount']._serialized_options = b'\310\336\037\000\332\336\037\033cosmossdk.io/math.LegacyDec\322\264-\ncosmos.Dec'
  _globals['_DECCOIN']._loaded_options = None
  _globals['_DECCOIN']._serialized_options = b'\350\240\037\001'
  _globals['_INTPROTO'].fields_by_name['int']._loaded_options = None
  _globals['_INTPROTO'].fields_by_name['int']._serialized_options = b'\310\336\037\000\332\336\037\025cosmossdk.io/math.Int\322\264-\ncosmos.Int'
  _globals['_DECPROTO'].fields_by_name['dec']._loaded_options = None
  _globals['_DECPROTO'].fields_by_name['dec']._serialized_options = b'\310\336\037\000\332\336\037\033cosmossdk.io/math.LegacyDec\322\264-\ncosmos.Dec'
  _globals['_COIN']._serialized_start=123
  _globals['_COIN']._serialized_end=216
  _globals['_DECCOIN']._serialized_start=218
  _globals['_DECCOIN']._serialized_end=315
  _globals['_INTPROTO']._serialized_start=317
  _globals['_INTPROTO']._serialized_end=385
  _globals['_DECPROTO']._serialized_start=387
  _globals['_DECPROTO']._serialized_end=461
# @@protoc_insertion_point(module_scope)
