from __future__ import annotations

from mypy.constraints import SUBTYPE_OF, SUPERTYPE_OF, Constraint, infer_constraints
from mypy.test.helpers import Suite
from mypy.test.typefixture import TypeFixture
from mypy.types import Instance, TupleType, UnpackType


class ConstraintsSuite(Suite):
    def setUp(self) -> None:
        self.fx = TypeFixture()

    def test_no_type_variables(self) -> None:
        assert not infer_constraints(self.fx.o, self.fx.o, SUBTYPE_OF)

    def test_basic_type_variable(self) -> None:
        fx = self.fx
        for direction in [SUBTYPE_OF, SUPERTYPE_OF]:
            assert infer_constraints(fx.gt, fx.ga, direction) == [
                Constraint(type_var=fx.t, op=direction, target=fx.a)
            ]

    def test_basic_type_var_tuple_subtype(self) -> None:
        fx = self.fx
        assert infer_constraints(
            Instance(fx.gvi, [UnpackType(fx.ts)]), Instance(fx.gvi, [fx.a, fx.b]), SUBTYPE_OF
        ) == [
            Constraint(type_var=fx.ts, op=SUBTYPE_OF, target=TupleType([fx.a, fx.b], fx.std_tuple))
        ]

    def test_basic_type_var_tuple(self) -> None:
        fx = self.fx
        assert set(
            infer_constraints(
                Instance(fx.gvi, [UnpackType(fx.ts)]), Instance(fx.gvi, [fx.a, fx.b]), SUPERTYPE_OF
            )
        ) == {
            Constraint(
                type_var=fx.ts, op=SUPERTYPE_OF, target=TupleType([fx.a, fx.b], fx.std_tuple)
            ),
            Constraint(
                type_var=fx.ts, op=SUBTYPE_OF, target=TupleType([fx.a, fx.b], fx.std_tuple)
            ),
        }

    def test_type_var_tuple_with_prefix_and_suffix(self) -> None:
        fx = self.fx
        assert set(
            infer_constraints(
                Instance(fx.gv2i, [fx.t, UnpackType(fx.ts), fx.s]),
                Instance(fx.gv2i, [fx.a, fx.b, fx.c, fx.d]),
                SUPERTYPE_OF,
            )
        ) == {
            Constraint(type_var=fx.t, op=SUPERTYPE_OF, target=fx.a),
            Constraint(
                type_var=fx.ts, op=SUPERTYPE_OF, target=TupleType([fx.b, fx.c], fx.std_tuple)
            ),
            Constraint(
                type_var=fx.ts, op=SUBTYPE_OF, target=TupleType([fx.b, fx.c], fx.std_tuple)
            ),
            Constraint(type_var=fx.s, op=SUPERTYPE_OF, target=fx.d),
        }

    def test_unpack_homogenous_tuple(self) -> None:
        fx = self.fx
        assert set(
            infer_constraints(
                Instance(fx.gvi, [UnpackType(Instance(fx.std_tuplei, [fx.t]))]),
                Instance(fx.gvi, [fx.a, fx.b]),
                SUPERTYPE_OF,
            )
        ) == {
            Constraint(type_var=fx.t, op=SUPERTYPE_OF, target=fx.a),
            Constraint(type_var=fx.t, op=SUBTYPE_OF, target=fx.a),
            Constraint(type_var=fx.t, op=SUPERTYPE_OF, target=fx.b),
            Constraint(type_var=fx.t, op=SUBTYPE_OF, target=fx.b),
        }

    def test_unpack_homogenous_tuple_with_prefix_and_suffix(self) -> None:
        fx = self.fx
        assert set(
            infer_constraints(
                Instance(fx.gv2i, [fx.t, UnpackType(Instance(fx.std_tuplei, [fx.s])), fx.u]),
                Instance(fx.gv2i, [fx.a, fx.b, fx.c, fx.d]),
                SUPERTYPE_OF,
            )
        ) == {
            Constraint(type_var=fx.t, op=SUPERTYPE_OF, target=fx.a),
            Constraint(type_var=fx.s, op=SUPERTYPE_OF, target=fx.b),
            Constraint(type_var=fx.s, op=SUBTYPE_OF, target=fx.b),
            Constraint(type_var=fx.s, op=SUPERTYPE_OF, target=fx.c),
            Constraint(type_var=fx.s, op=SUBTYPE_OF, target=fx.c),
            Constraint(type_var=fx.u, op=SUPERTYPE_OF, target=fx.d),
        }

    def test_unpack_with_prefix_and_suffix(self) -> None:
        fx = self.fx
        assert set(
            infer_constraints(
                Instance(fx.gv2i, [fx.u, fx.t, fx.s, fx.u]),
                Instance(fx.gv2i, [fx.a, fx.b, fx.c, fx.d]),
                SUPERTYPE_OF,
            )
        ) == {
            Constraint(type_var=fx.u, op=SUPERTYPE_OF, target=fx.a),
            Constraint(type_var=fx.t, op=SUPERTYPE_OF, target=fx.b),
            Constraint(type_var=fx.t, op=SUBTYPE_OF, target=fx.b),
            Constraint(type_var=fx.s, op=SUPERTYPE_OF, target=fx.c),
            Constraint(type_var=fx.s, op=SUBTYPE_OF, target=fx.c),
            Constraint(type_var=fx.u, op=SUPERTYPE_OF, target=fx.d),
        }

    def test_unpack_tuple_length_non_match(self) -> None:
        fx = self.fx
        assert set(
            infer_constraints(
                Instance(fx.gv2i, [fx.u, fx.t, fx.s, fx.u]),
                Instance(fx.gv2i, [fx.a, fx.b, fx.d]),
                SUPERTYPE_OF,
            )
            # We still get constraints on the prefix/suffix in this case.
        ) == {
            Constraint(type_var=fx.u, op=SUPERTYPE_OF, target=fx.a),
            Constraint(type_var=fx.u, op=SUPERTYPE_OF, target=fx.d),
        }

    def test_var_length_tuple_with_fixed_length_tuple(self) -> None:
        fx = self.fx
        assert not infer_constraints(
            TupleType([fx.t, fx.s], fallback=Instance(fx.std_tuplei, [fx.o])),
            Instance(fx.std_tuplei, [fx.a]),
            SUPERTYPE_OF,
        )
