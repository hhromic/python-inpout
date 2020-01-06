# python-inpout

Simple library for input/output using MessagePack and LZ4 compression in Python.

## Installation

You can use `pip` (or any PyPI-compatible package manager) for installation:

    pip install inpout

or, if you prefer a local user installation:

    pip install --user inpout

For Microsoft Windows users, you might need to run `pip` through the Python interpreter:

    python -m pip install inpout

**Note:** Visual C++ 14.0 is required for Windows installation. Get it with *Microsoft Visual C++ Build Tools*: <https://visualstudio.microsoft.com/downloads/>

## Usage

To use the functionality of this library, simply import it in your Python programs:

    import inpout

### High-Level Functions

For saving/loading data using MessagePack and LZ4 compression, the following high-level convenience functions are provided in the root namespace:

* `load_obj(path, **kwargs)`: return a single object loaded from a file on disk.

  See `data_unpacker()` for details on the keyword arguments.

* `load_iter(path, **kwargs)`: return an iterator of objects loaded from a file on disk.

  See `data_unpacker()` for details on the keyword arguments.

* `save_obj(obj, path, **kwargs)`: save a single object `obj` to a file on disk.

  See `data_pack()` for details on the keyword arguments.

* `save_iter(iterable, path, **kwargs)`: save an interable of objects `iterable` to a file on disk.

  See `data_pack()` for details on the keyword arguments.

### Context Manager Functions

For more flexibility, the following context manager functions are provided in the root namespace:

* `data_unpacker(path, compression=True, **kwargs)`: create a data unpacker (MessagePack) context manager with optional compression (LZ4) support to be used as an iterable unpacker.
  - `path`: path to the file on disk containing the data to read.
  - `compression`: boolean flag for using LZ4 compression.
  - `kwargs`: keyword arguments passed directly to the MessagePack unpacker. See below.

* `data_pack(path, compression=True, level=None, append=False, **kwargs)`: create a data pack (MessagePack) context manager with optional compression (LZ4) support and file appending to be used as a packing function.
  - `path`: path to the file on disk that will contain the written data.
  - `compression`: boolean flag for using LZ4 compression.
  - `level`: the compression level for the LZ4 compressor. See `compressor()` for details.
  - `append`: boolean flag for opening the file on disk in appending mode.
  - `kwargs`: keyword arguments passed directly to the MessagePack packer. See below.

### Packing Functions

For packing/unpacking data with MessagePack directly without compression, the following functions are provided in `inpout.packing`:

* `pack(obj, stream, **kwargs)`: pack a single object using MessagePack (with extended types support) to a stream of bytes.
  - `obj`: the object to pack.
  - `stream`: the bytes stream to use for writing data.
  - `kwargs`: keyword arguments passed directly to the MessagePack packer. See below.

* `packb(obj, **kwargs)`: pack a single object using MessagePack (with extended types support) and return packed bytes.
  - `obj`: the object to pack.
  - `kwargs`: keyword arguments passed directly to the MessagePack packer. See below.

* `unpack(stream, **kwargs)`: unpack a stream of packed bytes using MessagePack (with extended types support) and return a single unpacked object.
  - `stream`: the bytes stream to use for reading data.
  - `kwargs`: keyword arguments passed directly to the MessagePack unpacker. See below.

* `unpackb(packed, **kwargs)`: unpack packed bytes using MessagePack (with extended types support) and return a single unpacked object.
  - `packed`: the packed bytes to unpack.
  - `kwargs`: keyword arguments passed directly to the MessagePack unpacker. See below.

### Compressing Functions

For compressing/decompressing arbitrary data with LZ4 directly without packing, the following context manager functions are provided in `inpout.compression`:

* `decompressor(path)`: create a data decompressing context manager to be used as reader.
  - `path`: path to the file on disk containing the compressed data.

* `compressor(path, level=None, append=False)`: create a data compressing context manager to be used as a writer.
  - `path`: path to the file on disk that will contain the compressed data.
  - `level`: compression level to use. Defaults to `LZ4F_COMPRESSION_MAX` if `None`. Values lower than `3` (including negative ones) use fast compression. Recommended range for hc-type compression is between `4` and `9`. More information can be [found here](https://github.com/lz4/lz4/blob/dev/README.md).
  - `append`: boolean flag for opening the file on disk in appending mode.

### Keyword Arguments for MessagePack

Functions involving data packing with MessagePack support optional keyword arguments `kwargs` to be passed directly to MessagePack packer and unpacker. Useful options are described below:

* `use_list`: can be `True` (default) or `False`.

  List is the default sequence/array type for Python. But tuples are lighter than lists. You can use `use_list=False` while unpacking when performance is important for your program. Python objects that require hashable elements such as `dict` or `set` can't use lists as key, therefore `use_list=False` is required for unpacking data containing tuples as keys.

## Examples

Below is example code of how to use the main convenience functions of this library.

```python
from datetime import datetime
import inpout

# create some Python objects to test, set and datetime are supported out of the box
obj1 = [1,2,3,4,5]
obj2 = ("test", 1234)
obj3 = {"test": 1234, "test2": 5678}
obj4 = {"a", "b", "c", 5, 6, 7, 8}
obj5 = datetime.now()
obj6 = {(1,2): "tuple_key"}

# save all the above objects as a single tuple to disk
inpout.save_obj((obj1, obj2, obj3, obj4, obj5), "test1.mp.lz4")

# save all the above objects in order to disk one by one (iterator)
iterator = (o for o in (obj1, obj2, obj3, obj4, obj5))
inpout.save_iter(iterator, "test2.mp.lz4")

# append more data to the same test file (save_obj and save_iter can be mixed)
inpout.save_obj(obj1, "test2.mp.lz4", append=True)
inpout.save_iter((obj2, obj3), "test2.mp.lz4", append=True)

# save an object with a tuple as key to demonstrate 'use_list=False'
inpout.save_obj(obj6, "test3.mp.lz4")

# load the first test file
data = inpout.load_obj("test1.mp.lz4")
print("DATA=%r" % (data,))

# load the second test file (iterator)
for obj in inpout.load_iter("test2.mp.lz4"):
    print("OBJ=%r" % (obj,))

# load the third test file using tuple types, otherwise it fails
data = inpout.load_obj("test3.mp.lz4", use_list=False)
print("DATA=%r" % (data,))

# demonstrate the data pack function
with inpout.data_pack("test4.mp.lz4") as pack:
    for obj in (obj1, obj2, obj3, obj4, obj5, obj6):
        pack(obj)

# demonstrate the data unpacker function
with inpout.data_unpacker("test4.mp.lz4", use_list=False) as unpacker:
    for obj in unpacker:
        print("OBJ=%r" % (obj,))

# demonstrate the data pack function (no compression)
with inpout.data_pack("test4.mp", compression=False) as pack:
    for obj in (obj1, obj2, obj3, obj4, obj5, obj6):
        pack(obj)

# demonstrate the data unpacker function (no compression)
with inpout.data_unpacker("test4.mp", compression=False, use_list=False) as unpacker:
    for obj in unpacker:
        print("OBJ=%r" % (obj,))
```

## MessagePack Extended Types

This library supports MessagePack extended types and includes encoders/decoders for two standard Python objects: `set` (typecode `127`) and `datetime` (typecode `126`). These are automatically registered upon importing the library.

* `set` objects are serialised as tuples containing their elements and reconstructed from these stored tuples.
* `datetime` objects are serialised as a tuple of two integers `(seconds, microseconds)` representing the number of seconds and microseconds since the UNIX epoch (00:00:00 Thursday, 1 January 1970). Timezone information is used for the conversion but not stored, therefore `datetime` objects are reconstructed as naive, i.e. without timezone.

You can also easily create your own encoders/decoders for Python objects and register them for this library to be used during serialisation/deserialisation:

```python
import inpout

class MyType(object):
    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2

# define a representation for your type (encoder)
# we will assign '50' as the typecode for this type
def encode_mytype(obj, packb, ext_type):
    return ext_type(50, packb((obj.data1, obj.data2)))

# define how to create your type from your representation (decoder)
def decode_mytype(data, unpackb):
    data1, data2 = unpackb(data)
    return MyType(data1, data2)

# register custom encoder/decoders for your type
inpout.packing.register_ext_type_encoder(MyType, encode_mytype)
inpout.packing.register_ext_type_decoder(50, decode_mytype)

# test saving/loading your type
obj = MyType("test", 1234)
inpout.save_obj(obj, "test.mp.lz4")
obj2 = inpout.load_obj("test.mp.lz4")
print(obj2.data1, obj2.data2)
```

You can use any typecode for your own extended types, however it must be between `0` and `125` (inclusive).

More information about MessagePack extended types can be [found here](https://github.com/msgpack/msgpack/blob/master/spec.md#extension-types).

## Command-line Tools

The library includes the following command-line tools that are installed automatically by `pip`:

* `inpout-pprint`: iterate and pretty-print data files generated by this library.

  This tool is based on the `load_iter` function with the `use_list=False` keyword argument. Compression is activated if filenames end with `.lz4` (case insensitive). Optionally, the `NUMBER` of objects to process from each input file can be also provided. Usage:

      $ inpout-pprint [-n NUMBER] FILENAME [FILENAME ...]

## License

This software is under the **Apache License 2.0**.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

