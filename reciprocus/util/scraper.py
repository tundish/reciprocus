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
    blockquote_matcher = re.compile(r'<blockquote.*?/blockquote>', re.M | re.S)
    error_matcher = re.compile(r':\s+line\s+(?P<line>\d+)[, ]*column\s+(?P<column>\d+)\s*', re.M | re.S)

    @staticmethod
    def attach_aside(match):
        return match[0].replace("<div", "<aside").replace("</div>", "</aside>")

    @staticmethod
    def undiv_blockquote(match):
        return match[0].replace("<div", "<p").replace("</div>", "</p>")

    def __init__(self):
        self.logger = logging.getLogger("fixer")

    def __call__(self, path):
        text = path.read_text()
        text, n = Fixer.comment_matcher.subn("", text)
        text = text.replace("<br>", "<br />")
        text, n = Fixer.attachment_matcher.subn(Fixer.attach_aside, text)
        text, n = Fixer.blockquote_matcher.subn(Fixer.undiv_blockquote, text)
        match = Fixer.content_matcher.search(text)
        self.logger.debug(f"{match=}", extra=dict(path=path))
        try:
            text = match[0]
            return ET.fromstring(text)
        except TypeError:
            self.logger.info(f"No content", extra=dict(path=path))
        except ET.ParseError as error:
            match = Fixer.error_matcher.search(format(error))
            line = int(match["line"]) - 1
            pos = int(match["column"]) - 1
            snip = text.splitlines()[line]
            self.logger.warning(f"{error}", extra=dict(path=path))
            print(text)


class FixerTests(unittest.TestCase):

    def test_parse_pos(self):
        text = "mismatched tag: line 1, column 1561"
        match = Fixer.error_matcher.search(text)
        self.assertTrue(match)
        self.assertEqual(match["line"], "1")
        self.assertEqual(match["column"], "1561")

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

    def test_content_selectors(self):
        text = """
        <div class="content">Wikipedia tells us,<br />
        <blockquote class="uncited">
        <p>...in 1968, during the Vietnam War, Kaku, who was about to be drafted, joined the United States Army, remaining until 1970. He completed his basic training at Fort Benning, Georgia, and advanced infantry training at Fort Lewis, Washington.[7] However, he was never deployed to Vietnam.
        </p></blockquote>
        <a href="https://en.wikipedia.org/wiki/Michio_Kaku" class="postlink">https://en.wikipedia.org/wiki/Michio_Kaku</a>
        <br /> <br />
        What Wikipedia explicitly <em class="text-italics">doesn't</em>
        tell us is <strong class="text-strong">e = MC²</strong></span><br /> <br />r
        <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fuploads-ssl.webflow.com%2F5c55f4835309587c21460b5f%2F5e211638d2126f2ccbbc1a13_8de37575-p-800.png&amp;f=1&amp;nofb=1" class="postimage" alt="Image">
        ...only to find in the "end"...<br /> <br /> 1 = Φ(π/4)²<br /> <br /> ...they failed to ask the right <em class="text-italics">question(s)</em>.</div>
        """
        root = ET.fromstring(text)
        self.assertIsInstance(root, ET.Element)


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
