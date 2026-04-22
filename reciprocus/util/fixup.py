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
import datetime
import json
import logging
import operator
from pathlib import Path
import re
import sys
import textwrap
from xml.etree import ElementTree as ET
import unittest

from math_core import LatexToMathML


class Fixer:
    comment_matcher = re.compile(r"<!--.*?-->", re.M | re.S)
    head_matcher = re.compile(r"<head.*/head>", re.M | re.S)
    image_matcher = re.compile(r"<img.*?>", re.M | re.S)
    link_matcher = re.compile(r"<link.*?>", re.M | re.S)
    page_matcher = re.compile(r'<div class="pagination".*?/div>', re.M | re.S)
    code_matcher = re.compile(r'<div class="codebox".*?/div>', re.M | re.S)
    inner_matcher = re.compile(r'<div class="inner".*?/div>', re.M | re.S)
    content_matcher = re.compile(r'<div class="content".*?/div>', re.M | re.S)
    attachment_matcher = re.compile(r'<div class="inline-attachment".*?/div>', re.M | re.S)
    blockquote_matcher = re.compile(r'<blockquote.*?/blockquote>', re.M | re.S)
    error_matcher = re.compile(r':\s+line\s+(?P<line>\d+)[, ]*column\s+(?P<column>\d+)\s*', re.M | re.S)

    class Index:
        lookup = {}
        capture = [
            re.compile(r"DFT-([\d]+)([a-z]{0,1})")
        ]

    @staticmethod
    def attach_aside(match):
        return match[0].replace("<div", "<aside").replace("</div>", "</aside>")

    @staticmethod
    def code_section(match):
        return match[0].replace("<div", "<samp").replace("</div>", "</samp>")

    @staticmethod
    def terminate_image(match):
        if "/>" not in match[0]:
            return match[0].replace(">", " />")
        return match[0]

    @staticmethod
    def undiv_blockquote(match):
        text = match[0]
        if text.count("<blockquote") > 1:
            return text
        return text.replace("<div", "<p").replace("</div>", "</p>")

    @staticmethod
    def fix_math(text: str):
        """
        For command coverage see:
        https://github.com/tmke8/math-core/issues/155
        """
        text = text.strip()
        replace = {
            r"\!": "",
            r"\abs": r"\lvert",
            r"\huge": "",
            r"\leadsto": r"\Rarr",
        }
        if text.startswith(r"\(") and text.endswith(r"\)"):
            text = text.removeprefix(r"\(").removesuffix(r"\)")
        for k, v in replace.items():
            text = text.replace(k, v)
        if text.endswith(r"\right"):
            text = f"{text})"
        return text

    def __init__(self, path: pathlib.Path, data: dict = None):
        self.logger = logging.getLogger("fixer")
        self.path = path
        self.data = data or dict()

    def __call__(self, layout: str = None):
        text = self.path.read_text()
        tree = ET.ElementTree(element=ET.Element("main"))

        if self.path.suffix == ".html":
            page_index = int(self.path.stem.partition("-")[2] or 0)
            self.logger.debug(f"Page index is {page_index}", extra=dict(path=self.path))
            text, n = Fixer.attachment_matcher.subn(Fixer.attach_aside, text)
            text, n = Fixer.code_matcher.subn(Fixer.code_section, text)
            text, n = Fixer.blockquote_matcher.subn(Fixer.undiv_blockquote, text)
            for text in Fixer.content_matcher.findall(text):
                section = self.thread_page(text)
                tree.getroot().append(section)
            yield Path(self.path.name), tree, self.data
            return

        self.data.update(json.loads(text))
        name = f"{self.path.stem}.html"
        for regex in self.Index.capture:
            match = regex.search(self.data["title"])
            if match:
                index = (int(match[1]), match[2] or "0")
                self.Index.lookup[match[0]] = (index, name)

        thread_id = self.data.get("id", 0)
        for post in self.data.get("posts"):
            text = post.get("content", "")
            # text = "\n".join(f"<p>{i}</p>" for i in filter(None, (i.strip() for i in text.split("<br>"))))
            try:
                ts = datetime.datetime.strptime(post["date"], "%a %b  %d, %Y %I:%M %p")
            except ValueError as error:
                self.logger.debug(f"Bad timestamp: {error}", extra=dict(path=self.path))
                ts = ""
            header = textwrap.dedent(f"""
            <header>
            <dl>
            <dt>User</dt><dd class="user">{post['user']}</dd>
            <dt>Time</dt><dd class="time">{ts}</dd>
            </dl>
            </header>
            """).strip()
            section = self.thread_page(f'''<section id="{post['postid']}">\n{header}\n{text}\n</section>''')
            try:
                tree.getroot().append(section)
            except TypeError:
                self.logger.debug(
                    f"No valid content for post {post['postid']}", extra=dict(path=self.path)
                )
        yield Path(name), tree, self.data

    def thread_page(self, text: str, layout: str = None):
        self.logger.debug(f"Text: {text}", extra=dict(path=self.path))
        text, n = Fixer.comment_matcher.subn("", text)
        text, n = Fixer.image_matcher.subn(Fixer.terminate_image, text)
        text = text.replace("<br>", "<br />")

        try:
            return ET.fromstring(text)
        except ET.ParseError as error:
            match = Fixer.error_matcher.search(format(error))
            line_nr = int(match["line"]) - 1
            pos = int(match["column"]) - 1
            line = text.splitlines()[line_nr]
            a = max(0, pos - 36)
            b = min(pos + 8, len(line))
            self.logger.warning(f"{error}", extra=dict(path=self.path))
            self.logger.debug(f"{line[a: b]}", extra=dict(path=self.path))
            self.logger.debug(" " * 36 + "^", extra=dict(path=self.path))

    def to_html(self, tree: ET.ElementTree, metadata: dict = None):
        converter = LatexToMathML(annotation=True)
        prior = root = tree.getroot()
        parents = {c: p for p in tree.iter() for c in p}
        for elem in list(tree.iter()):
            if elem.tag == "img":
                formula = self.fix_math(elem.attrib.get("alt", ""))
                if formula.lower() != "image":
                    self.logger.debug(f"Converting formula {formula}", extra=dict(path=self.path))
                    mathml = converter.convert_with_local_counter(formula, displaystyle=False)
                    insert = ET.fromstring(mathml)
                    prior.append(insert)
                    parent = parents[elem]
                    parent.remove(elem)
                    prior = insert
            else:
                prior = elem

        breadcrumbs = " ".join([f"<dd>{i}</dd>" for i in metadata["path"]])
        yield textwrap.dedent(f"""
            <!doctype html>
            <html lang="en">
            <head>
            <title>{metadata['title']}</title>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <meta http-equiv="X-UA-Compatible" content="ie=edge" />
            <link rel="alternate" href="{metadata['url']}">
            </head>
            <body>
            <nav><dl>{breadcrumbs}</dl></nav>
            <h1>{metadata['title']}</h1>
        """).strip()

        yield ET.tostring(
            tree.getroot(), encoding="unicode",
            xml_declaration=False, default_namespace=None,
            method="html", short_empty_elements=False
        )

        yield textwrap.dedent("""
            </body>
            </html>
        """).strip()


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
        What Wikipedia explicitly <em class="text-italics">doesn't</em> tell us is
        <span style="font-size: 200%; line-height: normal"><strong class="text-strong">e = MC²</strong></span>
        <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fuploads-ssl.webflow.com%2F5c55f4835309587c21460b5f%2F5e211638d2126f2ccbbc1a13_8de37575-p-800.png&amp;f=1&amp;nofb=1" class="postimage" alt="Image">
        ...only to find in the "end"...<br /> <br /> 1 = Φ(π/4)²<br /> <br /> ...they failed to ask the right <em class="text-italics">question(s)</em>.</div>
        """
        text, n = Fixer.image_matcher.subn(Fixer.terminate_image, text)
        root = ET.fromstring(text)
        self.assertIsInstance(root, ET.Element)

    def test_fix_math(self):
        converter = LatexToMathML()
        for text in [
            r"\lambda" , r"\sigma(\lambda)" , r"\mathbb{R}^{3}_{S}" , r"\mathbb{R}^{3}_{T}" ,
            r"\(\mathbb{R}^{3}_{T}\)",
            r"\bigl\| R_{S}(\lambda) \bigr\|^{2} + \bigl\| R_{T}(\lambda) \bigr\|^{2} = C^{2}\!\bigl(\sigma(\lambda)\bigr)",
            r"\dot{\Theta}(\lambda) = \left(\dot{\theta}^1(\lambda),\ \dot{\theta}^2(\lambda),\ \dot{\theta}^3(\lambda)\right",
        ]:
            with self.subTest(text=text):
                formula = Fixer.fix_math(text)
                self.assertTrue(formula)
                mathml = converter.convert_with_local_counter(formula, displaystyle=False)
                self.assertTrue(mathml)


def main(args):
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=level, style="{",
        format="{asctime}|{levelname:>8}| {name:<16}| {path!s:<36}| {message}",
    )
    logger = logging.getLogger("scraper")
    args.output.mkdir(parents=True, exist_ok=True)

    def by_the_numbers(path):
        try:
            return int(path.stem)
        except ValueError:
            return path.name

    pages = {}
    for path in sorted(args.paths, key=by_the_numbers):
        logger.info(f"Fixing file", extra=dict(path=path))
        fix = Fixer(path)
        for name, tree, metadata in fix(layout=args.layout):
            try:
                html5 = "\n".join(fix.to_html(tree, metadata))
            except (AttributeError, ValueError) as error:
                logger.error(f"Not fixed. {error}", extra=dict(path=path))
            except Exception as error:
                logger.error(error, extra=dict(path=path), exc_info=True)
            else:
                pages[name] = (path, metadata["title"], html5)
                logger.info(f"Page created ({len(html5)} chars)", extra=dict(path=path))

    lookup = {Path(v): k for k, (i, v) in sorted(Fixer.Index.lookup.items(), key=operator.itemgetter(1))}
    for n, (name, (path, title, html5)) in enumerate(pages.items()):
        pos = list(lookup).index(name) - 1 if name in lookup else -1
        if n > 0 or pos >= 0:
            target = sorted(Fixer.Index.lookup.values())[pos][1] if pos >= 0 else list(pages)[n - 1]
            html5 = html5.replace("</head>", f'<link rel="prev" href="{target}">\n</head>')
            html5 = html5.replace("</dl></nav>", f'<dt>Back</dt><dd class="back"><a href="{target}">{target}</a></dd></dl></nav>')

        pos = list(lookup).index(name) + 1 if name in lookup else -1
        if n < len(pages) - 1 or 0 <= pos < len(lookup) - 1:
            target = sorted(Fixer.Index.lookup.values())[pos][1] if 0 <= pos < len(lookup) - 1 else list(pages)[n + 1]
            html5 = html5.replace("</head>", f'<link rel="next" href="{target}">\n</head>')
            html5 = html5.replace("</dl></nav>", f'<dt>Next</dt><dd class="next"><a href="{target}">{target}</a></dd></dl></nav>')

        for k, (i, v) in Fixer.Index.lookup.items():
            html5 = html5.replace(f"{k} ", f'<a href="{v}">{k}</a> ')
        output = args.output / name
        output.write_text(html5, encoding="utf8")
        logger.info(f"Written to {output}", extra=dict(path=path))

    logger.info(f"Completed actions", extra=dict(path=""))
    return 0


def parser():
    default_path = Path.cwd().joinpath("output").resolve()
    rv = argparse.ArgumentParser(usage=__doc__, fromfile_prefix_chars="=")
    rv.add_argument("paths", nargs="+", type=Path, help="Specify file paths")
    rv.add_argument("-O", "--output", type=Path, default=default_path, help=f"Specify output directory [{default_path}]")
    rv.add_argument("--layout", default="multi", choices = ["multi", "single"], help=f"Select page layout")
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
