# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/auth/v1beta1/auth.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.amino import amino_pb2 as amino_dot_amino__pb2
from v4_proto.cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x63osmos/auth/v1beta1/auth.proto\x12\x13\x63osmos.auth.v1beta1\x1a\x11\x61mino/amino.proto\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x14gogoproto/gogo.proto\x1a\x19google/protobuf/any.proto\"\xf7\x01\n\x0b\x42\x61seAccount\x12)\n\x07\x61\x64\x64ress\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12N\n\x07pub_key\x18\x02 \x01(\x0b\x32\x14.google.protobuf.AnyB\'\xea\xde\x1f\x14public_key,omitempty\xa2\xe7\xb0*\npublic_key\x12\x16\n\x0e\x61\x63\x63ount_number\x18\x03 \x01(\x04\x12\x10\n\x08sequence\x18\x04 \x01(\x04:C\x88\xa0\x1f\x00\xe8\xa0\x1f\x00\xca\xb4-\x1c\x63osmos.auth.v1beta1.AccountI\x8a\xe7\xb0*\x16\x63osmos-sdk/BaseAccount\"\xcc\x01\n\rModuleAccount\x12<\n\x0c\x62\x61se_account\x18\x01 \x01(\x0b\x32 .cosmos.auth.v1beta1.BaseAccountB\x04\xd0\xde\x1f\x01\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0bpermissions\x18\x03 \x03(\t:Z\x88\xa0\x1f\x00\xca\xb4-\"cosmos.auth.v1beta1.ModuleAccountI\x8a\xe7\xb0*\x18\x63osmos-sdk/ModuleAccount\x92\xe7\xb0*\x0emodule_account\"h\n\x10ModuleCredential\x12\x13\n\x0bmodule_name\x18\x01 \x01(\t\x12\x17\n\x0f\x64\x65rivation_keys\x18\x02 \x03(\x0c:&\x8a\xe7\xb0*!cosmos-sdk/GroupAccountCredential\"\xf7\x01\n\x06Params\x12\x1b\n\x13max_memo_characters\x18\x01 \x01(\x04\x12\x14\n\x0ctx_sig_limit\x18\x02 \x01(\x04\x12\x1d\n\x15tx_size_cost_per_byte\x18\x03 \x01(\x04\x12\x39\n\x17sig_verify_cost_ed25519\x18\x04 \x01(\x04\x42\x18\xe2\xde\x1f\x14SigVerifyCostED25519\x12=\n\x19sig_verify_cost_secp256k1\x18\x05 \x01(\x04\x42\x1a\xe2\xde\x1f\x16SigVerifyCostSecp256k1:!\xe8\xa0\x1f\x01\x8a\xe7\xb0*\x18\x63osmos-sdk/x/auth/ParamsB+Z)github.com/cosmos/cosmos-sdk/x/auth/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.auth.v1beta1.auth_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z)github.com/cosmos/cosmos-sdk/x/auth/types'
  _globals['_BASEACCOUNT'].fields_by_name['address']._loaded_options = None
  _globals['_BASEACCOUNT'].fields_by_name['address']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_BASEACCOUNT'].fields_by_name['pub_key']._loaded_options = None
  _globals['_BASEACCOUNT'].fields_by_name['pub_key']._serialized_options = b'\352\336\037\024public_key,omitempty\242\347\260*\npublic_key'
  _globals['_BASEACCOUNT']._loaded_options = None
  _globals['_BASEACCOUNT']._serialized_options = b'\210\240\037\000\350\240\037\000\312\264-\034cosmos.auth.v1beta1.AccountI\212\347\260*\026cosmos-sdk/BaseAccount'
  _globals['_MODULEACCOUNT'].fields_by_name['base_account']._loaded_options = None
  _globals['_MODULEACCOUNT'].fields_by_name['base_account']._serialized_options = b'\320\336\037\001'
  _globals['_MODULEACCOUNT']._loaded_options = None
  _globals['_MODULEACCOUNT']._serialized_options = b'\210\240\037\000\312\264-\"cosmos.auth.v1beta1.ModuleAccountI\212\347\260*\030cosmos-sdk/ModuleAccount\222\347\260*\016module_account'
  _globals['_MODULECREDENTIAL']._loaded_options = None
  _globals['_MODULECREDENTIAL']._serialized_options = b'\212\347\260*!cosmos-sdk/GroupAccountCredential'
  _globals['_PARAMS'].fields_by_name['sig_verify_cost_ed25519']._loaded_options = None
  _globals['_PARAMS'].fields_by_name['sig_verify_cost_ed25519']._serialized_options = b'\342\336\037\024SigVerifyCostED25519'
  _globals['_PARAMS'].fields_by_name['sig_verify_cost_secp256k1']._loaded_options = None
  _globals['_PARAMS'].fields_by_name['sig_verify_cost_secp256k1']._serialized_options = b'\342\336\037\026SigVerifyCostSecp256k1'
  _globals['_PARAMS']._loaded_options = None
  _globals['_PARAMS']._serialized_options = b'\350\240\037\001\212\347\260*\030cosmos-sdk/x/auth/Params'
  _globals['_BASEACCOUNT']._serialized_start=151
  _globals['_BASEACCOUNT']._serialized_end=398
  _globals['_MODULEACCOUNT']._serialized_start=401
  _globals['_MODULEACCOUNT']._serialized_end=605
  _globals['_MODULECREDENTIAL']._serialized_start=607
  _globals['_MODULECREDENTIAL']._serialized_end=711
  _globals['_PARAMS']._serialized_start=714
  _globals['_PARAMS']._serialized_end=961
# @@protoc_insertion_point(module_scope)
