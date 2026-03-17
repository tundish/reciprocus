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

from fractions import Fraction as F
import math
import unittest

from reciprocus.coordinates import Coordinates as C
from reciprocus.rotation import Rotation as R


class RotationTests(unittest.TestCase):

    def test_angle_range(self):
        axis = C(1, 1, 1)
        for a, r in [
            (-0.002 * math.pi, R(axis, turn=0 - 0.001)),
            (2.002 * math.pi, R(axis, turn=1.001)),
        ]:
            with self.subTest(r=r):
                with self.assertRaises(ValueError) as context:
                    r.angle
                self.assertIn(str(a), format(context.exception))

    def test_angle(self):
        axis = C(1, 1, 1)
        for a, r in [
            (0, R(axis)),
            (0, R(axis, turn=0)),
            (math.pi, R(axis, turn=0.5)),
        ]:
            with self.subTest(r=r):
                self.assertEqual(r.angle, a)

    def test_from_quaternion(self):
        for axis in (C(0, 0, 1), C(0, 1, 0), C(0, 0, 1)):
            for turn in (0, F(1, 12), F(1, 4), F(1, 3), F(1, 2)):
                r = R(axis, turn)
                with self.subTest(r=r):
                    x = R.from_rodrigues_parameters(C(*r))
                    if turn:
                        self.assertEqual([round(i, 12) for i in x.axis], [round(i, 12) for i in r.axis])
                    else:
                        self.assertEqual(x.axis, (1, 0, 0))
                    self.assertEqual(x.turn, r.turn, math.degrees(x.angle))
                    self.assertEqual(x.spin, r.spin)
                    self.assertEqual(x.angle, r.angle)

    def test_sequence(self):
        data = [
            (R(C(0, 0, 1), F(1, 12)), (0.9659, 0, 0, 0.2588)),
            (R(C(0, 1, 0), F(1, 12)), (0.9659, 0, 0.2588, 0)),
            (R(C(1, 0, 0), F(1, 12)), (0.9659, 0.2588, 0, 0)),
            (R(C(0, 0, -1), F(1, 12)), (0.9659, 0, 0, -0.2588)),
            (R(C(0, -1, 0), F(1, 12)), (0.9659, 0, -0.2588, 0)),
            (R(C(-1, 0, 0), F(1, 12)), (0.9659, -0.2588, 0, 0)),
        ]
        for r, x in data:
            with self.subTest(r=r, x=x):
                for a, b in zip(r, x):
                    self.assertAlmostEqual(a, b, places=4)

    def test_euler(self):
        self.assertEqual(R(C(1, 0, 0), F(1, 12)).roll, math.radians(30))
        self.assertEqual(R(C(0, 1, 0), F(1, 12)).pitch, math.radians(30))
        self.assertEqual(R(C(0, 0, 1), F(1, 12)).yaw, math.radians(30))

        self.assertEqual(R(C(0, 1, 0), F(1, 4)).roll, 0)
        self.assertEqual(R(C(0, 1, 0), F(1, 4)).pitch, math.radians(90))
        self.assertEqual(R(C(0, 1, 0), F(1, 4)).yaw, 0)

    def test_matrix(self):
        m = R(C(1, 0, 0), F(1, 12)).matrix
        self.assertEqual(m[0], [1, 0, 0])
        self.assertEqual([round(i, 3) for i in m[1]], [0, 0.866, -0.5])
        self.assertEqual([round(i, 3) for i in m[2]], [0, 0.5, 0.866])

        m = R(C(0, 1, 0), F(1, 12)).matrix
        self.assertEqual([round(i, 3) for i in m[0]], [0.866, 0, 0.5])
        self.assertEqual(m[1], [0, 1, 0])
        self.assertEqual([round(i, 3) for i in m[2]], [-0.5, 0, 0.866])

        m = R(C(0, 0, 1), F(1, 12)).matrix
        self.assertEqual([round(i, 3) for i in m[0]], [0.866, -0.5, 0])
        self.assertEqual([round(i, 3) for i in m[1]], [0.5, 0.866, 0])
        self.assertEqual(m[2], [0, 0, 1])
