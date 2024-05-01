"""Test cases for various RType operations."""

from __future__ import annotations

import unittest

from mypyc.ir.rtypes import (
    RUnion,
    bit_rprimitive,
    bool_rprimitive,
    int16_rprimitive,
    int32_rprimitive,
    int64_rprimitive,
    int_rprimitive,
    object_rprimitive,
    short_int_rprimitive,
    str_rprimitive,
)
from mypyc.rt_subtype import is_runtime_subtype
from mypyc.subtype import is_subtype

native_int_types = [int64_rprimitive, int32_rprimitive, int16_rprimitive]


class TestSubtype(unittest.TestCase):
    def test_bit(self) -> None:
        assert is_subtype(bit_rprimitive, bool_rprimitive)
        assert is_subtype(bit_rprimitive, int_rprimitive)
        assert is_subtype(bit_rprimitive, short_int_rprimitive)
        for rt in native_int_types:
            assert is_subtype(bit_rprimitive, rt)

    def test_bool(self) -> None:
        assert not is_subtype(bool_rprimitive, bit_rprimitive)
        assert is_subtype(bool_rprimitive, int_rprimitive)
        assert is_subtype(bool_rprimitive, short_int_rprimitive)
        for rt in native_int_types:
            assert is_subtype(bool_rprimitive, rt)

    def test_int64(self) -> None:
        assert is_subtype(int64_rprimitive, int64_rprimitive)
        assert is_subtype(int64_rprimitive, int_rprimitive)
        assert not is_subtype(int64_rprimitive, short_int_rprimitive)
        assert not is_subtype(int64_rprimitive, int32_rprimitive)
        assert not is_subtype(int64_rprimitive, int16_rprimitive)

    def test_int32(self) -> None:
        assert is_subtype(int32_rprimitive, int32_rprimitive)
        assert is_subtype(int32_rprimitive, int_rprimitive)
        assert not is_subtype(int32_rprimitive, short_int_rprimitive)
        assert not is_subtype(int32_rprimitive, int64_rprimitive)
        assert not is_subtype(int32_rprimitive, int16_rprimitive)

    def test_int16(self) -> None:
        assert is_subtype(int16_rprimitive, int16_rprimitive)
        assert is_subtype(int16_rprimitive, int_rprimitive)
        assert not is_subtype(int16_rprimitive, short_int_rprimitive)
        assert not is_subtype(int16_rprimitive, int64_rprimitive)
        assert not is_subtype(int16_rprimitive, int32_rprimitive)


class TestRuntimeSubtype(unittest.TestCase):
    def test_bit(self) -> None:
        assert is_runtime_subtype(bit_rprimitive, bool_rprimitive)
        assert not is_runtime_subtype(bit_rprimitive, int_rprimitive)

    def test_bool(self) -> None:
        assert not is_runtime_subtype(bool_rprimitive, bit_rprimitive)
        assert not is_runtime_subtype(bool_rprimitive, int_rprimitive)

    def test_union(self) -> None:
        bool_int_mix = RUnion([bool_rprimitive, int_rprimitive])
        assert not is_runtime_subtype(bool_int_mix, short_int_rprimitive)
        assert not is_runtime_subtype(bool_int_mix, int_rprimitive)
        assert not is_runtime_subtype(short_int_rprimitive, bool_int_mix)
        assert not is_runtime_subtype(int_rprimitive, bool_int_mix)


class TestUnionSimplification(unittest.TestCase):
    def test_simple_type_result(self) -> None:
        assert RUnion.make_simplified_union([int_rprimitive]) == int_rprimitive

    def test_remove_duplicate(self) -> None:
        assert RUnion.make_simplified_union([int_rprimitive, int_rprimitive]) == int_rprimitive

    def test_cannot_simplify(self) -> None:
        assert RUnion.make_simplified_union(
            [int_rprimitive, str_rprimitive, object_rprimitive]
        ) == RUnion([int_rprimitive, str_rprimitive, object_rprimitive])

    def test_nested(self) -> None:
        assert RUnion.make_simplified_union(
            [int_rprimitive, RUnion([str_rprimitive, int_rprimitive])]
        ) == RUnion([int_rprimitive, str_rprimitive])
        assert RUnion.make_simplified_union(
            [int_rprimitive, RUnion([str_rprimitive, RUnion([int_rprimitive])])]
        ) == RUnion([int_rprimitive, str_rprimitive])
