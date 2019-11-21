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

"""Classes and functions for data compression/decompression using LZ4 (http://www.lz4.org)."""

from contextlib import contextmanager
from lz4framed import Compressor, Decompressor
from lz4framed import Lz4FramedError, Lz4FramedNoDataError
from lz4framed import LZ4F_COMPRESSION_MAX

class _WritableCompressor(Compressor):
    def write(self, data): # pylint: disable=missing-docstring
        return self.update(data)

class _ReadableDecompressor(Decompressor):
    def readall(self):  # pylint: disable=missing-docstring
        data_buffer = bytearray()
        for chunk in self:
            data_buffer += chunk
        return bytes(data_buffer)

    def read(self, n=-1):  # pylint: disable=missing-docstring, invalid-name, unused-argument
        if n < 0:
            return self.readall()
        if n == 0:
            return bytes()
        iterator = iter(self)
        data_buffer = bytearray(n)
        bytes_read = 0
        while bytes_read < n:
            try:
                chunk = next(iterator)
                data_buffer[bytes_read:len(chunk)] = chunk
                bytes_read += len(chunk)
            except (Lz4FramedError, Lz4FramedNoDataError, StopIteration):
                break
        return bytes(data_buffer[0:bytes_read])

@contextmanager
def compressor(path, level=None, append=False):
    """Create a data compressing context manager for file writing.
       When 'level' is None, a default LZ4F_COMPRESSION_MAX level is used.
       When 'append' is True, the open mode is set for appending data."""
    level = LZ4F_COMPRESSION_MAX if level is None else level
    with open(path, "ab" if append else "wb") as writer:
        with _WritableCompressor(writer, level=level) as context:
            yield context

@contextmanager
def decompressor(path):
    """Create a data decompressing context manager for file reading."""
    with open(path, "rb") as reader:
        yield _ReadableDecompressor(reader)
