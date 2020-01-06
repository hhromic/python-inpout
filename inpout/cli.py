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

"""Command-line tools."""

import sys
from argparse import ArgumentParser
from pprint import PrettyPrinter
from .inpout import load_iter

def pprint():
    """Pretty-print files in MsgPack format with optional compression."""
    parser = ArgumentParser(description=pprint.__doc__)
    parser.add_argument("filenames", metavar="FILENAME", nargs="+",
                        help="an input filename to pretty-print")
    parser.add_argument("-n", metavar="NUMBER", type=int,
                        help="only process the first NUMBER objects"
                             " from each input file")
    args = parser.parse_args()

    # read and pretty-print the given input files
    pprinter = PrettyPrinter()
    for fname in args.filenames:
        sys.stderr.write("Processing file '%s' ...\n" % fname)
        try:
            compression = fname.lower().endswith(".lz4")
            for cnt, obj in enumerate(load_iter(fname, compression=compression, use_list=False)):
                if args.n is None or cnt < args.n:
                    pprinter.pprint(obj)
        except Exception as excp:  # pylint: disable=broad-except
            sys.stderr.write("%s\n" % excp)
