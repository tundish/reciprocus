#!/usr/bin/env python
#   encoding: utf-8

# Copyright (C) 2026 D E Haynes
# This file is part of reciprocus.

# Reciprocus is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Reciprocus is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with reciprocus.
# If not, see <https://www.gnu.org/licenses/>.

from collections.abc import Callable
import dataclasses
from fractions import Fraction as F
from numbers import Number
import unittest

from reciprocus.chain import Chain
from reciprocus.compat import ArrayInterface

# TODO Cross-ratio invariant in projective geometry.

@dataclasses.dataclass
class Result:
    value: numbers.Number = None
    terms: list = dataclasses.field(default_factory=list)
    units: list = dataclasses.field(default_factory=list)


def conjugate(val: Number):
    "N units of motion in time are equivalent to minus 1 / N units of motion in space."
    return - 1 / val


class ScalarTests(unittest.TestCase):

    def test_defs(self):
        c = complex(1.8)
        print(c.conjugate())
        print(conjugate(c))


class InterfaceTests(unittest.TestCase):
    """
    Test conformance with Python array API.
    See https://data-apis.org/array-api/latest/index.html

    """

    def test_array_namespace(self):
        self.assertIsInstance(getattr(ArrayInterface(), "__array_namespace__", None), Callable)
        xp = Chain().__array_namespace__(api_version="2025.12")
