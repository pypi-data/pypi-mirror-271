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

# mpm is the Macal DSL Package Manager

# The Macal DSL package manager is a simple package manager for Macal DSL packages.
# It allows users to install, uninstall, list, and search for Macal DSL packages.

# A Macal DSL package is a zip file with a .mcp extension that contains Macal DSL code files and/or other resources.

import os
import pathlib
import requests  # type: ignore
import argparse
import subprocess

from macal.sysvar import get_macal_dsl_lib_path
from macal.__about__ import __version__

# DEFAULT_REPO = "https://sigma-reporter.na.westcongrp.com/repository/macal-dsl/"
DEFAULT_REPO = "https://0xc007.nl/macal/"
DEFAULT_LIBRARY_PATH = pathlib.Path(get_macal_dsl_lib_path()).absolute()

PACKAGE_EXTENSION = ".mcp"
PACKAGE_INFO_EXTENSION = ".mpi"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Macal DSL Package Manager")
    parser.add_argument(
        "-v",
        "--version",
        help="Print version information",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-c",
        "--create",
        help="Create a new Macal DSL package",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-i",
        "--install",
        help="Install a Macal DSL package",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-u",
        "--uninstall",
        help="Uninstall a Macal DSL package",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-l",
        "--list",
        help="List installed Macal DSL packages",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Set the Macal DSL library path",
        action="store",
        default=DEFAULT_LIBRARY_PATH,
    )
    parser.add_argument(
        "-s",
        "--search",
        help="Search for Macal DSL packages",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-r",
        "--repo",
        help="Set the Macal DSL package repository",
        action="store",
        default=DEFAULT_REPO,
    )
    parser.add_argument(
        "package",
        help="The Macal DSL package to install, uninstall, or search for",
        nargs="?",
    )
    return parser.parse_args()


def _get_package_url(repo: str, package: str) -> str:
    return f"{repo}{package}{PACKAGE_EXTENSION}"


def install_package(package: str, repo: str, libpath: pathlib.Path) -> None:
    print(f"Installing package {package} from {repo}...")
    # download package zip file from repository
    url = _get_package_url(repo, package)
    response = requests.get(url)
    if response.status_code == 200:
        package_path = libpath / f"{package}{PACKAGE_EXTENSION}"
        # save package zip file to package directory and extract it to the library path
        with open(package_path, "wb") as f:
            f.write(response.content)
        subprocess.run(["unzip", "-o", package_path, "-d", libpath])
        # remove package zip file
        os.remove(package_path)

        print(f"Package {package} installed successfully.")
    else:
        print(f"Failed to install package {package}.")
        print(f"Response code: {response.status_code}")
        print(f"Response content: {response.content}")
    print()


def uninstall_package(package: str, libpath: pathlib.Path) -> None:
    print(f"Uninstalling package {package}...")
    package_path = libpath / f"{package}{PACKAGE_INFO_EXTENSION}"
    with open(package_path, "r") as f:
        package_info = f.readlines()
    ok = False
    for package_file in package_info:
        package_file = package_file.strip()
        package_file_path = libpath / package_file
        if os.path.exists(package_file_path):
            os.remove(package_file_path)
        else:
            ok = False
            break
    if ok:
        print(f"Package {package} uninstalled successfully.")
    else:
        print(f"Package {package} contents not found.")
    print()


def list_packages(libpath: pathlib.Path) -> None:
    print("Installed Macal DSL packages:")
    for package in os.listdir(libpath):
        if not package.endswith(PACKAGE_INFO_EXTENSION):
            continue
        # Print package name without extension
        print(f"  {pathlib.Path(package).stem}")
    print()


def search_packages(package: str, repo: str) -> None:
    print(f"Searching for package {package} in {repo}...")
    url = _get_package_url(repo, package)
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Package {package} found.")
    else:
        print(f"Package {package} not found.")
    print()


def create_package(package: str, libpath: pathlib.Path) -> None:
    print(f"Creating package {package}...")
    package_path = libpath / f"{package}{PACKAGE_INFO_EXTENSION}"
    with open(package_path, "r") as f:
        package_info = f.readlines()
    ok = False
    pif: list[str] = [str(package_path)]
    for package_file in package_info:
        package_file = package_file.strip()
        package_file_path = libpath / package_file
        pif.append(str(package_file_path))
        if os.path.exists(package_file_path):
            ok = True
        else:
            ok = False
            break
    if ok:
        package_zip_path = libpath / f"{package}{PACKAGE_EXTENSION}"
        args = ["zip", "-q", "-j", str(package_zip_path)]
        args.extend(pif)
        subprocess.run(args)

        print(f"Package {package} created successfully.")
        print()
        return
    print(f"Package {package} contents not found.")


def main() -> None:
    args = parse_args()

    if args.path:
        libpath = pathlib.Path(args.path).absolute()
    else:
        libpath = DEFAULT_LIBRARY_PATH

    if not os.path.exists(libpath):
        os.makedirs(libpath)

    if args.package is not None and args.package.endswith(PACKAGE_EXTENSION):
        args.package = args.package.replace(PACKAGE_EXTENSION, "")

    if args.create:
        create_package(args.package, libpath)
        return

    if args.version:
        print(f"Macal DSL Package Manager {__version__}")
        return

    if args.install:
        install_package(args.package, args.repo, libpath)
        return

    if args.uninstall:
        uninstall_package(args.package, libpath)
        return

    if args.list:
        list_packages(libpath)
        return

    if args.search:
        search_packages(args.package, args.repo)
        return

    print("No action specified. Use -h/--help for usage information.")
    print()


if __name__ == "__main__":
    main()
