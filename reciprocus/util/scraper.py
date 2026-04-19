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


class Fixer:
    comment_matcher = re.compile(r"<!--.*?-->", re.M | re.S)
    head_matcher = re.compile(r"<head.*/head>", re.M | re.S)
    link_matcher = re.compile(r"<link.*?>", re.M | re.S)
    page_matcher = re.compile(r'<div class="pagination".*?/div>', re.M | re.S)
    inner_matcher = re.compile(r'<div class="inner".*?/div>', re.M | re.S)
    content_matcher = re.compile(r'<div class="content".*?/div>', re.M | re.S)
    attachment_matcher = re.compile(r'<div class="inline-attachment".*?/div>', re.M | re.S)

    @staticmethod
    def attach_aside(match):
        return match[0].replace("<div", "<aside").replace("</div>", "</aside>")

    def __init__(self):
        self.logger = logging.getLogger("fixer")

    def __call__(self, path):
        text = path.read_text()
        text, n = Fixer.comment_matcher.subn("", text)
        text = text.replace("<br>", "<br />")
        text, n = Fixer.attachment_matcher.subn(Fixer.attach_aside, text)
        match = Fixer.content_matcher.search(text)
        self.logger.debug(f"{match=}", extra=dict(path=path))
        try:
            text = match[0]
            return ET.fromstring(text)
        except TypeError:
            self.logger.info(f"No content", extra=dict(path=path))
        except ET.ParseError as error:
            pos = int(format(error).split()[-1])
            a, b = max(0, pos - 64), min(pos + 12, len(text))
            self.logger.warning(f"XML error near {text[a: b]}", extra=dict(path=path))
            self.logger.warning(f"Pos {pos:08d}:    " + " " * 57 + "^", extra=dict(path=path))
            print(text)


class FixerTests(unittest.TestCase):

    def test_match_links(self):
        text = """
            <link rel="alternate" type="application/atom+xml" title="Feed - Topic - Rotational Vibration"
            href="/phpBB3/feed/topic/106"> <link rel="canonical"
            href="https://reciprocal.systems/phpBB3/viewtopic.php?t=106&amp;start=10">
        """
        links = Fixer.link_matcher.findall(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(" ".join(links), text.strip())

    def test_match_comments(self):
        text = """
            <!--[if lte IE 9]> <link href="./styles/prosilver/theme/tweaks.css?assets_version=29" rel="stylesheet">
            <![endif]-->
        """
        m = Fixer.comment_matcher.search(text)
        self.assertTrue(m)
        self.assertEqual(m[0], text.strip())

    def test_match_attachments(self):
        text = """
            <div class="inline-attachment"> <dl class="file"> <dt class="attach-image">
            <img src="./download/file.php?id=978" class="postimage" alt="invsqrlw.png"
            onclick="viewableArea(this);" /></dt> <dd>invsqrlw.png (133.56 KiB) Viewed 51840 times</dd> </dl>
            </div>
        """
        rv, n = Fixer.attachment_matcher.subn(Fixer.attach_aside, text)
        self.assertEqual(n, 1)
        self.assertEqual(rv.strip(), text.strip().replace("div", "aside"))



def main(args):
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=level, style="{",
        format="{asctime}|{levelname:>8}| {name:<16}| {path!s:<36}| {message}",
    )
    logger = logging.getLogger("scraper")
    args.output.mkdir(parents=True, exist_ok=True)

    fixer = Fixer()
    for path in args.paths:
        logger.info(f"Fixing file", extra=dict(path=path))
        root = fixer(path)

    logger.info(f"Completed actions", extra=dict(path=""))
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
