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
# Macal time library external functions
#

import time
from datetime import datetime

NUM_SECONDS_FIVE_MINUTES = 300
NUM_SECONDS_ONE_HOUR = 3600
TIME_FORMAT = "%Y%m%d%H%M%S"
ISO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
ISO_TIME_tzFORMAT = "%Y-%m-%dT%H:%M:%S.0Z"


def DateToUnix(var: str) -> int:
    """Convert a date_string of format YYYYMMDDhhmmss to unix time integer.
    Assumes the date string object is UTC time."""
    dt = datetime.strptime(var, TIME_FORMAT)
    epoch = datetime(1970, 1, 1)
    return int((dt - epoch).total_seconds())


def IsoToUnix(var: str) -> int:
    """Convert a date_string of format %Y-%m-%dT%H:%M:%S.%f to unix time integer.
    Assumes the date string object is in iso format."""
    dt = datetime.strptime(var, ISO_TIME_FORMAT)
    epoch = datetime(1970, 1, 1)
    return int((dt - epoch).total_seconds())


def DateFromUnix(var: int) -> str:
    """Converts time in seconds since UNIX EPOCH to UTC Time format"""
    return time.strftime(TIME_FORMAT, time.gmtime(var))


def IsoFromUnix(var: float) -> str:
    """Converts time in seconds since UNIX EPOCH to UTC Time format"""
    return time.strftime(ISO_TIME_tzFORMAT, time.gmtime(var))


def UtcNow() -> str:
    return datetime.utcnow().strftime("%Y%m%d%H%M%S")


def UtcIsoNow() -> str:
    return "{}Z".format(datetime.utcnow().isoformat())


def IsoNow() -> str:
    return datetime.now().isoformat()


def Now() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def PerfCounter() -> float:
    return time.perf_counter()
