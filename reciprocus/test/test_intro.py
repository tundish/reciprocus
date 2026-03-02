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

import dataclasses
from fractions import Fraction as F
from numbers import Number
import unittest

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
