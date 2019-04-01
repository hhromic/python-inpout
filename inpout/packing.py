# Simple input/output using MessagePack and LZ4 for Python
# Copyright 2019 Hugo Hromic
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functions for data packing and unpacking using MessagePack (https://msgpack.org/)."""

import msgpack

# global extended type encoders mapping (class -> encoder)
_EXT_TYPE_ENCODERS = {}

# global extended type decoders mapping (typecode -> decoder)
_EXT_TYPE_DECODERS = {}

def _encode_ext_type(obj):
    obj_type = type(obj)
    if obj_type in _EXT_TYPE_ENCODERS:
        return _EXT_TYPE_ENCODERS[obj_type](obj, packb=packb, ext_type=msgpack.ExtType)
    raise TypeError("unknown extended type encoder for %r" % obj_type)

def _decode_ext_type(typecode, data):
    if typecode in _EXT_TYPE_DECODERS:
        return _EXT_TYPE_DECODERS[typecode](data, unpackb=unpackb)
    raise TypeError("unknown extended type decoder for typecode %d" % typecode)

def register_ext_type_encoder(python_type, encoder):
    """Register a MessagePack ExtType encoder for a Python type."""
    _EXT_TYPE_ENCODERS[python_type] = encoder

def register_ext_type_decoder(typecode, decoder):
    """Register a Python type decoder for a MessagePack ExtType typecode."""
    _EXT_TYPE_DECODERS[typecode] = decoder

def pack(obj, stream, **kwargs):
    """Pack object using MessagePack (with extended types support)
       and write packed bytes to a stream."""
    msgpack.pack(obj, stream, default=_encode_ext_type, use_bin_type=True, **kwargs)

def packb(obj, **kwargs):
    """Pack object using MessagePack (with extended types support)
       and return packed bytes."""
    return msgpack.packb(obj, default=_encode_ext_type, use_bin_type=True, **kwargs)

def packer(*args, **kwargs):
    """Return a MessagePack (with extended types support) Packer object."""
    return msgpack.Packer(*args, default=_encode_ext_type, use_bin_type=True, **kwargs)

def unpack(stream, **kwargs):
    """Unpack a stream of packed bytes using MessagePack (with extended types support)
       and return unpacked object."""
    return msgpack.unpack(stream, ext_hook=_decode_ext_type, raw=False, **kwargs)

def unpackb(packed, **kwargs):
    """Unpack packed bytes using MessagePack (with extended types support)
       and return unpacked object."""
    return msgpack.unpackb(packed, ext_hook=_decode_ext_type, raw=False, **kwargs)

def unpacker(*args, **kwargs):
    """Return a MessagePack (with extended types support) Unpacker object."""
    return msgpack.Unpacker(*args, ext_hook=_decode_ext_type, raw=False, **kwargs)
