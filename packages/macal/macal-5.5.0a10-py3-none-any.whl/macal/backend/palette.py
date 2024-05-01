# -*- coding: utf-8 -*-
#
# Product:   Macal DSL IDE
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      2024-04-29
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

# Palette class

import curses as cs
from typing import Any

editor_color_type = dict[str, tuple[str, str]]

COLOR_BY_NAME = {
    "black": cs.COLOR_BLACK,
    "red": cs.COLOR_RED,
    "green": cs.COLOR_GREEN,
    "yellow": cs.COLOR_YELLOW,
    "blue": cs.COLOR_BLUE,
    "magenta": cs.COLOR_MAGENTA,
    "cyan": cs.COLOR_CYAN,
    "white": cs.COLOR_WHITE,
}


class Palette:
    def __init__(self) -> None:
        self._colors: list[editor_color_type] = []
        self._InitColors()
        self._define_color_pairs()

    # Initialize default colors
    def _InitColors(self) -> None:
        self.AddColor("status", "black", "white")
        self.AddColor("editor", "yellow", "blue")
        self.AddColor("default", "white", "black")
        self.AddColor("error", "white", "red")
        self.AddColor("highlight", "black", "yellow")

    def _define_color_pairs(self) -> None:
        for index, color in enumerate(self._colors):
            name = list(color.keys())[0]
            fg, bg = color[name]
            cs.init_pair(index + 1, COLOR_BY_NAME[fg], COLOR_BY_NAME[bg])

    def _have_color(self, name: str) -> bool:
        for color in self._colors:
            if name in color:
                return True
        return False

    def AddColor(self, name: str, fg: str, bg: str) -> None:
        if self._have_color(name):
            raise ValueError("Color already exists")
        self._colors.append({name: (fg, bg)})
        self._define_color_pairs()

    def EditColor(self, name: str, fg: str, bg: str) -> None:
        index = self._get_color_index(name)
        self._colors[index - 1][name] = (fg, bg)
        self._define_color_pairs()

    def _get_color_index(self, name: str) -> int:
        for index, color in enumerate(self._colors):
            if name in color:
                return index + 1
        raise ValueError("Color not found")

    def GetColor(self, name: str) -> int:
        index = self._get_color_index(name)
        return cs.color_pair(index)

    def __getattr__(self, name: str) -> Any:
        if self._have_color(name):
            return self.GetColor(name)
        return super().__getattribute__(name)
