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

# Main IDE application

import sys
import curses as cs
from macal.__about__ import __version__
from macal.backend.editor import Editor
from macal.backend.palette import Palette
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Macal DSL IDE")
    parser.add_argument("-l", "--library", help="path to libraries", default="./lib")
    parser.add_argument(
        "-v", "--version", action="version", version=f"Macal DSL IDE v{__version__}"
    )
    parser.add_argument("filename", nargs="?", help="File to open")
    return parser.parse_args()


def init_screen() -> cs.window:
    window = cs.initscr()
    cs.cbreak()
    cs.noecho()
    cs.raw()
    window.keypad(True)
    try:
        cs.start_color()
    except:
        pass
    return window


def run(stdscr, args: argparse.Namespace) -> None:
    rows, columns = stdscr.getmaxyx()  # Get the screen size
    title = f"Macal DSL IDE v{__version__} - A simple cli based IDE"
    editor = Editor(0, 0, rows, columns, title, Palette())
    if args.filename:
        editor.LoadFromFile(args.filename)
    if args.library:
        editor.Libraries = args.library
    editor.Edit()


def main():
    args = parse_args()
    stdscr = init_screen()
    try:
        run(stdscr, args)
    except Exception as e:  # ensure we restore the terminal state, hopefully.
        cs.nocbreak()
        cs.echo()
        cs.endwin()
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
