# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/clob/mev.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.dydxprotocol.subaccounts import subaccount_pb2 as dydxprotocol_dot_subaccounts_dot_subaccount__pb2
from v4_proto.dydxprotocol.clob import clob_pair_pb2 as dydxprotocol_dot_clob_dot_clob__pair__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1b\x64ydxprotocol/clob/mev.proto\x12\x11\x64ydxprotocol.clob\x1a\x14gogoproto/gogo.proto\x1a)dydxprotocol/subaccounts/subaccount.proto\x1a!dydxprotocol/clob/clob_pair.proto\"\xb3\x02\n\x08MEVMatch\x12I\n\x19taker_order_subaccount_id\x18\x01 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountId\x12\x15\n\rtaker_fee_ppm\x18\x02 \x01(\x05\x12I\n\x19maker_order_subaccount_id\x18\x03 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountId\x12\x1c\n\x14maker_order_subticks\x18\x04 \x01(\x04\x12\x1a\n\x12maker_order_is_buy\x18\x05 \x01(\x08\x12\x15\n\rmaker_fee_ppm\x18\x06 \x01(\x05\x12\x14\n\x0c\x63lob_pair_id\x18\x07 \x01(\r\x12\x13\n\x0b\x66ill_amount\x18\x08 \x01(\x04\"\xdf\x02\n\x13MEVLiquidationMatch\x12N\n\x18liquidated_subaccount_id\x18\x01 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountIdB\x04\xc8\xde\x1f\x00\x12+\n#insurance_fund_delta_quote_quantums\x18\x02 \x01(\x03\x12O\n\x19maker_order_subaccount_id\x18\x03 \x01(\x0b\x32&.dydxprotocol.subaccounts.SubaccountIdB\x04\xc8\xde\x1f\x00\x12\x1c\n\x14maker_order_subticks\x18\x04 \x01(\x04\x12\x1a\n\x12maker_order_is_buy\x18\x05 \x01(\x08\x12\x15\n\rmaker_fee_ppm\x18\x06 \x01(\x05\x12\x14\n\x0c\x63lob_pair_id\x18\x07 \x01(\r\x12\x13\n\x0b\x66ill_amount\x18\x08 \x01(\x04\"V\n\x0c\x43lobMidPrice\x12\x34\n\tclob_pair\x18\x01 \x01(\x0b\x32\x1b.dydxprotocol.clob.ClobPairB\x04\xc8\xde\x1f\x00\x12\x10\n\x08subticks\x18\x02 \x01(\x04\"\x94\x01\n\x13ValidatorMevMatches\x12\x32\n\x07matches\x18\x01 \x03(\x0b\x32\x1b.dydxprotocol.clob.MEVMatchB\x04\xc8\xde\x1f\x00\x12I\n\x13liquidation_matches\x18\x02 \x03(\x0b\x32&.dydxprotocol.clob.MEVLiquidationMatchB\x04\xc8\xde\x1f\x00\"\xfc\x01\n\x14MevNodeToNodeMetrics\x12\x45\n\x15validator_mev_matches\x18\x01 \x01(\x0b\x32&.dydxprotocol.clob.ValidatorMevMatches\x12>\n\x0f\x63lob_mid_prices\x18\x02 \x03(\x0b\x32\x1f.dydxprotocol.clob.ClobMidPriceB\x04\xc8\xde\x1f\x00\x12>\n\x0e\x62p_mev_matches\x18\x03 \x01(\x0b\x32&.dydxprotocol.clob.ValidatorMevMatches\x12\x1d\n\x15proposal_receive_time\x18\x04 \x01(\x04\x42\x38Z6github.com/dydxprotocol/v4-chain/protocol/x/clob/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.clob.mev_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z6github.com/dydxprotocol/v4-chain/protocol/x/clob/types'
  _globals['_MEVLIQUIDATIONMATCH'].fields_by_name['liquidated_subaccount_id']._loaded_options = None
  _globals['_MEVLIQUIDATIONMATCH'].fields_by_name['liquidated_subaccount_id']._serialized_options = b'\310\336\037\000'
  _globals['_MEVLIQUIDATIONMATCH'].fields_by_name['maker_order_subaccount_id']._loaded_options = None
  _globals['_MEVLIQUIDATIONMATCH'].fields_by_name['maker_order_subaccount_id']._serialized_options = b'\310\336\037\000'
  _globals['_CLOBMIDPRICE'].fields_by_name['clob_pair']._loaded_options = None
  _globals['_CLOBMIDPRICE'].fields_by_name['clob_pair']._serialized_options = b'\310\336\037\000'
  _globals['_VALIDATORMEVMATCHES'].fields_by_name['matches']._loaded_options = None
  _globals['_VALIDATORMEVMATCHES'].fields_by_name['matches']._serialized_options = b'\310\336\037\000'
  _globals['_VALIDATORMEVMATCHES'].fields_by_name['liquidation_matches']._loaded_options = None
  _globals['_VALIDATORMEVMATCHES'].fields_by_name['liquidation_matches']._serialized_options = b'\310\336\037\000'
  _globals['_MEVNODETONODEMETRICS'].fields_by_name['clob_mid_prices']._loaded_options = None
  _globals['_MEVNODETONODEMETRICS'].fields_by_name['clob_mid_prices']._serialized_options = b'\310\336\037\000'
  _globals['_MEVMATCH']._serialized_start=151
  _globals['_MEVMATCH']._serialized_end=458
  _globals['_MEVLIQUIDATIONMATCH']._serialized_start=461
  _globals['_MEVLIQUIDATIONMATCH']._serialized_end=812
  _globals['_CLOBMIDPRICE']._serialized_start=814
  _globals['_CLOBMIDPRICE']._serialized_end=900
  _globals['_VALIDATORMEVMATCHES']._serialized_start=903
  _globals['_VALIDATORMEVMATCHES']._serialized_end=1051
  _globals['_MEVNODETONODEMETRICS']._serialized_start=1054
  _globals['_MEVNODETONODEMETRICS']._serialized_end=1306
# @@protoc_insertion_point(module_scope)
