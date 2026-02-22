import dataclasses
from fractions import Fraction as F
import numbers
import unittest


@dataclasses.dataclass
class Result:
    value: numbers.Number = None
    terms: list = dataclasses.field(default_factory=list)
    units: list = dataclasses.field(default_factory=list)


class ScalarTests(unittest.TestCase):

    def test_defs(self):
        self.fail()
