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
Implements conformance with Python array API.
See https://data-apis.org/array-api/latest/index.html
"""

"""
Data Types
==========

bool
	

Boolean (True or False).

int8
	

An 8-bit signed integer whose values exist on the interval [-128, +127].

int16
	

A 16-bit signed integer whose values exist on the interval [−32,767, +32,767].

int32
	

A 32-bit signed integer whose values exist on the interval [−2,147,483,647, +2,147,483,647].

int64
	

A 64-bit signed integer whose values exist on the interval [−9,223,372,036,854,775,807, +9,223,372,036,854,775,807].

uint8
	

An 8-bit unsigned integer whose values exist on the interval [0, +255].

uint16
	

A 16-bit unsigned integer whose values exist on the interval [0, +65,535].

uint32
	

A 32-bit unsigned integer whose values exist on the interval [0, +4,294,967,295].

uint64
	

A 64-bit unsigned integer whose values exist on the interval [0, +18,446,744,073,709,551,615].

float32
	

IEEE 754 single-precision (32-bit) binary floating-point number (see IEEE 754-2019).

float64
	

IEEE 754 double-precision (64-bit) binary floating-point number (see IEEE 754-2019).

complex64
	

Single-precision (64-bit) complex floating-point number whose real and imaginary components must be IEEE 754 single-precision (32-bit) binary floating-point numbers (see IEEE 754-2019).

complex128
	

Double-precision (128-bit) complex floating-point number whose real and imaginary components must be IEEE 754 double-precision (64-bit) binary floating-point numbers (see IEEE 754-2019).
"""
"""
DLPack
======

There may be other reasons why it is not possible or desirable for an implementation to materialize the array as strided data in memory. In such cases, the implementation may raise a BufferError in the __dlpack__ or __dlpack_device__ method. In case an implementation is never able to export its array data via DLPack, it may omit __dlpack__ and __dlpack_device__ completely, and hence from_dlpack may raise an AttributeError.
"""

import enum


class DeviceType(enum.StrEnum):
    CPU = enum.auto()
    GPU = enum.auto()


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

