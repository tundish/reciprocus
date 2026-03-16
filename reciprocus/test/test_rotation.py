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


class QuaternionTests(unittest.TestCase):

    @unittest.skip("Dev")
    def test_generic_quat_matrix(self):
        x = Q.asarray([[3.0, 4, 0, 0], [5, 12, 0, 0]])
        r = Rotation.from_quat(x)
        expected_quat = x / Q.asarray([[5.0], [13.0]])
        xp_assert_close(r.as_quat(), expected_quat)

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

    def test_quaternion(self):
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
        self.assertEqual(R(C(0, 0, 1), F(1, 12)).yaw, math.radians(30))
