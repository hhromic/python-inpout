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

"""Encoders/decoders for Python types to be used with MessagePack (https://msgpack.org/)."""

from datetime import datetime

def encode_set(obj, typecode, packb, ext_type):
    """Encode a Python 'set' object into a MessagePack ExtType."""
    return ext_type(typecode, packb(tuple(obj)))

def decode_set(data, unpackb):
    """Decode MessagePack data into a Python 'set' object."""
    return set(unpackb(data, use_list=False))

def encode_datetime(obj, typecode, packb, ext_type):
    """Encode a Python 'datetime' object into a MessagePack ExtType."""
    delta = obj - datetime(1970, 1, 1, tzinfo=obj.tzinfo)
    data = delta.seconds + delta.days * 24 * 3600, delta.microseconds
    return ext_type(typecode, packb(data))

def decode_datetime(data, unpackb):
    """Decode MessagePack data into a Python 'datetime' object."""
    seconds, microseconds = unpackb(data)
    return datetime.utcfromtimestamp(seconds).replace(microsecond=microseconds)
