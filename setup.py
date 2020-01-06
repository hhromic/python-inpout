"""Main setup script."""

from setuptools import setup, find_packages

NAME = "inpout"
VERSION = "1.0.8"
DESCRIPTION = "Simple input/output using MessagePack and LZ4 for Python"
AUTHOR = "Hugo Hromic"
AUTHOR_EMAIL = "hhromic@gmail.com"
URL = "https://github.com/hhromic/python-inpout"
DOWNLOAD_URL = URL + "/tarball/" + VERSION
REQUIRES = [
    "msgpack",
    "py-lz4framed",
]
CLASSIFIERS = [
    "Topic :: System :: Archiving",
    "Intended Audience :: Developers",
]
KEYWORDS = [
    "messagepack",
    "lz4",
    "input",
    "output",
    "library",
]
ENTRY_POINTS = {
    "console_scripts": [
        "inpout-pprint = inpout.cli:pprint",
    ],
}
LICENSE = "Apache-2.0"

def _read_file(filename):
    with open(filename) as reader:
        return reader.read()

setup(
    name=NAME, version=VERSION, description=DESCRIPTION,
    author=AUTHOR, author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR, maintainer_email=AUTHOR_EMAIL,
    url=URL, download_url=DOWNLOAD_URL,
    classifiers=CLASSIFIERS,
    install_requires=REQUIRES,
    provides=[NAME],
    entry_points=ENTRY_POINTS,
    keywords=KEYWORDS,
    license=LICENSE,
    platforms=["all"],
    long_description=_read_file("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
