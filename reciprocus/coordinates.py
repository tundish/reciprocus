#! /usr/bin/env python3
# encoding: UTF-8

# This file is part of Plotlines.

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

from __future__ import annotations  # Until Python 3.14 is everywhere

import math
from numbers import Number


class Coordinates(tuple):

    def __new__(cls, *args, coerce=None):
        if coerce:
            args = [coerce(i) for i in args]
        return tuple.__new__(cls, args)

    def __abs__(self):
        return math.hypot(*self)

    def __getnewargs__(self):
        return self

    def __add__(self, other):
        return self.__class__(*[a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        return self.__class__(*[a - b for a, b in zip(self, other)])

    def __mul__(self, other):
        return self.__class__(*[other * i for i in self])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        return self.__class__(*[i // other for i in self])

    def __truediv__(self, other):
        return self.__class__(*[i / other for i in self])

    def __repr__(self):
        return "< {0} >".format(", ".join(f"{i}" for i in self))

    @staticmethod
    def intercept(origin: Coordinates, transit: Coordinates, point: Coordinates) -> Coordinates:
        "Find the normal intercept from a point to a line between origin and transit"
        try:
            shadow = (point - origin).unity.dot((transit - origin).unity) * abs(point - origin)
            return origin + (transit - origin) * shadow / abs(transit - origin)
        except TypeError:
            return None

    @property
    def unity(self):
        try:
            return self / abs(self)
        except ZeroDivisionError:
            return self

    def dot(self, other) -> Number:
        return math.sumprod(self, other)

    def cross(self, other) -> Coordinates:
        try:
            i = self[1] * other[2] - self[2] * other[1]
            j = self[2] * other[0] - self[0] * other[2]
            k = self[0] * other[1] - self[1] * other[0]
            return Coordinates(i, j, k)
        except IndexError:
            # Works in 3D only.
            raise NotImplementedError
