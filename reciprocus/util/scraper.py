#! /usr/bin/env python3
# encoding: UTF-8

# This file is part of reciprocus.

# Reciprocus is free software: You can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# Reciprocus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the
# GNU General Public License along with reciprocus.
# If not, see <https://www.gnu.org/licenses/>.


import argparse
import logging
from pathlib import Path
import re
import sys
from xml.etree import ElementTree as ET
import unittest


class RegexTests(unittest.TestCase):

    def test_match_comments(self):
        text = """
            <!--[if lte IE 9]> <link href="./styles/prosilver/theme/tweaks.css?assets_version=29" rel="stylesheet">
            <![endif]-->
        """
        self.fail(text)


def reformat(path):
    text = path.read_text()
    text = text.removeprefix("<!DOCTYPE html>")
    tree = ET.fromstring(text)
    return tree.getroot()


def main(args):
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=level, style="{",
    )
    logger = logging.getLogger("scraper")
    args.output.mkdir(parents=True, exist_ok=True)

    for path in args.paths:
        logger.info(f"{path}", extra=dict())
        root = reformat(path)

    logger.info(f"Completed actions", extra=dict())
    return 0


def parser():
    default_path = Path.cwd().joinpath("output").resolve()
    rv = argparse.ArgumentParser(usage=__doc__, fromfile_prefix_chars="=")
    rv.add_argument("paths", nargs="+", type=Path, help="Specify file paths")
    rv.add_argument("-O", "--output", type=Path, default=default_path, help=f"Specify output directory [{default_path}]")
    rv.add_argument("--debug", action="store_true", default=False, help=f"Display debug logs")
    rv.add_argument("--test", action="store_true", default=False, help=f"Run unit tests")
    rv.convert_arg_line_to_args = lambda x: x.split()
    return rv


def run():
    p = parser()
    args, res = p.parse_known_args()
    if args.test:
        sys.argv[1:] = []
        unittest.main()
    else:
        rv = main(args)
        sys.exit(rv)


if __name__ == "__main__":
    run()
