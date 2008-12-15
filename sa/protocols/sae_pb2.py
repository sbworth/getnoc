#!/usr/bin/python2.4
# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import service
from google.protobuf import service_reflection
from google.protobuf import descriptor_pb2
_ERRORCODE = descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='sae.ErrorCode',
  filename='ErrorCode',
  values=[
    descriptor.EnumValueDescriptor(
      name='ERR_OK', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_INTERNAL', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_INVALID_METHOD', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_INVALID_TRANSACTION', index=3, number=3,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_TRANSACTION_EXISTS', index=4, number=4,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_UNKNOWN_ACTIVATOR', index=5, number=5,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_INVALID_PROFILE', index=6, number=6,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_INVALID_SCHEME', index=7, number=7,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_UNKNOWN_EVENT_SOURCE', index=8, number=8,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_AUTH_FAILED', index=9, number=9,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_AUTH_REQUIRED', index=10, number=10,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_INVALID_UPGRADE', index=11, number=11,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ERR_OVERLOAD', index=12, number=12,
      options=None,
      type=None),
  ],
  options=None,
)


_ACCESSSCHEME = descriptor.EnumDescriptor(
  name='AccessScheme',
  full_name='sae.AccessScheme',
  filename='AccessScheme',
  values=[
    descriptor.EnumValueDescriptor(
      name='TELNET', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='SSH', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='HTTP', index=2, number=2,
      options=None,
      type=None),
  ],
  options=None,
)


_EVENTSOURCE = descriptor.EnumDescriptor(
  name='EventSource',
  full_name='sae.EventSource',
  filename='EventSource',
  values=[
    descriptor.EnumValueDescriptor(
      name='ES_UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ES_SNMP_TRAP', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='ES_SYSLOG', index=2, number=2,
      options=None,
      type=None),
  ],
  options=None,
)


_EVENTACTION = descriptor.EnumDescriptor(
  name='EventAction',
  full_name='sae.EventAction',
  filename='EventAction',
  values=[
    descriptor.EnumValueDescriptor(
      name='EA_IGNORE', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='EA_PROXY', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='EA_CONFIG_CHANGED', index=2, number=2,
      options=None,
      type=None),
  ],
  options=None,
)


ERR_OK = 0
ERR_INTERNAL = 1
ERR_INVALID_METHOD = 2
ERR_INVALID_TRANSACTION = 3
ERR_TRANSACTION_EXISTS = 4
ERR_UNKNOWN_ACTIVATOR = 5
ERR_INVALID_PROFILE = 6
ERR_INVALID_SCHEME = 7
ERR_UNKNOWN_EVENT_SOURCE = 8
ERR_AUTH_FAILED = 9
ERR_AUTH_REQUIRED = 10
ERR_INVALID_UPGRADE = 11
ERR_OVERLOAD = 12
TELNET = 0
SSH = 1
HTTP = 2
ES_UNKNOWN = 0
ES_SNMP_TRAP = 1
ES_SYSLOG = 2
EA_IGNORE = 0
EA_PROXY = 1
EA_CONFIG_CHANGED = 2



_MESSAGE = descriptor.Descriptor(
  name='Message',
  full_name='sae.Message',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='sae.Message.id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='request', full_name='sae.Message.request', index=1,
      number=2, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='response', full_name='sae.Message.response', index=2,
      number=3, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='error', full_name='sae.Message.error', index=3,
      number=4, type=11, cpp_type=10, label=1,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_REQUEST = descriptor.Descriptor(
  name='Request',
  full_name='sae.Request',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='method', full_name='sae.Request.method', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='serialized_request', full_name='sae.Request.serialized_request', index=1,
      number=2, type=12, cpp_type=9, label=2,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_RESPONSE = descriptor.Descriptor(
  name='Response',
  full_name='sae.Response',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='serialized_response', full_name='sae.Response.serialized_response', index=0,
      number=1, type=12, cpp_type=9, label=1,
      default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_ERROR = descriptor.Descriptor(
  name='Error',
  full_name='sae.Error',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='code', full_name='sae.Error.code', index=0,
      number=1, type=14, cpp_type=8, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='text', full_name='sae.Error.text', index=1,
      number=2, type=9, cpp_type=9, label=1,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_ACCESSPROFILE = descriptor.Descriptor(
  name='AccessProfile',
  full_name='sae.AccessProfile',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='profile', full_name='sae.AccessProfile.profile', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='scheme', full_name='sae.AccessProfile.scheme', index=1,
      number=2, type=14, cpp_type=8, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='address', full_name='sae.AccessProfile.address', index=2,
      number=3, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='port', full_name='sae.AccessProfile.port', index=3,
      number=4, type=9, cpp_type=9, label=1,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='user', full_name='sae.AccessProfile.user', index=4,
      number=5, type=9, cpp_type=9, label=1,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='password', full_name='sae.AccessProfile.password', index=5,
      number=6, type=9, cpp_type=9, label=1,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='super_password', full_name='sae.AccessProfile.super_password', index=6,
      number=7, type=9, cpp_type=9, label=1,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='path', full_name='sae.AccessProfile.path', index=7,
      number=8, type=9, cpp_type=9, label=1,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_PINGREQUEST = descriptor.Descriptor(
  name='PingRequest',
  full_name='sae.PingRequest',
  filename='sae.proto',
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_PINGRESPONSE = descriptor.Descriptor(
  name='PingResponse',
  full_name='sae.PingResponse',
  filename='sae.proto',
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_REGISTERREQUEST = descriptor.Descriptor(
  name='RegisterRequest',
  full_name='sae.RegisterRequest',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name', full_name='sae.RegisterRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_REGISTERRESPONSE = descriptor.Descriptor(
  name='RegisterResponse',
  full_name='sae.RegisterResponse',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='nonce', full_name='sae.RegisterResponse.nonce', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_AUTHREQUEST = descriptor.Descriptor(
  name='AuthRequest',
  full_name='sae.AuthRequest',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name', full_name='sae.AuthRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='digest', full_name='sae.AuthRequest.digest', index=1,
      number=2, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_AUTHRESPONSE = descriptor.Descriptor(
  name='AuthResponse',
  full_name='sae.AuthResponse',
  filename='sae.proto',
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_PULLCONFIGREQUEST = descriptor.Descriptor(
  name='PullConfigRequest',
  full_name='sae.PullConfigRequest',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='access_profile', full_name='sae.PullConfigRequest.access_profile', index=0,
      number=1, type=11, cpp_type=10, label=2,
      default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_PULLCONFIGRESPONSE = descriptor.Descriptor(
  name='PullConfigResponse',
  full_name='sae.PullConfigResponse',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='config', full_name='sae.PullConfigResponse.config', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_FILECHECKSUM = descriptor.Descriptor(
  name='FileChecksum',
  full_name='sae.FileChecksum',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name', full_name='sae.FileChecksum.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='hash', full_name='sae.FileChecksum.hash', index=1,
      number=2, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_MANIFESTREQUEST = descriptor.Descriptor(
  name='ManifestRequest',
  full_name='sae.ManifestRequest',
  filename='sae.proto',
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_MANIFESTRESPONSE = descriptor.Descriptor(
  name='ManifestResponse',
  full_name='sae.ManifestResponse',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='files', full_name='sae.ManifestResponse.files', index=0,
      number=1, type=11, cpp_type=10, label=3,
      default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_SOFTWAREUPGRADEREQUEST = descriptor.Descriptor(
  name='SoftwareUpgradeRequest',
  full_name='sae.SoftwareUpgradeRequest',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='names', full_name='sae.SoftwareUpgradeRequest.names', index=0,
      number=1, type=9, cpp_type=9, label=3,
      default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_FILECODE = descriptor.Descriptor(
  name='FileCode',
  full_name='sae.FileCode',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name', full_name='sae.FileCode.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='code', full_name='sae.FileCode.code', index=1,
      number=2, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_SOFTWAREUPGRADERESPONSE = descriptor.Descriptor(
  name='SoftwareUpgradeResponse',
  full_name='sae.SoftwareUpgradeResponse',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='codes', full_name='sae.SoftwareUpgradeResponse.codes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_EVENTFILTERREQUEST = descriptor.Descriptor(
  name='EventFilterRequest',
  full_name='sae.EventFilterRequest',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='sources', full_name='sae.EventFilterRequest.sources', index=0,
      number=1, type=14, cpp_type=8, label=3,
      default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_EVENTFILTERRESPONSE_EVENTFILTER = descriptor.Descriptor(
  name='EventFilter',
  full_name='sae.EventFilterResponse.EventFilter',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='source', full_name='sae.EventFilterResponse.EventFilter.source', index=0,
      number=1, type=14, cpp_type=8, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ip', full_name='sae.EventFilterResponse.EventFilter.ip', index=1,
      number=2, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='mask', full_name='sae.EventFilterResponse.EventFilter.mask', index=2,
      number=3, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='action', full_name='sae.EventFilterResponse.EventFilter.action', index=3,
      number=4, type=14, cpp_type=8, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)

_EVENTFILTERRESPONSE = descriptor.Descriptor(
  name='EventFilterResponse',
  full_name='sae.EventFilterResponse',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='expire', full_name='sae.EventFilterResponse.expire', index=0,
      number=1, type=5, cpp_type=1, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='filters', full_name='sae.EventFilterResponse.filters', index=1,
      number=2, type=11, cpp_type=10, label=3,
      default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_EVENTRESPONSE = descriptor.Descriptor(
  name='EventResponse',
  full_name='sae.EventResponse',
  filename='sae.proto',
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_EVENTPROXYREQUEST = descriptor.Descriptor(
  name='EventProxyRequest',
  full_name='sae.EventProxyRequest',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='source', full_name='sae.EventProxyRequest.source', index=0,
      number=1, type=14, cpp_type=8, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ip', full_name='sae.EventProxyRequest.ip', index=1,
      number=2, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='message', full_name='sae.EventProxyRequest.message', index=2,
      number=3, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='body', full_name='sae.EventProxyRequest.body', index=3,
      number=4, type=9, cpp_type=9, label=1,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_EVENTCONFIGCHANGEDREQUEST = descriptor.Descriptor(
  name='EventConfigChangedRequest',
  full_name='sae.EventConfigChangedRequest',
  filename='sae.proto',
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='source', full_name='sae.EventConfigChangedRequest.source', index=0,
      number=1, type=14, cpp_type=8, label=2,
      default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='ip', full_name='sae.EventConfigChangedRequest.ip', index=1,
      number=2, type=9, cpp_type=9, label=2,
      default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],  # TODO(robinson): Implement.
  enum_types=[
  ],
  options=None)


_MESSAGE.fields_by_name['request'].message_type = _REQUEST
_MESSAGE.fields_by_name['response'].message_type = _RESPONSE
_MESSAGE.fields_by_name['error'].message_type = _ERROR
_ERROR.fields_by_name['code'].enum_type = _ERRORCODE
_ACCESSPROFILE.fields_by_name['scheme'].enum_type = _ACCESSSCHEME
_PULLCONFIGREQUEST.fields_by_name['access_profile'].message_type = _ACCESSPROFILE
_MANIFESTRESPONSE.fields_by_name['files'].message_type = _FILECHECKSUM
_SOFTWAREUPGRADERESPONSE.fields_by_name['codes'].message_type = _FILECODE
_EVENTFILTERREQUEST.fields_by_name['sources'].enum_type = _EVENTSOURCE
_EVENTFILTERRESPONSE_EVENTFILTER.fields_by_name['source'].enum_type = _EVENTSOURCE
_EVENTFILTERRESPONSE_EVENTFILTER.fields_by_name['action'].enum_type = _EVENTACTION
_EVENTFILTERRESPONSE.fields_by_name['filters'].message_type = _EVENTFILTERRESPONSE_EVENTFILTER
_EVENTPROXYREQUEST.fields_by_name['source'].enum_type = _EVENTSOURCE
_EVENTCONFIGCHANGEDREQUEST.fields_by_name['source'].enum_type = _EVENTSOURCE

class Message(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MESSAGE

class Request(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REQUEST

class Response(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _RESPONSE

class Error(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ERROR

class AccessProfile(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ACCESSPROFILE

class PingRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PINGREQUEST

class PingResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PINGRESPONSE

class RegisterRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REGISTERREQUEST

class RegisterResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REGISTERRESPONSE

class AuthRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHREQUEST

class AuthResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHRESPONSE

class PullConfigRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PULLCONFIGREQUEST

class PullConfigResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PULLCONFIGRESPONSE

class FileChecksum(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FILECHECKSUM

class ManifestRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MANIFESTREQUEST

class ManifestResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MANIFESTRESPONSE

class SoftwareUpgradeRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SOFTWAREUPGRADEREQUEST

class FileCode(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _FILECODE

class SoftwareUpgradeResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SOFTWAREUPGRADERESPONSE

class EventFilterRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EVENTFILTERREQUEST

class EventFilterResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class EventFilter(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _EVENTFILTERRESPONSE_EVENTFILTER
  DESCRIPTOR = _EVENTFILTERRESPONSE

class EventResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EVENTRESPONSE

class EventProxyRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EVENTPROXYREQUEST

class EventConfigChangedRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _EVENTCONFIGCHANGEDREQUEST


_SAESERVICE = descriptor.ServiceDescriptor(
  name='SAEService',
  full_name='sae.SAEService',
  index=0,
  options=None,
  methods=[
  descriptor.MethodDescriptor(
    name='ping',
    full_name='sae.SAEService.ping',
    index=0,
    containing_service=None,
    input_type=_PINGREQUEST,
    output_type=_PINGRESPONSE,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='register',
    full_name='sae.SAEService.register',
    index=1,
    containing_service=None,
    input_type=_REGISTERREQUEST,
    output_type=_REGISTERRESPONSE,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='auth',
    full_name='sae.SAEService.auth',
    index=2,
    containing_service=None,
    input_type=_AUTHREQUEST,
    output_type=_AUTHRESPONSE,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='manifest',
    full_name='sae.SAEService.manifest',
    index=3,
    containing_service=None,
    input_type=_MANIFESTREQUEST,
    output_type=_MANIFESTRESPONSE,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='software_upgrade',
    full_name='sae.SAEService.software_upgrade',
    index=4,
    containing_service=None,
    input_type=_SOFTWAREUPGRADEREQUEST,
    output_type=_SOFTWAREUPGRADERESPONSE,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='pull_config',
    full_name='sae.SAEService.pull_config',
    index=5,
    containing_service=None,
    input_type=_PULLCONFIGREQUEST,
    output_type=_PULLCONFIGRESPONSE,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='event_filter',
    full_name='sae.SAEService.event_filter',
    index=6,
    containing_service=None,
    input_type=_EVENTFILTERREQUEST,
    output_type=_EVENTFILTERRESPONSE,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='event_proxy',
    full_name='sae.SAEService.event_proxy',
    index=7,
    containing_service=None,
    input_type=_EVENTPROXYREQUEST,
    output_type=_EVENTRESPONSE,
    options=None,
  ),
  descriptor.MethodDescriptor(
    name='event_config_changed',
    full_name='sae.SAEService.event_config_changed',
    index=8,
    containing_service=None,
    input_type=_EVENTCONFIGCHANGEDREQUEST,
    output_type=_EVENTRESPONSE,
    options=None,
  ),
])

class SAEService(service.Service):
  __metaclass__ = service_reflection.GeneratedServiceType
  DESCRIPTOR = _SAESERVICE
class SAEService_Stub(SAEService):
  __metaclass__ = service_reflection.GeneratedServiceStubType
  DESCRIPTOR = _SAESERVICE

