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
import sys


def main(args):
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=level, style="{",
    )
    logger = logging.getLogger("scraper")
    args.output.mkdir(parents=True, exist_ok=True)

    logger.debug(f"{args.paths}", extra=dict())
    logger.info(f"Completed actions", extra=dict())
    return 0


def parser():
    default_path = Path.cwd().joinpath("output").resolve()
    rv = argparse.ArgumentParser(usage=__doc__, fromfile_prefix_chars="=")
    rv.add_argument("paths", nargs="+", type=Path, help="Specify file paths")
    rv.add_argument("-O", "--output", type=Path, default=default_path, help=f"Specify output directory [{default_path}]")
    rv.add_argument("--debug", action="store_true", default=False, help=f"Display debug logs")
    rv.convert_arg_line_to_args = lambda x: x.split()
    return rv


def run():
    p = parser()
    args, res = p.parse_known_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
