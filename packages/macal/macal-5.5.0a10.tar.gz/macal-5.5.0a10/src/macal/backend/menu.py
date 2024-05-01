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

# Menu + MenuOption classes


class MenuOption:
    def __init__(self, text: str, shortcut: str, action) -> None:
        self.text: str = text
        self.shortcut: str = shortcut
        self.action = action

    @property
    def length(self) -> int:
        return len(self.text)

    def Draw(self, window, top: int, left: int, color, shortcut_color) -> None:
        lpos = self.text.find(self.shortcut.upper())
        window.addstr(top, left, self.text[:lpos], color)
        window.addstr(top, left + lpos, self.shortcut.upper(), shortcut_color)
        window.addstr(top, left + lpos + 1, self.text[lpos + 1 :], color)

    def IsClicked(self, ch: int) -> bool:
        return ch == ord(self.shortcut) & 0x1F


class Menu:
    def __init__(self, top: int, left: int, color, shortcut_color) -> None:
        self.top: int = top
        self.left: int = left
        self._color = color
        self._shortcut_color = shortcut_color
        self._options: list[MenuOption] = []

    def AddOption(self, text: str, shortcut: str, action) -> None:
        self._options.append(MenuOption(text, shortcut, action))

    @property
    def option_width(self) -> int:
        return sum([option.length + 2 for option in self._options])

    def Draw(self, canvas) -> None:
        option_left = 2
        for option in self._options:
            option.Draw(
                canvas,
                0,
                option_left,
                self._color,
                self._shortcut_color,
            )
            option_left += option.length + 2

    def HandleClickedAction(self, ch: int) -> bool:
        for option in self._options:
            if option.IsClicked(ch):
                option.action()
                return True
        return False
