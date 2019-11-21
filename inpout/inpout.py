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

"""Functions for data input/output."""

from contextlib import contextmanager
from .compression import decompressor, compressor
from .packing import unpacker, packer

@contextmanager
def data_unpacker(path, compression=True, **kwargs):
    """Create a data unpacker (MessagePack) context manager with
       optional compression (LZ4) support."""
    with decompressor(path) if compression else open(path, "rb") as reader:
        yield unpacker(reader, **kwargs)

@contextmanager
def data_pack(path, compression=True, level=None, append=False, **kwargs):
    """Create a data pack (MessagePack) context manager with
       optional compression (LZ4) support and file appending."""
    if compression:
        context = compressor(path, level=level, append=append)
    else:
        context = open(path, "ab" if append else "wb")
    with context as writer:
        pkr = packer(**kwargs)
        def _pack(obj):
            writer.write(pkr.pack(obj))
        yield _pack

def load_obj(path, **kwargs):
    """Load an object from disk."""
    with data_unpacker(path, **kwargs) as _unpacker:
        return next(_unpacker)

def load_iter(path, **kwargs):
    """Iterate objects from disk (MessagePack-LZ4 format)."""
    with data_unpacker(path, **kwargs) as _unpacker:
        for obj in _unpacker:
            yield obj

def save_obj(obj, path, **kwargs):
    """Save an object to disk (MessagePack-LZ4 format)."""
    with data_pack(path, **kwargs) as _pack:
        _pack(obj)

def save_iter(iterable, path, **kwargs):
    """Save an iterable to disk (MessagePack-LZ4 format)."""
    with data_pack(path, **kwargs) as _pack:
        for element in iterable:
            _pack(element)
