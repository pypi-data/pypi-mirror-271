# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/vault/tx.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from v4_proto.cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from v4_proto.dydxprotocol.subaccounts import subaccount_pb2 as dydxprotocol_dot_subaccounts_dot_subaccount__pb2
from v4_proto.dydxprotocol.vault import params_pb2 as dydxprotocol_dot_vault_dot_params__pb2
from v4_proto.dydxprotocol.vault import vault_pb2 as dydxprotocol_dot_vault_dot_vault__pb2
from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1b\x64ydxprotocol/vault/tx.proto\x12\x12\x64ydxprotocol.vault\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x17\x63osmos/msg/v1/msg.proto\x1a)dydxprotocol/subaccounts/subaccount.proto\x1a\x1f\x64ydxprotocol/vault/params.proto\x1a\x1e\x64ydxprotocol/vault/vault.proto\x1a\x14gogoproto/gogo.proto\"\xf7\x01\n\x11MsgDepositToVault\x12-\n\x08vault_id\x18\x01 \x01(\x0b\x32\x1b.dydxprotocol.vault.VaultId\x12=\n\rsubaccount_id\x18\x02 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountId\x12`\n\x0equote_quantums\x18\x03 \x01(\x0c\x42H\xc8\xde\x1f\x00\xda\xde\x1f@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt:\x12\x82\xe7\xb0*\rsubaccount_id\"\x1b\n\x19MsgDepositToVaultResponse\"\x80\x01\n\x0fMsgUpdateParams\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12\x30\n\x06params\x18\x02 \x01(\x0b\x32\x1a.dydxprotocol.vault.ParamsB\x04\xc8\xde\x1f\x00:\x0e\x82\xe7\xb0*\tauthority\"\x19\n\x17MsgUpdateParamsResponse2\xcf\x01\n\x03Msg\x12\x66\n\x0e\x44\x65positToVault\x12%.dydxprotocol.vault.MsgDepositToVault\x1a-.dydxprotocol.vault.MsgDepositToVaultResponse\x12`\n\x0cUpdateParams\x12#.dydxprotocol.vault.MsgUpdateParams\x1a+.dydxprotocol.vault.MsgUpdateParamsResponseB9Z7github.com/dydxprotocol/v4-chain/protocol/x/vault/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.vault.tx_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z7github.com/dydxprotocol/v4-chain/protocol/x/vault/types'
  _globals['_MSGDEPOSITTOVAULT'].fields_by_name['quote_quantums']._loaded_options = None
  _globals['_MSGDEPOSITTOVAULT'].fields_by_name['quote_quantums']._serialized_options = b'\310\336\037\000\332\336\037@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt'
  _globals['_MSGDEPOSITTOVAULT']._loaded_options = None
  _globals['_MSGDEPOSITTOVAULT']._serialized_options = b'\202\347\260*\rsubaccount_id'
  _globals['_MSGUPDATEPARAMS'].fields_by_name['authority']._loaded_options = None
  _globals['_MSGUPDATEPARAMS'].fields_by_name['authority']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_MSGUPDATEPARAMS'].fields_by_name['params']._loaded_options = None
  _globals['_MSGUPDATEPARAMS'].fields_by_name['params']._serialized_options = b'\310\336\037\000'
  _globals['_MSGUPDATEPARAMS']._loaded_options = None
  _globals['_MSGUPDATEPARAMS']._serialized_options = b'\202\347\260*\tauthority'
  _globals['_MSGDEPOSITTOVAULT']._serialized_start=234
  _globals['_MSGDEPOSITTOVAULT']._serialized_end=481
  _globals['_MSGDEPOSITTOVAULTRESPONSE']._serialized_start=483
  _globals['_MSGDEPOSITTOVAULTRESPONSE']._serialized_end=510
  _globals['_MSGUPDATEPARAMS']._serialized_start=513
  _globals['_MSGUPDATEPARAMS']._serialized_end=641
  _globals['_MSGUPDATEPARAMSRESPONSE']._serialized_start=643
  _globals['_MSGUPDATEPARAMSRESPONSE']._serialized_end=668
  _globals['_MSG']._serialized_start=671
  _globals['_MSG']._serialized_end=878
# @@protoc_insertion_point(module_scope)
