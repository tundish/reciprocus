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
Implements conformity with Python array API.
See https://data-apis.org/array-api/latest/index.html
"""

from collections import namedtuple
import enum


C = namedtuple("Constraint", ["type", "code", "min", "max"], defaults = [None, None])


class DataType(enum.Enum):
    BOOL        =  C(bool, "?", False, True)
    INT8        =  C(int, "b", -128, +127)
    INT16       =  C(int, "h", -32767, +32767)
    INT32       =  C(int, "i", -2147483647, +2147483647)
    INT64       =  C(int, "q", -9223372036854775807, +9223372036854775807)
    UINT8       =  C(int, "B", 0, 255)
    UINT16      =  C(int, "H", 0, 65535)
    UINT32      =  C(int, "I", 0, 4294967295)
    UINT64      =  C(int, "Q", 0, 18446744073709551615)
    FLOAT32     =  C(float, "f")
    FLOAT64     =  C(float, "d")
    COMPLEX64   =  C(float, "F")
    COMPLEX128  =  C(float, "D")


class DeviceType(enum.StrEnum):
    CPU = enum.auto()
    GPU = enum.auto()


class DLPackDeviceType(enum.IntEnum):
    CPU = 1
    CUDA = 2
    CPU_PINNED = 3
    OPENCL = 4
    VULKAN = 7
    METAL = 8
    VPI = 9
    ROCM = 10
    CUDA_MANAGED = 13
    ONE_API = 14


class ArrayInterface:

    # https://data-apis.org/array-api/latest/API_specification/array_object.html#arithmetic-operators

    def __pos__(self):
        """
        +x

        operator.pos(x)

        """
        raise NotImplementedError

    def __neg__(self):
        """
        -x

        operator.neg(x)

        """
        raise NotImplementedError

    def __add__(self, x):
        """
        x1 + x2

        operator.add(x1, x2)

        """
        raise NotImplementedError

    def __sub__(self, x):
        """
        x1 - x2

        operator.sub(x1, x2)

        """
        raise NotImplementedError

    def __mul__(self, x):
        """
        x1 * x2

        operator.mul(x1, x2)

        """
        raise NotImplementedError

    def __truediv__(self, x):
        """
        x1 / x2

        operator.truediv(x1, x2)

        """
        raise NotImplementedError

    def __floordiv__(self, x):
        """
        x1 // x2

        operator.floordiv(x1, x2)

        """
        raise NotImplementedError

    def __mod__(self, x):
        """
        x1 % x2

        operator.mod(x1, x2)

        """
        raise NotImplementedError

    def __pow__(self, x):
        """
        x1 ** x2

        operator.pow(x1, x2)

        """
        raise NotImplementedError

    # In-place arithmetic

    def __iadd__(self, x):
        """
        x1 += x2

        operator.iadd(x1, x2)

        """
        raise NotImplementedError

    def __isub__(self, x):
        """
        x1 -= x2

        operator.isub(x1, x2)

        """
        raise NotImplementedError

    def __imul__(self, x):
        """
        x1 *= x2

        operator.imul(x1, x2)

        """
        raise NotImplementedError

    def __itruediv__(self, x):
        """
        x1 /= x2

        operator.itruediv(x1, x2)

        """
        raise NotImplementedError

    def __ifloordiv__(self, x):
        """
        x1 //= x2

        operator.ifloordiv(x1, x2)

        """
        raise NotImplementedError

    def __imod__(self, x):
        """
        x1 %= x2

        operator.imod(x1, x2)

        """
        raise NotImplementedError

    def __ipow__(self, x):
        """
        x1 **= x2

        operator.ipow(x1, x2)

        """
        raise NotImplementedError

    # Reflected arithmetic operators

    def __radd__(self, x):
        """ x2 + x1 """
        raise NotImplementedError

    def __rsub__(self, x):
        """ x1 - x2 """
        raise NotImplementedError

    def __rmul__(self, x):
        """ x2 * x1 """
        raise NotImplementedError

    def __rtruediv__(self, x):
        """ x2 / x1 """
        raise NotImplementedError

    def __rfloordiv__(self, x):
        """ x2 // x1 """
        raise NotImplementedError

    def __rmod__(self, x):
        """ x2 % x1 """
        raise NotImplementedError

    def __rpow__(self, x):
        """ x2 ** x1 """
        raise NotImplementedError

    # https://data-apis.org/array-api/latest/API_specification/array_object.html#array-operators

    def __matmul__(self, x):
        """
        x1 @ x2

        operator.matmul(x1, x2)

        """
        raise NotImplementedError

    def __imatmul__(self, x):
        """
        x1 @= x2

        operator.imatmul(x1, x2)

        """
        raise NotImplementedError

    def __rmatmul__(self, x):
        """ x2 @ x1 """
        raise NotImplementedError

    # https://data-apis.org/array-api/latest/API_specification/array_object.html#bitwise-operators

    def __invert__(self, x):
        """
        x1 ~ x2

        operator.inv(x1, x2)

        """
        raise NotImplementedError

    def __and__(self, x):
        """
        x1 & x2

        operator.and(x1, x2)

        """
        raise NotImplementedError

    def __or__(self, x):
        """
        x1 | x2

        operator.or(x1, x2)

        """
        raise NotImplementedError

    def __xor__(self, x):
        """
        x1 ^ x2

        operator.xor(x1, x2)

        """
        raise NotImplementedError

    def __lshift__(self, x):
        """
        x1 << x2

        operator.lshift(x1, x2)

        """
        raise NotImplementedError

    def __rshift__(self, x):
        """
        x1 >> x2

        operator.rshift(x1, x2)

        """
        raise NotImplementedError

    # In-place bitwise

    def __iand__(self, x):
        """
        x1 &= x2

        operator.iand(x1, x2)

        """
        raise NotImplementedError

    def __ior__(self, x):
        """
        x1 |= x2

        operator.ior(x1, x2)

        """
        raise NotImplementedError

    def __ixor__(self, x):
        """
        x1 ^= x2

        operator.ixor(x1, x2)

        """
        raise NotImplementedError

    def __ilshift__(self, x):
        """
        x1 <<= x2

        operator.ilshift(x1, x2)

        """
        raise NotImplementedError

    def __irshift__(self, x):
        """
        x1 >>= x2

        operator.irshift(x1, x2)

        """
        raise NotImplementedError

    # Reflected bitwise

    def __rand__(self, x):
        """ x2 & x1 """
        raise NotImplementedError

    def __ror__(self, x):
        """ x2 | x1 """
        raise NotImplementedError

    def __rxor__(self, x):
        """ x2 ^ x1 """
        raise NotImplementedError

    def __rlshift__(self, x):
        """ x2 << x1 """
        raise NotImplementedError

    def __rrshift__(self, x):
        """ x2 >> x1 """
        raise NotImplementedError

    # https://data-apis.org/array-api/latest/API_specification/array_object.html#comparison-operators

    def __lt__(self, x):
        """
        x1 < x2

        operator.lt(x1, x2)

        """
        raise NotImplementedError

    def __le__(self, x):
        """
        x1 <= x2

        operator.le(x1, x2)

        """
        raise NotImplementedError

    def __gt__(self, x):
        """
        x1 > x2

        operator.gt(x1, x2)

        """
        raise NotImplementedError

    def __ge__(self, x):
        """
        x1 >= x2

        operator.ge(x1, x2)

        """
        raise NotImplementedError

    def __eq__(self, x):
        """
        x1 == x2

        operator.eq(x1, x2)

        """
        raise NotImplementedError

    def __neq__(self, x):
        """
        x1 != x2

        operator.neq(x1, x2)

        """
        raise NotImplementedError

    # https://data-apis.org/array-api/latest/API_specification/array_object.html#attributes

    @property
    def dtype(self):
        """ Data type of the array elements. """
        raise NotImplementedError

    @property
    def device(self):
        """ Hardware device the array data resides on. """
        raise NotImplementedError

    @property
    def mT(self):
        """ Transpose of a matrix (or a stack of matrices). """
        raise NotImplementedError

    @property
    def ndim(self):
        """ Number of array dimensions (axes). """
        raise NotImplementedError

    @property
    def shape(self):
        """ Array dimensions. """
        raise NotImplementedError

    @property
    def size(self):
        """ Number of elements in an array. """
        raise NotImplementedError

    @property
    def T(self):
        """ Transpose of the array. """
        raise NotImplementedError

    # https://data-apis.org/array-api/latest/API_specification/array_object.html#methods

    def __abs__(self):
        """ Calculates the absolute value for each element of an array instance.  """
        raise NotImplementedError

    def __array_namespace__(self, *, api_version=None) -> dict:
        """ Returns an object that has all the array API functions on it. """
        raise NotImplementedError

    def __bool__(self) -> bool:
        """ Converts a zero-dimensional array to a Python bool object. """
        raise NotImplementedError

    def __complex__(self) -> complex:
        """ Converts a zero-dimensional array to a Python complex object. """
        raise NotImplementedError

    def __dlpack__(
        self,
        *,
        stream: int | object | None = None,
        max_version: tuple[int, int] | None = None,
        dl_device: tuple[enum.Enum, int] | None = None,
        copy: bool | None = None
    ) -> "PyCapsule":
        """ Exports the array for consumption by from_dlpack() as a DLPack capsule. """
        raise NotImplementedError

    def __dlpack_device__(self) -> tuple[enum.Enum, int]:
        """ Returns device type and device ID in DLPack format. """
        raise NotImplementedError

    def __float__(self) -> float:
        """ Converts a zero-dimensional array to a Python float object. """
        raise NotImplementedError

    def __index__(self) -> int:
        """ Converts a zero-dimensional array to a Python int object. """
        raise NotImplementedError

    def __int__(self) -> int:
        """ Converts a zero-dimensional array to a Python int object. """
        raise NotImplementedError

    def to_device(self, device: DeviceType, /, *, stream: int | object | None = None) -> ArrayInterface:
        """ Copy the array from the device on which it currently resides to the specified device. """
        raise NotImplementedError
