#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Product:   Macal DSL
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      2024-04-30
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

# sysvar containts the functions to get the system environment variables for Macal DSL

import os

_INCLUDE_PATH_ENV_VAR_NAME = "MACAL_DSL_PATH"
_LIBRARY_PATH_ENV_VAR_NAME = "MACAL_DSL_LIB_PATH"


def get_macal_dsl_path() -> str:
    return os.getenv(_INCLUDE_PATH_ENV_VAR_NAME, "")


def get_macal_dsl_lib_path() -> str:
    return os.getenv(_LIBRARY_PATH_ENV_VAR_NAME, "")
