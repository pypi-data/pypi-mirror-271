from __future__ import annotations

import unittest

from mypyc.codegen.emit import Emitter, EmitterContext
from mypyc.ir.ops import BasicBlock, Register, Value
from mypyc.ir.rtypes import RTuple, bool_rprimitive, int_rprimitive, str_rprimitive
from mypyc.namegen import NameGenerator


class TestEmitter(unittest.TestCase):
    def setUp(self) -> None:
        self.n = Register(int_rprimitive, "n")
        self.context = EmitterContext(NameGenerator([["mod"]]))

    def test_label(self) -> None:
        emitter = Emitter(self.context, {})
        assert emitter.label(BasicBlock(4)) == "CPyL4"

    def test_reg(self) -> None:
        names: dict[Value, str] = {self.n: "n"}
        emitter = Emitter(self.context, names)
        assert emitter.reg(self.n) == "cpy_r_n"

    def test_object_annotation(self) -> None:
        emitter = Emitter(self.context, {})
        assert emitter.object_annotation("hello, world", "line;") == " /* 'hello, world' */"
        assert (
            emitter.object_annotation(list(range(30)), "line;")
            == """\
 /* [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
         23, 24, 25, 26, 27, 28, 29] */"""
        )

    def test_emit_line(self) -> None:
        emitter = Emitter(self.context, {})
        emitter.emit_line("line;")
        emitter.emit_line("a {")
        emitter.emit_line("f();")
        emitter.emit_line("}")
        assert emitter.fragments == ["line;\n", "a {\n", "    f();\n", "}\n"]
        emitter = Emitter(self.context, {})
        emitter.emit_line("CPyStatics[0];", ann="hello, world")
        emitter.emit_line("CPyStatics[1];", ann=list(range(30)))
        assert emitter.fragments[0] == "CPyStatics[0]; /* 'hello, world' */\n"
        assert (
            emitter.fragments[1]
            == """\
CPyStatics[1]; /* [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                  21, 22, 23, 24, 25, 26, 27, 28, 29] */\n"""
        )

    def test_emit_undefined_value_for_simple_type(self) -> None:
        emitter = Emitter(self.context, {})
        assert emitter.c_undefined_value(int_rprimitive) == "CPY_INT_TAG"
        assert emitter.c_undefined_value(str_rprimitive) == "NULL"
        assert emitter.c_undefined_value(bool_rprimitive) == "2"

    def test_emit_undefined_value_for_tuple(self) -> None:
        emitter = Emitter(self.context, {})
        assert (
            emitter.c_undefined_value(RTuple([str_rprimitive, int_rprimitive, bool_rprimitive]))
            == "(tuple_T3OIC) { NULL, CPY_INT_TAG, 2 }"
        )
        assert emitter.c_undefined_value(RTuple([str_rprimitive])) == "(tuple_T1O) { NULL }"
        assert (
            emitter.c_undefined_value(RTuple([RTuple([str_rprimitive]), bool_rprimitive]))
            == "(tuple_T2T1OC) { { NULL }, 2 }"
        )
