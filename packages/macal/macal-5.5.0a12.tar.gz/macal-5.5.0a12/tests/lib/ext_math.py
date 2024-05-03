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
# Macal math library external functions
#

from math import (
    acos,
    asin,
    atan,
    ceil,
    cos,
    exp,
    expm1,
    floor,
    log,
    log2,
    log10,
    pow,
    sin,
    sqrt,
    tan,
)
from typing import Any


def math_round(rval: Any, digits=None) -> Any:
    """Implementation of round function"""
    if rval is None:
        raise Exception("Round requires at least one argument.")
    if digits is None:
        return round(rval)
    else:
        return round(rval, digits)


def math_floor(rval) -> Any:
    """Implementation of floor function"""
    return floor(rval)


def math_ceil(rval: Any) -> Any:
    """Implementation of ceil function"""
    return ceil(rval)


def math_cos(rval: Any) -> Any:
    """Implementation of cos function"""
    return cos(rval)


def math_acos(rval: Any) -> Any:
    """Implementation of acos function"""
    return acos(rval)


def math_sin(rval: Any) -> Any:
    """Implementation of sin function"""
    return sin(rval)


def math_asin(rval: Any) -> Any:
    """Implementation of asin function"""
    return asin(rval)


def math_tan(rval: Any) -> Any:
    """Implementation of tan function"""
    return tan(rval)


def math_atan(rval: Any) -> Any:
    """Implementation of atan function"""
    return atan(rval)


def math_sqrt(rval: Any) -> Any:
    """Implementation of sqrt function"""
    return sqrt(rval)


def math_log(rval: Any) -> Any:
    """Implementation of log function"""
    return log(rval)


def math_log2(rval: Any) -> Any:
    """Implementation of log2 function"""
    return log2(rval)


def math_log10(rval: Any) -> Any:
    """Implementation of log10 function"""
    return log10(rval)


def math_exp(rval: Any) -> Any:
    """Implementation of exp function"""
    return exp(rval)


def math_expm1(rval: Any) -> Any:
    """Implementation of expm1 function"""
    return expm1(rval)
