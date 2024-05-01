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
# IO Library external functions

import json
import os
from typing import Any


def loadTextFile(fileName: str) -> str:
    """Implementation of Load function"""
    with open(fileName, "r") as tf:
        content = tf.read()
    return content


def readJSONFile(fileName: str) -> str:
    """Implementation of Read JSON file function"""
    with open(fileName, "r") as fp:
        content = json.load(fp)
    return content


def existsFile(filename: str) -> bool:
    """Implementation of Exists function"""
    return os.path.exists(filename)


def saveTextFile(filename: str, content: str) -> bool:
    """Implementation of Save function"""
    with open(filename, "w") as tf:
        tf.write(content)
    return True


def writeJSONFile(filename: str, content: str) -> bool:
    """Implementation of Save function"""
    with open(filename, "w") as fp:
        json.dump(content, fp, indent=4)
    return True


def getLastRun(org_name: str, default: Any) -> Any:
    """Implementation of GetLastRun function"""
    fileName = f"/tmp/last_run_{org_name}.ctl"
    if os.name == "nt":
        fileName = f"c:/temp/last_run_{org_name}.ctl"
    if os.path.exists(fileName):
        with open(fileName, "r") as tf:
            result = tf.read()
        if result is None or result == "":
            result = default
    else:
        result = default
    return result


def setLastRun(org_name: str, iso_now: Any) -> Any:
    """Implementation of SetLastRun function"""
    fileName = f"/tmp/last_run_{org_name}.ctl"
    if os.name == "nt":
        fileName = f"c:/temp/last_run_{org_name}.ctl"
    with open(fileName, "w") as tf:
        tf.write(iso_now)


def getPwd() -> str:
    """Implementation of GetPwd function"""
    return os.getcwd()
