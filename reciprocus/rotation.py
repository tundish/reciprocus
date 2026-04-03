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

from collections.abc import Sequence
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
    norm: tuple = dataclasses.field(init=False)

    @classmethod
    def from_rodrigues_parameters(cls, q: Sequence[Number], spin: Number = Orbit.ANALOGUE.value, places: int = 12):
        assert len(q) == 4
        theta = 2 * math.acos(q[0])
        try:
            axis = Coordinates(*(i / math.sin(theta / 2) for i in q[1:]))
        except ZeroDivisionError:
            axis = Coordinates(1, 0, 0)  # Default axis for identity quaternion
        turn = Fraction(theta / spin / 2).limit_denominator(10 ** places)
        return cls(axis, turn=turn, spin=spin)

    def __post_init__(self):
        object.__setattr__(self, "norm", tuple(self))

    def __iter__(self):
        try:
            yield from self.norm
        except AttributeError:
            # Generate Rodrigues Quaternion
            theta = self.angle
            yield math.cos(theta / 2)
            yield from (i * math.sin(theta / 2) for i in self.axis)

    def __getitem__(self, key):
        return self.norm[key]

    def __len__(self):
        return len(self.norm)

    @property
    def angle(self):
        "Rotation angle"
        rv = 2 * self.spin * self.turn
        if not 0 <= rv <= self.spin:
            raise ValueError(f"{rv} is outside range [0, {self.spin}]")
        else:
            return rv

    @property
    def roll(self):
        "Euler angle u"
        q = tuple(self)
        a = 2 * (q[0] * q[1] + q[2] * q[3])
        b = q[0] ** 2 - q[1] ** 2 - q[2] ** 2 + q[3] ** 2
        return math.atan2(a, b)

    @property
    def pitch(self):
        "Euler angle v"
        q = tuple(self)
        return math.asin(2 * (q[0] * q[2] - q[1] * q[3]))

    @property
    def yaw(self):
        "Euler angle w"
        q = tuple(self)
        a = 2 * (q[0] * q[3] + q[1] * q[2])
        b = q[0] ** 2 + q[1] ** 2 - q[2] ** 2 - q[3] ** 2
        return math.atan2(a, b)

    @property
    def matrix(self):
        "Rotation matrix"
        q = tuple(self)
        return [
            [
             q[0] ** 2 + q[1] ** 2 - q[2] ** 2 - q[3] ** 2,
             2 * q[1] * q[2] - 2 * q[0] * q[3],
             2 * q[1] * q[3] + 2 * q[0] * q[2],
            ],
            [
             2 * q[1] * q[2] + 2 * q[0] * q[3],
             q[0] ** 2 - q[1] ** 2 + q[2] ** 2 - q[3] ** 2,
             2 * q[2] * q[3] - 2 * q[0] * q[1],
            ],
            [
             2 * q[1] * q[3] - 2 * q[0] * q[2],
             2 * q[2] * q[3] + 2 * q[0] * q[1],
             q[0] ** 2 - q[1] ** 2 - q[2] ** 2 + q[3] ** 2,
            ],
        ]

    def __invert__(self):
        q = tuple(self)
        return self.from_rodrigues_parameters([q[0], -q[1], -q[2], -q[3]], spin=self.spin)

    def __matmul__(self, x):
        r = tuple(self)
        s = tuple(x)
        return self.from_rodrigues_parameters(
            [
                r[0] * s[0] - r[1] * s[1] - r[2] * s[2] - r[3] * s[3],
                r[0] * s[1] + r[1] * s[0] - r[2] * s[3] + r[3] * s[2],
                r[0] * s[2] + r[1] * s[3] + r[2] * s[0] - r[3] * s[1],
                r[0] * s[3] - r[1] * s[2] + r[2] * s[1] + r[3] * s[0],
            ],
            spin=self.spin
        )
