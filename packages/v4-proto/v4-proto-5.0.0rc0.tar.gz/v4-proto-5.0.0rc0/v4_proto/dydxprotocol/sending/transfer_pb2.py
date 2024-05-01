# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/sending/transfer.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from v4_proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from v4_proto.cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.dydxprotocol.subaccounts import subaccount_pb2 as dydxprotocol_dot_subaccounts_dot_subaccount__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#dydxprotocol/sending/transfer.proto\x12\x14\x64ydxprotocol.sending\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x17\x63osmos/msg/v1/msg.proto\x1a\x14gogoproto/gogo.proto\x1a)dydxprotocol/subaccounts/subaccount.proto\"\xab\x01\n\x08Transfer\x12<\n\x06sender\x18\x01 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountIdB\x04\xc8\xde\x1f\x00\x12?\n\trecipient\x18\x02 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountIdB\x04\xc8\xde\x1f\x00\x12\x10\n\x08\x61sset_id\x18\x03 \x01(\r\x12\x0e\n\x06\x61mount\x18\x04 \x01(\x04\"\xb4\x01\n\x16MsgDepositToSubaccount\x12(\n\x06sender\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12?\n\trecipient\x18\x02 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountIdB\x04\xc8\xde\x1f\x00\x12\x10\n\x08\x61sset_id\x18\x03 \x01(\r\x12\x10\n\x08quantums\x18\x04 \x01(\x04:\x0b\x82\xe7\xb0*\x06sender\"\xb7\x01\n\x19MsgWithdrawFromSubaccount\x12<\n\x06sender\x18\x02 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountIdB\x04\xc8\xde\x1f\x00\x12+\n\trecipient\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12\x10\n\x08\x61sset_id\x18\x03 \x01(\r\x12\x10\n\x08quantums\x18\x04 \x01(\x04:\x0b\x82\xe7\xb0*\x06sender\"\xd1\x01\n\x1aMsgSendFromModuleToAccount\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12\x1a\n\x12sender_module_name\x18\x02 \x01(\t\x12+\n\trecipient\x18\x03 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12-\n\x04\x63oin\x18\x04 \x01(\x0b\x32\x19.cosmos.base.v1beta1.CoinB\x04\xc8\xde\x1f\x00:\x0e\x82\xe7\xb0*\tauthorityB;Z9github.com/dydxprotocol/v4-chain/protocol/x/sending/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.sending.transfer_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z9github.com/dydxprotocol/v4-chain/protocol/x/sending/types'
  _globals['_TRANSFER'].fields_by_name['sender']._loaded_options = None
  _globals['_TRANSFER'].fields_by_name['sender']._serialized_options = b'\310\336\037\000'
  _globals['_TRANSFER'].fields_by_name['recipient']._loaded_options = None
  _globals['_TRANSFER'].fields_by_name['recipient']._serialized_options = b'\310\336\037\000'
  _globals['_MSGDEPOSITTOSUBACCOUNT'].fields_by_name['sender']._loaded_options = None
  _globals['_MSGDEPOSITTOSUBACCOUNT'].fields_by_name['sender']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_MSGDEPOSITTOSUBACCOUNT'].fields_by_name['recipient']._loaded_options = None
  _globals['_MSGDEPOSITTOSUBACCOUNT'].fields_by_name['recipient']._serialized_options = b'\310\336\037\000'
  _globals['_MSGDEPOSITTOSUBACCOUNT']._loaded_options = None
  _globals['_MSGDEPOSITTOSUBACCOUNT']._serialized_options = b'\202\347\260*\006sender'
  _globals['_MSGWITHDRAWFROMSUBACCOUNT'].fields_by_name['sender']._loaded_options = None
  _globals['_MSGWITHDRAWFROMSUBACCOUNT'].fields_by_name['sender']._serialized_options = b'\310\336\037\000'
  _globals['_MSGWITHDRAWFROMSUBACCOUNT'].fields_by_name['recipient']._loaded_options = None
  _globals['_MSGWITHDRAWFROMSUBACCOUNT'].fields_by_name['recipient']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_MSGWITHDRAWFROMSUBACCOUNT']._loaded_options = None
  _globals['_MSGWITHDRAWFROMSUBACCOUNT']._serialized_options = b'\202\347\260*\006sender'
  _globals['_MSGSENDFROMMODULETOACCOUNT'].fields_by_name['authority']._loaded_options = None
  _globals['_MSGSENDFROMMODULETOACCOUNT'].fields_by_name['authority']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_MSGSENDFROMMODULETOACCOUNT'].fields_by_name['recipient']._loaded_options = None
  _globals['_MSGSENDFROMMODULETOACCOUNT'].fields_by_name['recipient']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_MSGSENDFROMMODULETOACCOUNT'].fields_by_name['coin']._loaded_options = None
  _globals['_MSGSENDFROMMODULETOACCOUNT'].fields_by_name['coin']._serialized_options = b'\310\336\037\000'
  _globals['_MSGSENDFROMMODULETOACCOUNT']._loaded_options = None
  _globals['_MSGSENDFROMMODULETOACCOUNT']._serialized_options = b'\202\347\260*\tauthority'
  _globals['_TRANSFER']._serialized_start=211
  _globals['_TRANSFER']._serialized_end=382
  _globals['_MSGDEPOSITTOSUBACCOUNT']._serialized_start=385
  _globals['_MSGDEPOSITTOSUBACCOUNT']._serialized_end=565
  _globals['_MSGWITHDRAWFROMSUBACCOUNT']._serialized_start=568
  _globals['_MSGWITHDRAWFROMSUBACCOUNT']._serialized_end=751
  _globals['_MSGSENDFROMMODULETOACCOUNT']._serialized_start=754
  _globals['_MSGSENDFROMMODULETOACCOUNT']._serialized_end=963
# @@protoc_insertion_point(module_scope)
