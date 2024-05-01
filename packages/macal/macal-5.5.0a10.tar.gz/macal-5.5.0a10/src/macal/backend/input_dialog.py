# -*- coding: utf-8 -*-
#
# Product:   Macal DSL IDE
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      2024-04-22
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

# Input dialog class


import curses as cs

MAX_WIDTH = 60


class InputDialog:
    def __init__(self, y: int, x: int, title: str, width: int = MAX_WIDTH) -> None:
        if len(title) > width - 2:
            raise ValueError("Title too long")
        self.y: int = y
        self.x: int = x
        self.width: int = width
        self.title: str = title
        self.text: str = ""
        self.window = cs.newwin(3, width, y, x)

    def _Draw(self) -> None:
        self.window.box()
        self.window.addstr(0, (self.width - len(self.title)) // 2, self.title)
        self.window.refresh()

    def Input(self) -> None:
        self._Draw()
        cs.echo()
        self.text = self.window.getstr(1, 2, self.width - 4).decode("utf-8")
        cs.noecho()
