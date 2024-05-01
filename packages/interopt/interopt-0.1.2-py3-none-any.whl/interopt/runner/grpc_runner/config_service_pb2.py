# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: config_service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x63onfig_service.proto\"#\n\x0fShutdownRequest\x12\x10\n\x08shutdown\x18\x01 \x01(\x08\"#\n\x10ShutdownResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"X\n\x14\x43onfigurationRequest\x12&\n\x0e\x63onfigurations\x18\x01 \x01(\x0b\x32\x0e.Configuration\x12\x18\n\x10output_data_file\x18\x02 \x01(\t\"\x82\x01\n\rConfiguration\x12\x32\n\nparameters\x18\x01 \x03(\x0b\x32\x1e.Configuration.ParametersEntry\x1a=\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x19\n\x05value\x18\x02 \x01(\x0b\x32\n.Parameter:\x02\x38\x01\"\x91\x02\n\tParameter\x12&\n\rinteger_param\x18\x01 \x01(\x0b\x32\r.IntegerParamH\x00\x12 \n\nreal_param\x18\x02 \x01(\x0b\x32\n.RealParamH\x00\x12.\n\x11\x63\x61tegorical_param\x18\x03 \x01(\x0b\x32\x11.CategoricalParamH\x00\x12&\n\rordinal_param\x18\x04 \x01(\x0b\x32\r.OrdinalParamH\x00\x12$\n\x0cstring_param\x18\x05 \x01(\x0b\x32\x0c.StringParamH\x00\x12.\n\x11permutation_param\x18\x06 \x01(\x0b\x32\x11.PermutationParamH\x00\x42\x0c\n\nparam_type\"\x1d\n\x0cIntegerParam\x12\r\n\x05value\x18\x01 \x01(\x05\"\x1a\n\tRealParam\x12\r\n\x05value\x18\x01 \x01(\x02\"!\n\x10\x43\x61tegoricalParam\x12\r\n\x05value\x18\x01 \x01(\x05\"\x1d\n\x0cOrdinalParam\x12\r\n\x05value\x18\x01 \x01(\x05\"\x1c\n\x0bStringParam\x12\r\n\x05value\x18\x01 \x01(\t\"\"\n\x10PermutationParam\x12\x0e\n\x06values\x18\x01 \x03(\x05\"n\n\x15\x43onfigurationResponse\x12\x18\n\x07metrics\x18\x01 \x03(\x0b\x32\x07.Metric\x12\x1e\n\ntimestamps\x18\x02 \x01(\x0b\x32\n.Timestamp\x12\x1b\n\x08\x66\x65\x61sible\x18\x03 \x01(\x0b\x32\t.Feasible\"&\n\x06Metric\x12\x0e\n\x06values\x18\x01 \x03(\x01\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x1e\n\tTimestamp\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\"\x19\n\x08\x46\x65\x61sible\x12\r\n\x05value\x18\x01 \x01(\x08\x32\x97\x01\n\x14\x43onfigurationService\x12N\n\x1dRunConfigurationsClientServer\x12\x15.ConfigurationRequest\x1a\x16.ConfigurationResponse\x12/\n\x08Shutdown\x12\x10.ShutdownRequest\x1a\x11.ShutdownResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'config_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CONFIGURATION_PARAMETERSENTRY']._options = None
  _globals['_CONFIGURATION_PARAMETERSENTRY']._serialized_options = b'8\001'
  _globals['_SHUTDOWNREQUEST']._serialized_start=24
  _globals['_SHUTDOWNREQUEST']._serialized_end=59
  _globals['_SHUTDOWNRESPONSE']._serialized_start=61
  _globals['_SHUTDOWNRESPONSE']._serialized_end=96
  _globals['_CONFIGURATIONREQUEST']._serialized_start=98
  _globals['_CONFIGURATIONREQUEST']._serialized_end=186
  _globals['_CONFIGURATION']._serialized_start=189
  _globals['_CONFIGURATION']._serialized_end=319
  _globals['_CONFIGURATION_PARAMETERSENTRY']._serialized_start=258
  _globals['_CONFIGURATION_PARAMETERSENTRY']._serialized_end=319
  _globals['_PARAMETER']._serialized_start=322
  _globals['_PARAMETER']._serialized_end=595
  _globals['_INTEGERPARAM']._serialized_start=597
  _globals['_INTEGERPARAM']._serialized_end=626
  _globals['_REALPARAM']._serialized_start=628
  _globals['_REALPARAM']._serialized_end=654
  _globals['_CATEGORICALPARAM']._serialized_start=656
  _globals['_CATEGORICALPARAM']._serialized_end=689
  _globals['_ORDINALPARAM']._serialized_start=691
  _globals['_ORDINALPARAM']._serialized_end=720
  _globals['_STRINGPARAM']._serialized_start=722
  _globals['_STRINGPARAM']._serialized_end=750
  _globals['_PERMUTATIONPARAM']._serialized_start=752
  _globals['_PERMUTATIONPARAM']._serialized_end=786
  _globals['_CONFIGURATIONRESPONSE']._serialized_start=788
  _globals['_CONFIGURATIONRESPONSE']._serialized_end=898
  _globals['_METRIC']._serialized_start=900
  _globals['_METRIC']._serialized_end=938
  _globals['_TIMESTAMP']._serialized_start=940
  _globals['_TIMESTAMP']._serialized_end=970
  _globals['_FEASIBLE']._serialized_start=972
  _globals['_FEASIBLE']._serialized_end=997
  _globals['_CONFIGURATIONSERVICE']._serialized_start=1000
  _globals['_CONFIGURATIONSERVICE']._serialized_end=1151
# @@protoc_insertion_point(module_scope)
