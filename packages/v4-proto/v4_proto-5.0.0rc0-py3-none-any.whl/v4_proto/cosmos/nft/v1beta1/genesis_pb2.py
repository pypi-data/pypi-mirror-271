# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/nft/v1beta1/genesis.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.cosmos.nft.v1beta1 import nft_pb2 as cosmos_dot_nft_dot_v1beta1_dot_nft__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n cosmos/nft/v1beta1/genesis.proto\x12\x12\x63osmos.nft.v1beta1\x1a\x1c\x63osmos/nft/v1beta1/nft.proto\"f\n\x0cGenesisState\x12*\n\x07\x63lasses\x18\x01 \x03(\x0b\x32\x19.cosmos.nft.v1beta1.Class\x12*\n\x07\x65ntries\x18\x02 \x03(\x0b\x32\x19.cosmos.nft.v1beta1.Entry\"=\n\x05\x45ntry\x12\r\n\x05owner\x18\x01 \x01(\t\x12%\n\x04nfts\x18\x02 \x03(\x0b\x32\x17.cosmos.nft.v1beta1.NFTB\x14Z\x12\x63osmossdk.io/x/nftb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.nft.v1beta1.genesis_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\022cosmossdk.io/x/nft'
  _globals['_GENESISSTATE']._serialized_start=86
  _globals['_GENESISSTATE']._serialized_end=188
  _globals['_ENTRY']._serialized_start=190
  _globals['_ENTRY']._serialized_end=251
# @@protoc_insertion_point(module_scope)
