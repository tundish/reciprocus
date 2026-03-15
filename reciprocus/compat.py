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
