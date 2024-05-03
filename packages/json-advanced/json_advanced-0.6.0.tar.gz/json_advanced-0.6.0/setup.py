import os
import re

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="json-advanced",
    version=get_version("json_advanced"),
    python_requires=">=3",
    url="https://github.com/mahdikiani/json-advanced",
    license="MIT License",
    description="This Python package provides an extended JSON encoder class, `JSONSerializer`, that enables encoding of complex Python data types such as `datetime.datetime`, `datetime.date`, `datetime.time`, `bytes` and `uuid`. It also supports objects that have a `to_json` method, allowing for customizable JSON encoding.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Mahdi Kiani",
    author_email="mahdikiany@gmail.com",
    packages=find_packages(),
    zip_safe=False,
)
