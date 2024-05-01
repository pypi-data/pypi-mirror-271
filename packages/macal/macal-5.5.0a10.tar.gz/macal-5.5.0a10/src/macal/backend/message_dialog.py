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

# Message dialog class


import curses as cs


class MessageDialog:
    def __init__(self, y: int, x: int, title: str, message: str) -> None:
        if len(title) > 38:
            raise ValueError("Title too long")
        if len(message) > 80:
            raise ValueError("Message too long")
        self.y: int = y
        self.x: int = x
        self.width: int = len(message) + 4
        self.title: str = title
        self.message: str = message
        self.window = cs.newwin(3, self.width, y, x)

    def _Draw(self) -> None:
        self.window.box()
        self.window.addstr(0, (self.width - len(self.title)) // 2, self.title)
        self.window.addstr(1, 2, self.message)
        self.window.refresh()

    def ShowDialog(self) -> None:
        self._Draw()


class TextDialog:
    def __init__(
        self, y: int, x: int, h: int, w: int, title: str, text: list[str]
    ) -> None:
        if len(title) > w - 2:
            raise ValueError("Title too wide")
        for l in text:
            if len(l) > w - 4:
                raise ValueError("Text too wide")
        if len(text) > h - 2:
            raise ValueError("Text too long")
        self.y: int = y
        self.x: int = x
        self.width: int = w
        self.title: str = title
        self.text: list[str] = text
        self.window = cs.newwin(h, w, y, x)

    def _Draw(self) -> None:
        self.window.box()
        self.window.addstr(0, (self.width - len(self.title)) // 2, self.title)
        for i, line in enumerate(self.text):
            self.window.addstr(i + 1, 2, line)
        self.window.refresh()

    def ShowDialog(self) -> None:
        self._Draw()
