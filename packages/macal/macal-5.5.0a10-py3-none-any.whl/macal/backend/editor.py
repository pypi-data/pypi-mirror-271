# -*- coding: utf-8 -*-
#
# Product:   Macal DSL IDE
# Author:    Marco Caspers
# Email:     SamaDevTeam@westcon.com
# License:   MIT License
# Date:      2024-04-19
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

# Editor class


import sys
import os
import curses as cs
import click  # type: ignore
import datetime
import pathlib
from typing import Optional
from macal.backend.input_dialog import InputDialog
from macal.backend.message_dialog import MessageDialog, TextDialog
from macal.backend.menu import Menu
from macal.backend.palette import Palette
from macal.macal import Macal
from macal.frontend.mlexer import Lexer, Token
from macal.sysvar import get_macal_dsl_lib_path, get_macal_dsl_path

TAB = ord("\t")
ENTER = [10, 13]
HOME = [cs.KEY_HOME, 262]
BACKSPACE = [8, 127, 263]
DELETE = [330]
RESIZE = 410
CTRL_RIGHT_ARROW = 561
CTRL_LEFT_ARROW = 546
CTRL_PAGE_DOWN = 531
CTRL_PAGE_UP = 536
CTRL_D = 4
CTRL_F = 6
CTRL_G = 7
CTRL_X = 24

SHIFT_LEFT_ARROW = 393
SHIFT_RIGHT_ARROW = 402
SHIFT_UP_ARROW = 337
SHIFT_DOWN_ARROW = 336

TEMP_FILE = "/tmp/mide_temp.mcl"


class Editor:
    def __init__(
        self, top: int, left: int, rows: int, columns: int, title: str, palette: Palette
    ) -> None:
        self._window_top: int = top
        self._window_left: int = left
        self._window_rows: int = rows
        self._window_columns: int = columns

        self.palette: Palette = palette

        self._canvas: cs.window
        self._init_canvas()

        self._canvas_top: int = 1
        self._canvas_left: int = 5
        self._canvas_rows: int = rows - 2
        self._canvas_columns: int = columns - 5
        self._page_length: int = self._canvas_rows - 1
        self._page_width: int = self._canvas_columns - 1

        self._buffer: list[list[int]] = [[]]  # Buffer for the file
        self.search_results: list[tuple[int, int]] = []
        self.search_index: int = 0

        self._block_start: tuple[int, int] = (-1, -1)
        self._block_end: tuple[int, int] = (-1, -1)

        self.top: int = 0
        self.left: int = 0
        self.cursor_x: int = 0
        self.cursor_y: int = 0
        self._filename: str = "noname.txt"
        self.title: str = title or "Macal DSL IDE - A Simple Terminal IDE"
        self.insert: bool = True
        self._menu: Menu
        self._libraries: str = ""
        self.modified: bool = False
        self.marking: bool = False
        self._InitMenu()

    def reset(self):
        self._buffer = [[]]
        self.top = 0
        self.left = 0
        self.cursor_x = 0
        self.cursor_y = 0
        self._filename = "noname.txt"
        self.insert = True
        self.modified = False
        self.search_index = 0
        self.search_results = []
        self._block_start = (-1, -1)
        self._block_end = (-1, -1)

    def reset_block(self) -> None:
        self._block_start = (-1, -1)
        self._block_end = (-1, -1)
        self._marking = False

    def DoBounds(self):
        if self.cursor_x < 0:
            if self.left > 0:
                self.left -= 1
            self.cursor_x = 0

        if self.cursor_y < 0:
            if self.top > 0:
                self.top -= 1
            self.cursor_y = 0

        if self.cursor_x >= self._canvas_columns:
            self.cursor_x = self._canvas_columns - 1
            self.left += 1

        if self.cursor_y >= self._canvas_rows - 1:
            self.top += 1
            self.cursor_y = self._canvas_rows - 2

    def sort_block(self) -> None:
        sy, sx = self._block_start
        ey, ex = self._block_end
        if sy > ey or (sy == ey and sx > ex):
            self._block_start = (ey, ex)
            self._block_end = (sy, sx)

    def _log(self, msg: str) -> None:
        with open("editor.log", "a") as f:
            f.write(f"{datetime.date} {datetime.time} {msg}\n")

    @property
    def Libraries(self) -> str:
        return self._libraries

    @Libraries.setter
    def Libraries(self, libraries: str) -> None:
        self._libraries = libraries

    @property
    def lines(self) -> int:
        return len(self._buffer)

    @property
    def page_width(self) -> int:
        return self._page_width

    @property
    def page_length(self) -> int:
        return self._page_length

    @property
    def pages(self) -> int:
        return (len(self._buffer) - 1) // self._page_length

    def _init_canvas(self) -> None:
        self._canvas = cs.newwin(
            self._window_rows, self._window_columns, self._window_top, self._window_left
        )
        self._canvas.bkgd(" ", self.palette.editor)
        self._canvas.keypad(True)
        self._canvas.nodelay(True)

    def _InitMenu(self) -> None:
        self._menu = Menu(0, 0, self.palette.status, self.palette.default)
        self._menu.AddOption("New", "n", self._HandleNewFile)
        self._menu.AddOption("Save", "s", self._HandleSaveToFile)
        self._menu.AddOption("Load", "l", self._HandleLoadFromFile)
        self._menu.AddOption("Quit", "q", self._HandleQuit)
        self._menu.AddOption("Run", "r", self._Run)

    def CloseScreen(self) -> None:
        cs.echo()  # Echo input
        cs.nocbreak()  # Enable buffering
        cs.endwin()  # End the window

    def Shutdown(self) -> None:
        self._canvas.keypad(False)  # Disable keypad
        self.CloseScreen()  # Close the window

    def _DrawTitle(self) -> None:
        available_width = (
            self._canvas_columns - self._menu.option_width + 2 - len(self.title)
        )
        left = self._menu.option_width + available_width // 2
        self._canvas.addstr(0, 0, " " * (self._canvas_columns + 5), self.palette.status)
        self._menu.Draw(self._canvas)
        self._canvas.addstr(0, left, self.title, self.palette.status)

    def _Draw(self) -> None:
        self._DrawTitle()
        l = len(self._buffer)
        sy, sx = self._block_start
        ey, ex = self._block_end
        for i in range(self._canvas_rows - 1):  # Print the buffer
            brow: int = i + self.top
            self._canvas.move(self._canvas_top + i, self._canvas_left)
            if brow >= 0 and brow < l:
                for j in range(self._canvas_columns - 1):
                    bcol = j + self.left
                    if bcol >= 0 and bcol < len(self._buffer[brow]):
                        if self.marking:
                            if (
                                sy <= brow <= ey
                                and sx <= bcol <= ex
                                and not (brow == ey and bcol == ex)
                            ):
                                self._canvas.addch(
                                    self._buffer[brow][bcol], self.palette.highlight
                                )
                            else:
                                self._canvas.addch(self._buffer[brow][bcol])
                        else:
                            self._canvas.addch(self._buffer[brow][bcol])
            self._canvas.clrtoeol()  # clear to end of line
            try:
                self._canvas.addch("\n")
            except:
                pass
        self._DrawStatus()

    def _DrawLineNumbers(self) -> None:
        for i in range(self._canvas_rows - 1):
            self._canvas.move(self._canvas_top + i, 0)
            self._canvas.addstr(f"{self.top + i + 1:4}")

    def _DrawCursor(self) -> None:
        try:
            self._canvas.move(
                self._canvas_top + self.cursor_y, self._canvas_left + self.cursor_x
            )
        except Exception as e:
            msg = f"Error: Cannot move cursor to position {self.cursor_x} {self.cursor_y} {self._canvas_top}\n{e}"
            self.Shutdown()
            self._log(msg)
            sys.exit(1)

    def _DrawStatus(self) -> None:
        try:
            self._canvas.addstr(
                self._window_top + self._window_rows - 1,
                0,
                " " * (self._canvas_columns + 5),
                self.palette.status,
            )
        except:
            pass
        try:
            sy, sx = self._block_start
            ey, ex = self._block_end
            status = (
                f"Row: {self.top + self.cursor_y + 1}, Column: {self.left + self.cursor_x + 1}"
                # + f" Top: {self.top}, Left: {self.left}"
                # + f" cX: {self.cursor_x} cY: {self.cursor_y}"
                # + f" bW: {len(self._buffer[self.top + self.cursor_y])}"
                # + f" bL: {len(self._buffer)}"
                # + f" pL: {self._canvas_left} pT: {self._canvas_top}"
                # + f" pR: {self._canvas_rows} pC: {self._canvas_columns}"
                # + f" W: {self._window_top} L: {self._window_left}"
                # + f" pgL: {self.page_length} pgW: {self.page_width}"
                # + f" lines: {self.lines} pages: {self.pages}"
                # + f" block: {sy} {sx} {ey} {ex} {self.marking}"
                + f" {'INS' if self.insert else 'OVR'}"
                + f" {'MOD' if self.modified else ''}"
                + f" {self._filename}"
            )
        except IndexError:
            status = (
                "Index Error"
                + f"Row: {self.top + self.cursor_y}, Column: {self.left + self.cursor_x}"
                + f" Top: {self.top}, Left: {self.left}"
                + f" X: {self.cursor_x} Y: {self.cursor_y}"
                + f" lines: {self.lines} pages: {self.pages}"
                + f" {'INS' if self.insert else 'OVR'}"
            )
        # status = f'{status}{" " * (self._canvas_columns - len(status) - 1)}'
        self._canvas.addstr(
            self._window_top + self._window_rows - 1, 0, status, self.palette.status
        )

    def _Clear(self) -> None:
        self._canvas.erase()

    def _Refresh(self) -> None:
        self._canvas.refresh()

    def LoadFromFile(self, src: Optional[str] = None) -> None:
        if src is None:
            src = self._filename
        self._buffer = []  # Buffer for the file
        try:
            with open(src, "r") as f:
                content: str = f.read().split("\n")  # type: ignore # Read the file
                content = (
                    content[:-1] if len(content) > 1 else content
                )  # Remove the last empty line
                for row in content:
                    self._buffer.append(
                        [ord(c) for c in row]
                    )  # Convert the row to ASCII
                while len(self._buffer) > 1 and len(self._buffer[0]) == 0:
                    del self._buffer[0]
        except FileNotFoundError:
            self._buffer.append([])  # Add an empty line
        self._filename = src

    @property
    def Text(self) -> str:
        return "".join(["".join([chr(c) for c in row]) + "\n" for row in self._buffer])

    def SaveToFile(self, src: Optional[str] = None) -> None:
        if src is None:
            src = self._filename
        with open(src, "w") as f:
            f.write(self.Text)

    def Edit(self) -> None:
        while True:
            self._Clear()
            self._Draw()
            self._DrawLineNumbers()
            self._DrawCursor()
            self._Refresh()
            self._HandleInput()

    def get_key(self) -> int:
        ch: int = -1
        while ch == -1:
            ch = self._canvas.getch()
        return ch

    def help(self) -> None:
        help_text = [
            "Key Bindings:",
            "",
            "F1: Help",
            "F3: Find Next",
            "Page Up: Scroll up",
            "Page Down: Scroll down",
            "Home: Move to start of line",
            "End: Move to end of line",
            "Arrow Keys: Move cursor",
            "Backspace: Delete character",
            "Delete: Delete character",
            "Enter: Newline",
            "Tab: Insert 4 spaces",
            "",
            "_______________CTRL +______________",
            "| D: Delete Line | F: Find        |",
            "| G: Go to Line  | L: Load        |",
            "| N: New File    | Q: Quit        |",
            "| R: Run         | S: Save        |",
            "| V: Paste       | X: Quit        |",
            "| ->: Move right | <-: Move left  |",
            "| Up: Move up    | Down: Move down|",
            "___________________________________",
        ]
        dialog = TextDialog(1, 1, 27, 80, "Help", help_text)
        dialog.ShowDialog()
        self._Pause()

    def _HandleInput(self) -> None:
        ch = self.get_key()
        if self._menu.HandleClickedAction(ch):
            return
        # Arrow Keys
        if ch == cs.KEY_RIGHT:  # Right arrow
            self._HandleRightArrow()
        elif ch == cs.KEY_LEFT:  # Left arrow
            self._HandleLeftArrow()
        elif ch == cs.KEY_UP:  # Up arrow
            self._HandleUpArrow()
        elif ch == cs.KEY_DOWN:  # Down arrow
            self._HandleDownArrow()
        elif ch == cs.KEY_PPAGE:
            self._HandlePageUp()
        elif ch == cs.KEY_NPAGE:
            self._HandlePageDown()
        # Ctrl + Page Up + Page Down
        elif ch == CTRL_PAGE_UP:
            self._HandleScrollToStart()
        elif ch == CTRL_PAGE_DOWN:
            self._HandleScrollToEnd()
        # Ctrl + Arrow Keys
        elif ch == CTRL_RIGHT_ARROW:
            self._HandleCtrlRightArrow()
        elif ch == CTRL_LEFT_ARROW:
            self._HandleCtrlLeftArrow()
        # Shift + Arrow Keys
        elif ch == SHIFT_RIGHT_ARROW:
            self._HandleMarkBlockRight()
        elif ch == SHIFT_LEFT_ARROW:
            self._HandleMarkBlockLeft()
        elif ch == SHIFT_UP_ARROW:
            self._HandleMarkBlockUp()
        elif ch == SHIFT_DOWN_ARROW:
            self._HandleMarkBlockDown()
        # Home + End
        elif ch in HOME:  # Home
            self.cursor_x = 0
        elif ch == cs.KEY_END:  # End
            self.cursor_x = len(self._buffer[self.top + self.cursor_y])
        # Enter + Backspace
        elif ch in ENTER:  # Enter
            self._HandleNewline()
        elif ch in BACKSPACE:  # Backspace
            self._HandleBackspace()
        elif ch == cs.KEY_DC:  # Delete
            self._HandleDelete()
        elif ch == CTRL_D:  # Ctrl + D
            self._HandleDeleteLine()
        elif ch == CTRL_F:  # Ctrl + F
            self._HandleFind()
        elif ch == CTRL_G:  # Ctrl + G
            self._HandleGoToLine()
        elif ch == cs.KEY_F1:  # Help
            self.help()
        elif ch == cs.KEY_F3:  # Find Next
            self._HandleFindNext()
        elif ch == TAB:  # Tab
            self._HandlePrintableCharacter(ord(" "))
            self._HandlePrintableCharacter(ord(" "))
            self._HandlePrintableCharacter(ord(" "))
            self._HandlePrintableCharacter(ord(" "))
        elif ch == RESIZE:  # Resize
            self._Resize()
        elif ch > 31 and ch < 128:  # Printable characters
            self._HandlePrintableCharacter(ch)
        else:
            cs.beep()
            MessageDialog(5, 5, "Error", f"Unknown key: {ch}").ShowDialog()
            self._Pause()

    def _Pause(self) -> None:
        ch: int = -1
        while ch == -1:
            ch = self._canvas.getch()

    def _HandleMarkBlockRight(self) -> None:
        if self.top + self.cursor_y == len(
            self._buffer
        ) - 1 and self.cursor_x + self.left == len(
            self._buffer[self.top + self.cursor_y]
        ):
            cs.beep()
            return
        if self.marking is False:
            self.reset_block()
        if self._block_start == (-1, -1):
            self._block_start = (self.top + self.cursor_y, self.left + self.cursor_x)
        self.cursor_x += 1
        self.DoBounds()
        self._block_end = (self.top + self.cursor_y, self.left + self.cursor_x)
        self.sort_block()
        self.marking = True

    def _HandleMarkBlockLeft(self) -> None:
        if self.left + self.cursor_x - 1 < 0:
            cs.beep()
            return
        if self.marking is False:
            self.reset_block()
        if self._block_start == (-1, -1):
            self._block_start = (self.top + self.cursor_y, self.left + self.cursor_x)
        self.cursor_x -= 1
        self.DoBounds()
        self._block_end = (self.top + self.cursor_y, self.left + self.cursor_x)
        self.sort_block()
        self.marking = True

    def _HandleMarkBlockDown(self) -> None:
        if self.top + self.cursor_y + 1 >= len(self._buffer):
            cs.beep()
            return
        if self.marking is False:
            self.reset_block()
        if self._block_start == (-1, -1):
            self._block_start = (self.top + self.cursor_y, self.left + self.cursor_x)
        self.cursor_y += 1
        self.DoBounds()
        self._block_end = (self.top + self.cursor_y, self.left + self.cursor_x)
        self.sort_block()
        self.marking = True

    def _HandleMarkBlockUp(self) -> None:
        if self.top + self.cursor_y - 1 < 0:
            cs.beep()
            return
        if self.marking is False:
            self.reset_block()
        if self._block_start == (-1, -1):
            self._block_start = (self.top + self.cursor_y, self.left + self.cursor_x)
        self.cursor_y -= 1
        self.DoBounds()
        self._block_end = (self.top + self.cursor_y, self.left + self.cursor_x)
        self.sort_block()
        self.marking = True

    def _HandleGoToLine(self) -> None:
        self.marking = False
        dialog = InputDialog(5, 5, "Go to line: ")
        dialog.Input()
        try:
            line = int(dialog.text)
        except ValueError:
            cs.beep()
            return
        if line < 1 or line > len(self._buffer):
            cs.beep()
            return
        self.top = line - 1
        self.cursor_y = 0
        self.left = 0
        self.cursor_x = 0

    def _HandleFind(self) -> None:
        self.marking = False
        dialog = InputDialog(5, self._canvas_left, "Find: ", self._canvas_columns - 2)
        dialog.Input()
        if dialog.text == "":
            return
        self.search_results = []
        for i, row in enumerate(self._buffer):
            line = "".join([chr(c) for c in row])
            for col in range(len(line) - len(dialog.text) + 1):
                if line[col : col + len(dialog.text)] == dialog.text:
                    self.search_results.append((i, col))
        if len(self.search_results) == 0:
            return
        self.search_index = -1
        self._HandleFindNext()

    def _HandleFindNext(self) -> None:
        self.marking = False
        if self.search_index >= len(self.search_results) - 1:
            self.search_index = -1
        self.search_index += 1
        l, c = self.search_results[self.search_index]
        self.top = l
        self.cursor_y = 0
        self.left = 0
        self.cursor_x = c
        if self.cursor_x >= self._canvas_columns:
            self.left = self.cursor_x - self._canvas_columns
            self.cursor_x = self._canvas_columns - 1

    def _HandleCtrlRightArrow(self) -> None:
        self.marking = False
        y = self.top + self.cursor_y
        x = self.left + self.cursor_x
        if x == len(self._buffer[y]):
            cs.beep()
            return
        lexer: Lexer = Lexer()
        source = "".join([chr(c) for c in self._buffer[y]])
        tokens: list[Token] = lexer.lex(source, "")
        # Note: x is 0-based, column is 1-based
        for token in tokens:
            if token.column - 1 > x:
                self.cursor_x = token.column - 1 - self.left
                break
        if self.left + self.cursor_x > len(self._buffer[y]):
            self.cursor_x = len(self._buffer[y]) - self.left
        if self.cursor_x > self._canvas_columns:
            self.left = self.cursor_x - self._canvas_columns
            self.cursor_x = self._canvas_columns - 1

    def _HandleCtrlLeftArrow(self) -> None:
        self.marking = False
        y = self.top + self.cursor_y
        x = self.left + self.cursor_x
        if x == 0:
            cs.beep()
            return
        lexer: Lexer = Lexer()
        source = "".join([chr(c) for c in self._buffer[y]])
        tokens: list[Token] = lexer.lex(source, "")
        # Note: x is 0-based, column is 1-based
        for token in reversed(tokens):
            if token.column - 1 < x:
                self.cursor_x = token.column - 1 - self.left
                break
        if self.cursor_x < 0:
            self.cursor_x = 0
            self.left = 0

    def _HandleScrollToEnd(self) -> None:
        self.marking = False
        y = self.top + self.cursor_y
        if y >= self.lines:
            cs.beep()
            return
        self.top = self.pages * self._page_length
        self.cursor_y = self.lines - self.top
        self.left = 0
        self.cursor_x = 0

    def _HandleScrollToStart(self) -> None:
        self.marking = False
        self.top = 0
        self.cursor_y = 0
        self.left = 0
        self.cursor_x = 0

    def _HandlePageDown(self):
        self.marking = False
        if self.top + self.cursor_y + self._page_length >= len(self._buffer) - 1:
            cs.beep()
            return
        self.top += self._page_length + self.cursor_y
        self.cursor_y = 0
        self.cursor_x = 0
        self.left = 0

    def _HandlePageUp(self) -> None:
        self.marking = False
        if self.top + self.cursor_y - self._page_length < 0:
            cs.beep()
            return
        self.top -= self._page_length + self.cursor_y
        self.cursor_y = 0
        self.cursor_x = 0
        self.left = 0

    def _HandlePrintableCharacter(self, ch: int) -> None:
        self.marking = False
        if self.insert is True:
            self._buffer[self.top + self.cursor_y].insert(self.left + self.cursor_x, ch)
        else:
            if self.left + self.cursor_x < len(self._buffer[self.cursor_y]):
                self._buffer[self.top + self.cursor_y][self.left + self.cursor_x] = ch
            else:
                self._buffer[self.top + self.cursor_y].append(ch)
        self.cursor_x += 1
        if self.cursor_x >= self._canvas_columns:
            self.cursor_x = self._canvas_columns - 1
            self.left += 1
        self.modified = True

    def _HandleDownArrow(self) -> None:
        self.marking = False
        if self.top + self.cursor_y + 1 >= len(self._buffer):
            cs.beep()
            return
        self.cursor_y += 1
        self.cursor_x = min(self.cursor_x, len(self._buffer[self.top + self.cursor_y]))
        if self.cursor_y >= self._canvas_rows - 1:
            if self.top + self.cursor_y < len(self._buffer):
                self.top += 1
            self.cursor_y = self._canvas_rows - 2

    def _HandleUpArrow(self) -> None:
        self.marking = False
        if self.top + self.cursor_y - 1 < 0:
            cs.beep()
            return
        self.cursor_y -= 1
        self.cursor_x = min(self.cursor_x, len(self._buffer[self.top + self.cursor_y]))
        if self.cursor_y < 0:
            if self.top > 0:
                self.top -= 1
            self.cursor_y = 0

    def _HandleLeftArrow(self) -> None:
        self.marking = False
        if self.left + self.cursor_x - 1 < 0:
            cs.beep()
            return
        if self.left + self.cursor_x > 0:
            self.cursor_x -= 1
        elif self.top + self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = len(self._buffer[self.top + self.cursor_y])
        if self.cursor_x < 0:
            if self.left > 0:
                self.left -= 1
            self.cursor_x = 0

    def _HandleRightArrow(self) -> None:
        self.marking = False
        if self.top + self.cursor_y == len(
            self._buffer
        ) - 1 and self.cursor_x + self.left == len(
            self._buffer[self.top + self.cursor_y]
        ):
            cs.beep()
            return
        if self.cursor_x < len(self._buffer[self.top + self.cursor_y]):
            self.cursor_x += 1
        elif self.top + self.cursor_y < len(self._buffer) - 1:
            self.cursor_y += 1
            self.cursor_x = 0
        if self.cursor_x >= self._canvas_columns:
            self.cursor_x = self._canvas_columns - 1
            if self.left + self.cursor_x < len(self._buffer[self.top + self.cursor_y]):
                self.left += 1

    def _HandleBackspace(self) -> None:
        self.marking = False
        if self.left + self.cursor_x == 0 and self.top + self.cursor_y == 0:
            cs.beep()
            return
        if self.cursor_x > 0:
            self.cursor_x -= 1
            del self._buffer[self.top + self.cursor_y][self.left + self.cursor_x]
        elif self.cursor_x == 0 and self.left > 0:
            self.left -= 1
            del self._buffer[self.top + self.cursor_y][self.left + self.cursor_x]
        elif self.cursor_x == 0 and self.left == 0 and self.top + self.cursor_y > 0:
            l = self._buffer[self.top + self.cursor_y][self.left + self.cursor_x :]
            del self._buffer[self.top + self.cursor_y]
            self.cursor_y -= 1
            self.cursor_x = len(self._buffer[self.top + self.cursor_y])
            self._buffer[self.top + self.cursor_y] += l
        # should not be able to reach this.
        if self.cursor_x < 0:
            if self.left > 0:
                self.left -= 1
            self.cursor_x = 0
        self.modified = True

    def _HandleDelete(self) -> None:
        self.marking = False
        c = self.left + self.cursor_x
        y = self.top + self.cursor_y
        if c == len(self._buffer[y]) and y == len(self._buffer) - 1:
            cs.beep()
            return
        if c < len(self._buffer[y]):
            del self._buffer[y][c]
            return
        if y < len(self._buffer) - 1:
            l = self._buffer[y + 1]
            del self._buffer[y + 1]
            self._buffer[y] += l
        self.modified = True

    def _HandleDeleteLine(self) -> None:
        self.marking = False
        y = self.top + self.cursor_y
        if y == len(self._buffer):
            cs.beep()
            return
        del self._buffer[y]
        self.cursor_x = 0
        self.left = 0
        self.modified = True

    def _HandleNewline(self) -> None:
        self.marking = False
        line = self._buffer[self.top + self.cursor_y][self.left + self.cursor_x :]
        self._buffer[self.top + self.cursor_y] = self._buffer[self.top + self.cursor_y][
            : self.left + self.cursor_x
        ]
        self.cursor_y += 1
        self.cursor_x = 0
        self.left = 0
        self._buffer.insert(self.top + self.cursor_y, line)
        if self.cursor_y >= self._canvas_rows - 1:
            self.top += 1
            self.cursor_y = self._canvas_rows - 2
        self.modified = True

    def _HandleLoadFromFile(self) -> None:
        self.marking = False
        dialog = InputDialog(5, 5, "Load file: ")
        dialog.Input()
        if dialog.text == "":
            return
        if not os.path.exists(dialog.text):
            MessageDialog(5, 5, "Error", f"File not found: {dialog.text}").ShowDialog()
            self._Pause()
            return
        self._filename = dialog.text
        self.LoadFromFile()
        self.modified = False

    def _HandleSaveToFile(self) -> None:
        self.marking = False
        dialog = InputDialog(5, 5, "Save file: ")
        dialog.Input()
        if dialog.text == "":
            return
        self._filename = dialog.text
        self.SaveToFile()
        self.modified = False

    def _HandleModified(self) -> None:
        self.marking = False
        dialog = MessageDialog(5, 5, "Warning", "File has been modified. Save (y/n)?")
        dialog.ShowDialog()
        ch = self.get_key()
        if ch == cs.KEY_ENTER or ch == ord("y") or ch == ord("Y"):
            self.SaveToFile()

    def _HandleQuit(self) -> None:
        self.marking = False
        if self.modified:
            self._HandleModified()
        self.Shutdown()
        sys.exit(0)

    def _RunApplication(self, filename: str) -> None:
        self.marking = False
        macal = Macal()
        macal.AddPath(os.path.dirname(__file__))
        include_path = pathlib.Path(get_macal_dsl_path()).absolute()
        library_path = pathlib.Path(get_macal_dsl_lib_path()).absolute()
        macal.AddPath(str(include_path))
        macal.AddPath(str(library_path))
        if self._libraries:
            macal.AddPath(self._libraries)
        macal.RegisterConstant("argv", sys.argv)
        macal.Run(filename)

    def _HandleNewFile(self) -> None:
        self.marking = False
        if self.modified:
            self._HandleModified()
        self.reset()

    def _Run(self) -> None:
        self.marking = False
        code = self.Text.strip()
        if len(code) == 0:
            MessageDialog(5, 5, "Error", "No code to run").ShowDialog()
            self._Pause()
            return
        self.Shutdown()
        with open(TEMP_FILE, "w") as temp:
            temp.write(code)
        print("Running the application...")
        print()
        error = False
        ex = None
        try:
            self._RunApplication(TEMP_FILE)  # Run the application
            print()
            print("Done, press any key to return.")
        except Exception as e:
            error = True
            ex = e
        finally:
            self.init_screen()
        if error:
            cs.beep()
            TextDialog(
                y=1, x=1, h=26, w=100, title="Error", text=str(ex).splitlines()
            ).ShowDialog()
            self._Pause()

    def init_screen(self):
        click.getchar()
        cs.initscr()
        cs.cbreak()
        cs.noecho()
        cs.raw()
        try:
            cs.start_color()
        except:
            pass
        self._init_canvas()

    def _Resize(self) -> None:
        cs.beep()
        MessageDialog(5, 5, "Error", "Resize not supported").ShowDialog()
        self._Pause()
        self.Shutdown()
        raise NotImplementedError("Resize not supported")
