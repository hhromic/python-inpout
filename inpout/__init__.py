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

"""Simple input/output using MessagePack and LZ4 package."""

from datetime import datetime
from functools import partial
from . import compression
from . import packing
from . import ext_types
from .inpout import (
    data_unpacker,
    data_pack,
    load_obj,
    load_iter,
    save_obj,
    save_iter,
)

# register included extended type for Python 'set' objects
packing.register_ext_type_encoder(set, partial(ext_types.encode_set, typecode=127))
packing.register_ext_type_decoder(127, ext_types.decode_set)

# register included extended type for Python 'datetime' objects
packing.register_ext_type_encoder(datetime, partial(ext_types.encode_datetime, typecode=126))
packing.register_ext_type_decoder(126, ext_types.decode_datetime)
