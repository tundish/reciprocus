#! /usr/bin/env python3
# encoding: UTF-8

# This file is part of Reciprocus.

# Reciprocus is free software: You can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# Reciprocus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the
# GNU General Public License along with Reciprocus.
# If not, see <https://www.gnu.org/licenses/>.

import argparse
import datetime
import sys


def main(args):
    ts = datetime.datetime.now(tz=datetime.timezone.utc)
    print(ts)
    return 0


def parser():
    rv = argparse.ArgumentParser(usage=__doc__, fromfile_prefix_chars="=")
    rv.convert_arg_line_to_args = lambda x: x.split()
    return rv


def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)


if __name__ == "__main__":
    run()
