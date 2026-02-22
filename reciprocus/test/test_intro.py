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
