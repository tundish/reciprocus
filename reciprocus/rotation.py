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

"""
See "Rotations, Quaternions, and Double Groups", Altmann, 1986.

Thanks also to:
https://danceswithcode.net/engineeringnotes/quaternions/quaternions.html
https://danceswithcode.net/engineeringnotes/quaternions/conversion_tool.html

"""

import dataclasses
import enum
from fractions import Fraction
import math
from numbers import Number

from reciprocus.coordinates import Coordinates


class Orbit(enum.Enum):
    " Reference orbital velocity "
    ANALOGUE = math.pi
    DISCRETE = 4


@dataclasses.dataclass(
    init=True, repr=True, eq=False,
    order=False, unsafe_hash=False, frozen=True,
    match_args=True, kw_only=False,
    slots=True, weakref_slot=True
)
class Rotation:
    axis: Coordinates
    turn: Fraction = 0
    spin: Number = Orbit.ANALOGUE.value

    def __iter__(self):
        "Generate Rodrigues Quaternion"
        theta = self.angle
        yield math.cos(theta / 2)
        yield from (i * math.sin(theta / 2) for i in self.axis)

    @property
    def angle(self):
        "Rotation angle"
        return 2 * self.spin * self.turn

    @property
    def roll(self):
        "Euler angle u"
        raise NotImplementedError

    @property
    def pitch(self):
        "Euler angle v"
        raise NotImplementedError

    @property
    def yaw(self):
        "Euler angle w"
        raise NotImplementedError
