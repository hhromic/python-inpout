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

For saving/loading data using MessagePack and LZ4 compression, the following convenience functions are provided:

* `load_obj(path, **kwargs)`: load a single object from the file in `path`. See below for `kwargs`.
* `load_iter(path, **kwargs)`: iterate objects from the file in `path`. See below for `kwargs`.
* `save_obj(obj, path, **kwargs)`: save a single object `obj` to a file in `path`. See below for `kwargs`.
* `save_iter(iterable, path, **kwargs)`: save a interable `iterable` of objects to a file in `path`. See below for `kwargs`.

For more fine-grained control, the following context-aware functions are also provided:

* `decompressing_unpacker(path, **kwargs)`: create a decompressing unpacker context manager to be used as a data reader. See below for `kwargs`.
* `compressing_pack(path, **kwargs)`: create a compressing pack context manager to be used as a data writer. See below for `kwargs`.

If you want to pack data with MessagePack but without compression, you might use these functions directly:

* `pack(obj, stream, **kwargs)`: pack a single object `obj` using MessagePack (with extended types support) and write packed bytes to a stream of bytes in `stream`. See below for `kwargs`.
* `packb(obj, **kwargs)`: pack a single object `obj` using MessagePack (with extended types support) and return packed bytes. See below for `kwargs`.
* `unpack(stream, **kwargs)`: unpack a stream of packed bytes in `stream` using MessagePack (with extended types support) and return a single unpacked object. See below for `kwargs`.
* `unpackb(packed, **kwargs)`: unpack packed bytes using MessagePack (with extended types support) in `packed` and return a single unpacked object. See below for `kwargs`.

If you want to compress data using LZ4 without packing with MessagePack, you might use these context-aware functions directly:

* `compressor(path, level=LZ4F_COMPRESSION_MAX)`: create a data compressing context manager for file writing to `path`. A compression level can be specified in `level`. Values lower than `3` (including negative ones) use fast compression. Recommended range for hc compression is between `4` and `9`. More information can be [found here](https://github.com/lz4/lz4/blob/dev/README.md).
* `decompressor(path)`: create a data decompressing context manager for file reading from `path`.

Functions involving data packing with MessagePack support optional keyword arguments (`kwargs`) to be passed directly to MessagePack. Useful options are described below:

* `use_list`: can be `True` (default) or `False`. List is the default sequence type of Python. But tuples are lighter than lists. You can use `use_list=False` while unpacking when performance is important for your program. Python objects that require hashable elements such as `dict` or `set` can't use lists as key, therefore `use_list=False` is required for unpacking data containing tuples as keys.

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

# demonstrate the compressing pack function
with inpout.compressing_pack("test4.mp.lz4") as pack:
    for obj in (obj1, obj2, obj3, obj4, obj5, obj6):
        pack(obj)

# demonstrate the decompressing unpacker
with inpout.decompressing_unpacker("test4.mp.lz4", use_list=False) as reader:
    for obj in reader:
        print("OBJ=%r" % (obj,))
```

## MessagePack Extended Types

This library supports MessagePack extended types and includes encoders/decoders for two standard Python objects: `set` (typecode `127`) and `datetime` (typecode `126`). These are automatically registered upon importing the library.

* `set` objects are serialised as tuples containing their elements, therefore `use_list=False` must be used when deserialising data with `set` objects.
* `datetime` objects are serialised as a floating point number counting the number of seconds since the UNIX epoch (00:00:00 on January 1, 1970). Timezone information is used correctly for serialisation but not stored, therefore they will be re-created as naive `datetime` objects, i.e. without timezone.

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

