# -*- coding: utf-8 -*-
#
# Product:   Macal DSL Library
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      2024-05-01
#
# Copyright 2024 Westcon-Comstor
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT
#

# Product:   Macal
# Author:    Marco Caspers
# Date:      16-10-2023
#
#    This library is licensed under the MIT license.
#
#    (c) 2023 Westcon-Comstor
#    (c) 2023 WestconGroup, Inc.
#    (c) 2023 WestconGroup International Limited
#    (c) 2023 WestconGroup EMEA Operations Limited
#    (c) 2023 WestconGroup European Operations Limited
#    (c) 2023 Sama Development Team
#
# System Library external functions
#

import os
import platform
import sys
from typing import Any, Optional
from dotenv import load_dotenv


def Console(*args, **kwargs):
    print(*args, **kwargs)


def Array(*args) -> list:
    return [arg for arg in args]


def RecordHasField(record: dict, fieldname: str) -> bool:
    """Checks if a record has a field"""
    if not isinstance(record, dict):
        raise TypeError("RecordHasField can only be used on a record")
    if not isinstance(fieldname, str):
        raise TypeError("RecordHasField can only be used with a string as fieldname")
    return fieldname in record


def GetPlatform() -> str:
    return platform.system()


# Implementation of the Items function.
# Items returns key/value pairs.
def RecordItems(var: dict) -> list:
    """Implementation of Items function used in conjunction with foreach for iterating over records.  Items returns key/value pairs."""
    if not isinstance(var, dict):
        raise TypeError("Items can only be used on a record")
    return [{key: value} for key, value in var.items()]


def RecordItemKey(var: dict) -> str:
    """Implementation of Key function used in conjunction the Items function that returns key/value pairs. Key returns the key part of a key value pair."""
    if not isinstance(var, dict):
        raise TypeError("ItemKey can only be used on a record")
    for (
        k,
        _,
    ) in (
        var.items()
    ):  # there are different ways, but this is by far the most simple and safe way to do it.
        return k
    return "nil"  # this should never happen, but just in case we return nil, also we keep the linter happy this way.


def RecordKeys(var: dict) -> list:
    """Implementation of Keys function used in conjunction the Items function that returns key/value pairs. Key returns the key part of a key value pair."""
    if not isinstance(var, dict):
        raise TypeError("Keys can only be used on a record")
    return [k for k in var.keys()]


def RecordItemValue(var: dict) -> Any:
    """Implementation of Value function used in conjunction the Items function that returns key/value pairs. Value returns the value part of a key value pair."""
    if not isinstance(var, dict):
        raise TypeError("ItemValue can only be used on a record")
    for (
        _,
        v,
    ) in (
        var.items()
    ):  # there are different ways, but this is by far the most simple and safe way to do it.
        return v


def RecordValues(var: dict) -> list:
    """Implementation of Value function used in conjunction the Items function that returns key/value pairs. Value returns the value part of a key value pair."""
    if not isinstance(var, dict):
        raise TypeError("Values can only be used on a record")
    return [v for v in var.values()]


__loaded_env = False


def LoadEnv(path: Optional[str] = None) -> None:
    """Loads environment variables from a file"""
    global __loaded_env
    if __loaded_env is True:
        return
    __loaded_env = True
    if path is None:
        load_dotenv()
    else:
        load_dotenv(path)


def GetEnv(varname: str) -> Optional[str]:
    """Returns the value of an environment variable"""
    return os.getenv(varname)


def SetEnv(varname: str, value: str) -> None:
    """Sets the value of an environment variable"""
    os.environ[varname] = value


def GetArgs() -> list:
    """Returns a list of arguments passed to the program"""
    return sys.argv


def GetArg(index: int) -> str:
    """Returns a single argument passed to the program"""
    return sys.argv[index]


def GetArgCount() -> int:
    """Returns the number of arguments passed to the program"""
    return len(sys.argv)
