"""Classes for representing mypy types."""

from __future__ import annotations

import sys
from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Final,
    Iterable,
    NamedTuple,
    NewType,
    Sequence,
    TypeVar,
    Union,
    cast,
)
from typing_extensions import Self, TypeAlias as _TypeAlias, TypeGuard, overload

import mypy.nodes
from mypy.bogus_type import Bogus
from mypy.nodes import (
    ARG_POS,
    ARG_STAR,
    ARG_STAR2,
    INVARIANT,
    ArgKind,
    FakeInfo,
    FuncDef,
    SymbolNode,
)
from mypy.options import Options
from mypy.state import state
from mypy.util import IdMapper

T = TypeVar("T")

JsonDict: _TypeAlias = Dict[str, Any]

# The set of all valid expressions that can currently be contained
# inside of a Literal[...].
#
# Literals can contain bytes and enum-values: we special-case both of these
# and store the value as a string. We rely on the fallback type that's also
# stored with the Literal to determine how a string is being used.
#
# TODO: confirm that we're happy with representing enums (and the
# other types) in the manner described above.
#
# Note: if we change the set of types included below, we must also
# make sure to audit the following methods:
#
# 1. types.LiteralType's serialize and deserialize methods: this method
#    needs to make sure it can convert the below types into JSON and back.
#
# 2. types.LiteralType's 'value_repr` method: this method is ultimately used
#    by TypeStrVisitor's visit_literal_type to generate a reasonable
#    repr-able output.
#
# 3. server.astdiff.SnapshotTypeVisitor's visit_literal_type_method: this
#    method assumes that the following types supports equality checks and
#    hashability.
#
# Note: Although "Literal[None]" is a valid type, we internally always convert
# such a type directly into "None". So, "None" is not a valid parameter of
# LiteralType and is omitted from this list.
#
# Note: Float values are only used internally. They are not accepted within
# Literal[...].
LiteralValue: _TypeAlias = Union[int, str, bool, float]


# If we only import type_visitor in the middle of the file, mypy
# breaks, and if we do it at the top, it breaks at runtime because of
# import cycle issues, so we do it at the top while typechecking and
# then again in the middle at runtime.
# We should be able to remove this once we are switched to the new
# semantic analyzer!
if TYPE_CHECKING:
    from mypy.type_visitor import (
        SyntheticTypeVisitor as SyntheticTypeVisitor,
        TypeVisitor as TypeVisitor,
    )

TYPE_VAR_LIKE_NAMES: Final = (
    "typing.TypeVar",
    "typing_extensions.TypeVar",
    "typing.ParamSpec",
    "typing_extensions.ParamSpec",
    "typing.TypeVarTuple",
    "typing_extensions.TypeVarTuple",
)

TYPED_NAMEDTUPLE_NAMES: Final = ("typing.NamedTuple", "typing_extensions.NamedTuple")

# Supported names of TypedDict type constructors.
TPDICT_NAMES: Final = (
    "typing.TypedDict",
    "typing_extensions.TypedDict",
    "mypy_extensions.TypedDict",
)

# Supported fallback instance type names for TypedDict types.
TPDICT_FB_NAMES: Final = (
    "typing._TypedDict",
    "typing_extensions._TypedDict",
    "mypy_extensions._TypedDict",
)

# Supported names of Protocol base class.
PROTOCOL_NAMES: Final = ("typing.Protocol", "typing_extensions.Protocol")

# Supported TypeAlias names.
TYPE_ALIAS_NAMES: Final = ("typing.TypeAlias", "typing_extensions.TypeAlias")

# Supported Final type names.
FINAL_TYPE_NAMES: Final = ("typing.Final", "typing_extensions.Final")

# Supported @final decorator names.
FINAL_DECORATOR_NAMES: Final = ("typing.final", "typing_extensions.final")

# Supported @type_check_only names.
TYPE_CHECK_ONLY_NAMES: Final = ("typing.type_check_only", "typing_extensions.type_check_only")

# Supported Literal type names.
LITERAL_TYPE_NAMES: Final = ("typing.Literal", "typing_extensions.Literal")

# Supported Annotated type names.
ANNOTATED_TYPE_NAMES: Final = ("typing.Annotated", "typing_extensions.Annotated")

# Supported @deprecated type names
DEPRECATED_TYPE_NAMES: Final = ("warnings.deprecated", "typing_extensions.deprecated")

# We use this constant in various places when checking `tuple` subtyping:
TUPLE_LIKE_INSTANCE_NAMES: Final = (
    "builtins.tuple",
    "typing.Iterable",
    "typing.Container",
    "typing.Sequence",
    "typing.Reversible",
)

IMPORTED_REVEAL_TYPE_NAMES: Final = ("typing.reveal_type", "typing_extensions.reveal_type")
REVEAL_TYPE_NAMES: Final = ("builtins.reveal_type", *IMPORTED_REVEAL_TYPE_NAMES)

ASSERT_TYPE_NAMES: Final = ("typing.assert_type", "typing_extensions.assert_type")

OVERLOAD_NAMES: Final = ("typing.overload", "typing_extensions.overload")

# Attributes that can optionally be defined in the body of a subclass of
# enum.Enum but are removed from the class __dict__ by EnumMeta.
ENUM_REMOVED_PROPS: Final = ("_ignore_", "_order_", "__order__")

NEVER_NAMES: Final = (
    "typing.NoReturn",
    "typing_extensions.NoReturn",
    "mypy_extensions.NoReturn",
    "typing.Never",
    "typing_extensions.Never",
)

# Mypyc fixed-width native int types (compatible with builtins.int)
MYPYC_NATIVE_INT_NAMES: Final = (
    "mypy_extensions.i64",
    "mypy_extensions.i32",
    "mypy_extensions.i16",
    "mypy_extensions.u8",
)

DATACLASS_TRANSFORM_NAMES: Final = (
    "typing.dataclass_transform",
    "typing_extensions.dataclass_transform",
)
# Supported @override decorator names.
OVERRIDE_DECORATOR_NAMES: Final = ("typing.override", "typing_extensions.override")

# A placeholder used for Bogus[...] parameters
_dummy: Final[Any] = object()

# A placeholder for int parameters
_dummy_int: Final = -999999


class TypeOfAny:
    """
    This class describes different types of Any. Each 'Any' can be of only one type at a time.
    """

    __slots__ = ()

    # Was this Any type inferred without a type annotation?
    unannotated: Final = 1
    # Does this Any come from an explicit type annotation?
    explicit: Final = 2
    # Does this come from an unfollowed import? See --disallow-any-unimported option
    from_unimported_type: Final = 3
    # Does this Any type come from omitted generics?
    from_omitted_generics: Final = 4
    # Does this Any come from an error?
    from_error: Final = 5
    # Is this a type that can't be represented in mypy's type system? For instance, type of
    # call to NewType(...). Even though these types aren't real Anys, we treat them as such.
    # Also used for variables named '_'.
    special_form: Final = 6
    # Does this Any come from interaction with another Any?
    from_another_any: Final = 7
    # Does this Any come from an implementation limitation/bug?
    implementation_artifact: Final = 8
    # Does this Any come from use in the suggestion engine?  This is
    # used to ignore Anys inserted by the suggestion engine when
    # generating constraints.
    suggestion_engine: Final = 9


def deserialize_type(data: JsonDict | str) -> Type:
    if isinstance(data, str):
        return Instance.deserialize(data)
    classname = data[".class"]
    method = deserialize_map.get(classname)
    if method is not None:
        return method(data)
    raise NotImplementedError(f"unexpected .class {classname}")


class Type(mypy.nodes.Context):
    """Abstract base class for all types."""

    __slots__ = ("_can_be_true", "_can_be_false")
    # 'can_be_true' and 'can_be_false' mean whether the value of the
    # expression can be true or false in a boolean context. They are useful
    # when inferring the type of logic expressions like `x and y`.
    #
    # For example:
    #   * the literal `False` can't be true while `True` can.
    #   * a value with type `bool` can be true or false.
    #   * `None` can't be true
    #   * ...

    def __init__(self, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        # Value of these can be -1 (use the default, lazy init), 0 (false) or 1 (true)
        self._can_be_true = -1
        self._can_be_false = -1

    @property
    def can_be_true(self) -> bool:
        if self._can_be_true == -1:  # Lazy init helps mypyc
            self._can_be_true = self.can_be_true_default()
        return bool(self._can_be_true)

    @can_be_true.setter
    def can_be_true(self, v: bool) -> None:
        self._can_be_true = v

    @property
    def can_be_false(self) -> bool:
        if self._can_be_false == -1:  # Lazy init helps mypyc
            self._can_be_false = self.can_be_false_default()
        return bool(self._can_be_false)

    @can_be_false.setter
    def can_be_false(self, v: bool) -> None:
        self._can_be_false = v

    def can_be_true_default(self) -> bool:
        return True

    def can_be_false_default(self) -> bool:
        return True

    def resolve_string_annotation(self) -> Type:
        return self

    def accept(self, visitor: TypeVisitor[T]) -> T:
        raise RuntimeError("Not implemented", type(self))

    def __repr__(self) -> str:
        return self.accept(TypeStrVisitor(options=Options()))

    def str_with_options(self, options: Options) -> str:
        return self.accept(TypeStrVisitor(options=options))

    def serialize(self) -> JsonDict | str:
        raise NotImplementedError(f"Cannot serialize {self.__class__.__name__} instance")

    @classmethod
    def deserialize(cls, data: JsonDict) -> Type:
        raise NotImplementedError(f"Cannot deserialize {cls.__name__} instance")

    def is_singleton_type(self) -> bool:
        return False


class TypeAliasType(Type):
    """A type alias to another type.

    To support recursive type aliases we don't immediately expand a type alias
    during semantic analysis, but create an instance of this type that records the target alias
    definition node (mypy.nodes.TypeAlias) and type arguments (for generic aliases).

    This is very similar to how TypeInfo vs Instance interact, where a recursive class-based
    structure like
        class Node:
            value: int
            children: List[Node]
    can be represented in a tree-like manner.
    """

    __slots__ = ("alias", "args", "type_ref")

    def __init__(
        self,
        alias: mypy.nodes.TypeAlias | None,
        args: list[Type],
        line: int = -1,
        column: int = -1,
    ) -> None:
        super().__init__(line, column)
        self.alias = alias
        self.args = args
        self.type_ref: str | None = None

    def _expand_once(self) -> Type:
        """Expand to the target type exactly once.

        This doesn't do full expansion, i.e. the result can contain another
        (or even this same) type alias. Use this internal helper only when really needed,
        its public wrapper mypy.types.get_proper_type() is preferred.
        """
        assert self.alias is not None
        if self.alias.no_args:
            # We know that no_args=True aliases like L = List must have an instance
            # as their target.
            assert isinstance(self.alias.target, Instance)  # type: ignore[misc]
            return self.alias.target.copy_modified(args=self.args)

        # TODO: this logic duplicates the one in expand_type_by_instance().
        if self.alias.tvar_tuple_index is None:
            mapping = {v.id: s for (v, s) in zip(self.alias.alias_tvars, self.args)}
        else:
            prefix = self.alias.tvar_tuple_index
            suffix = len(self.alias.alias_tvars) - self.alias.tvar_tuple_index - 1
            start, middle, end = split_with_prefix_and_suffix(tuple(self.args), prefix, suffix)
            tvar = self.alias.alias_tvars[prefix]
            assert isinstance(tvar, TypeVarTupleType)
            mapping = {tvar.id: TupleType(list(middle), tvar.tuple_fallback)}
            for tvar, sub in zip(
                self.alias.alias_tvars[:prefix] + self.alias.alias_tvars[prefix + 1 :], start + end
            ):
                mapping[tvar.id] = sub

        new_tp = self.alias.target.accept(InstantiateAliasVisitor(mapping))
        new_tp.accept(LocationSetter(self.line, self.column))
        new_tp.line = self.line
        new_tp.column = self.column
        return new_tp

    def _partial_expansion(self, nothing_args: bool = False) -> tuple[ProperType, bool]:
        # Private method mostly for debugging and testing.
        unroller = UnrollAliasVisitor(set())
        if nothing_args:
            alias = self.copy_modified(args=[UninhabitedType()] * len(self.args))
        else:
            alias = self
        unrolled = alias.accept(unroller)
        assert isinstance(unrolled, ProperType)
        return unrolled, unroller.recursed

    def expand_all_if_possible(self, nothing_args: bool = False) -> ProperType | None:
        """Attempt a full expansion of the type alias (including nested aliases).

        If the expansion is not possible, i.e. the alias is (mutually-)recursive,
        return None. If nothing_args is True, replace all type arguments with an
        UninhabitedType() (used to detect recursively defined aliases).
        """
        unrolled, recursed = self._partial_expansion(nothing_args=nothing_args)
        if recursed:
            return None
        return unrolled

    @property
    def is_recursive(self) -> bool:
        """Whether this type alias is recursive.

        Note this doesn't check generic alias arguments, but only if this alias
        *definition* is recursive. The property value thus can be cached on the
        underlying TypeAlias node. If you want to include all nested types, use
        has_recursive_types() function.
        """
        assert self.alias is not None, "Unfixed type alias"
        is_recursive = self.alias._is_recursive
        if is_recursive is None:
            is_recursive = self.expand_all_if_possible(nothing_args=True) is None
            # We cache the value on the underlying TypeAlias node as an optimization,
            # since the value is the same for all instances of the same alias.
            self.alias._is_recursive = is_recursive
        return is_recursive

    def can_be_true_default(self) -> bool:
        if self.alias is not None:
            return self.alias.target.can_be_true
        return super().can_be_true_default()

    def can_be_false_default(self) -> bool:
        if self.alias is not None:
            return self.alias.target.can_be_false
        return super().can_be_false_default()

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_type_alias_type(self)

    def __hash__(self) -> int:
        return hash((self.alias, tuple(self.args)))

    def __eq__(self, other: object) -> bool:
        # Note: never use this to determine subtype relationships, use is_subtype().
        if not isinstance(other, TypeAliasType):
            return NotImplemented
        return self.alias == other.alias and self.args == other.args

    def serialize(self) -> JsonDict:
        assert self.alias is not None
        data: JsonDict = {
            ".class": "TypeAliasType",
            "type_ref": self.alias.fullname,
            "args": [arg.serialize() for arg in self.args],
        }
        return data

    @classmethod
    def deserialize(cls, data: JsonDict) -> TypeAliasType:
        assert data[".class"] == "TypeAliasType"
        args: list[Type] = []
        if "args" in data:
            args_list = data["args"]
            assert isinstance(args_list, list)
            args = [deserialize_type(arg) for arg in args_list]
        alias = TypeAliasType(None, args)
        alias.type_ref = data["type_ref"]
        return alias

    def copy_modified(self, *, args: list[Type] | None = None) -> TypeAliasType:
        return TypeAliasType(
            self.alias, args if args is not None else self.args.copy(), self.line, self.column
        )


class TypeGuardedType(Type):
    """Only used by find_isinstance_check() etc."""

    __slots__ = ("type_guard",)

    def __init__(self, type_guard: Type) -> None:
        super().__init__(line=type_guard.line, column=type_guard.column)
        self.type_guard = type_guard

    def __repr__(self) -> str:
        return f"TypeGuard({self.type_guard})"


class RequiredType(Type):
    """Required[T] or NotRequired[T]. Only usable at top-level of a TypedDict definition."""

    def __init__(self, item: Type, *, required: bool) -> None:
        super().__init__(line=item.line, column=item.column)
        self.item = item
        self.required = required

    def __repr__(self) -> str:
        if self.required:
            return f"Required[{self.item}]"
        else:
            return f"NotRequired[{self.item}]"

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return self.item.accept(visitor)


class ProperType(Type):
    """Not a type alias.

    Every type except TypeAliasType must inherit from this type.
    """

    __slots__ = ()


class TypeVarId:
    # A type variable is uniquely identified by its raw id and meta level.

    # For plain variables (type parameters of generic classes and
    # functions) raw ids are allocated by semantic analysis, using
    # positive ids 1, 2, ... for generic class parameters and negative
    # ids -1, ... for generic function type arguments. A special value 0
    # is reserved for Self type variable (autogenerated). This convention
    # is only used to keep type variable ids distinct when allocating
    # them; the type checker makes no distinction between class and
    # function type variables.

    # Metavariables are allocated unique ids starting from 1.
    raw_id: int = 0

    # Level of the variable in type inference. Currently either 0 for
    # declared types, or 1 for type inference metavariables.
    meta_level: int = 0

    # Class variable used for allocating fresh ids for metavariables.
    next_raw_id: ClassVar[int] = 1

    # Fullname of class (or potentially function in the future) which
    # declares this type variable (not the fullname of the TypeVar
    # definition!), or ''
    namespace: str

    def __init__(self, raw_id: int, meta_level: int = 0, *, namespace: str = "") -> None:
        self.raw_id = raw_id
        self.meta_level = meta_level
        self.namespace = namespace

    @staticmethod
    def new(meta_level: int) -> TypeVarId:
        raw_id = TypeVarId.next_raw_id
        TypeVarId.next_raw_id += 1
        return TypeVarId(raw_id, meta_level)

    def __repr__(self) -> str:
        return self.raw_id.__repr__()

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, TypeVarId)
            and self.raw_id == other.raw_id
            and self.meta_level == other.meta_level
            and self.namespace == other.namespace
        )

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((self.raw_id, self.meta_level, self.namespace))

    def is_meta_var(self) -> bool:
        return self.meta_level > 0


class TypeVarLikeType(ProperType):
    __slots__ = ("name", "fullname", "id", "upper_bound", "default")

    name: str  # Name (may be qualified)
    fullname: str  # Fully qualified name
    id: TypeVarId
    upper_bound: Type
    default: Type

    def __init__(
        self,
        name: str,
        fullname: str,
        id: TypeVarId | int,
        upper_bound: Type,
        default: Type,
        line: int = -1,
        column: int = -1,
    ) -> None:
        super().__init__(line, column)
        self.name = name
        self.fullname = fullname
        if isinstance(id, int):
            id = TypeVarId(id)
        self.id = id
        self.upper_bound = upper_bound
        self.default = default

    def serialize(self) -> JsonDict:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data: JsonDict) -> TypeVarLikeType:
        raise NotImplementedError

    def copy_modified(self, *, id: TypeVarId, **kwargs: Any) -> Self:
        raise NotImplementedError

    @classmethod
    def new_unification_variable(cls, old: Self) -> Self:
        new_id = TypeVarId.new(meta_level=1)
        return old.copy_modified(id=new_id)

    def has_default(self) -> bool:
        t = get_proper_type(self.default)
        return not (isinstance(t, AnyType) and t.type_of_any == TypeOfAny.from_omitted_generics)


class TypeVarType(TypeVarLikeType):
    """Type that refers to a type variable."""

    __slots__ = ("values", "variance")

    values: list[Type]  # Value restriction, empty list if no restriction
    variance: int

    def __init__(
        self,
        name: str,
        fullname: str,
        id: TypeVarId | int,
        values: list[Type],
        upper_bound: Type,
        default: Type,
        variance: int = INVARIANT,
        line: int = -1,
        column: int = -1,
    ) -> None:
        super().__init__(name, fullname, id, upper_bound, default, line, column)
        assert values is not None, "No restrictions must be represented by empty list"
        self.values = values
        self.variance = variance

    def copy_modified(
        self,
        *,
        values: Bogus[list[Type]] = _dummy,
        upper_bound: Bogus[Type] = _dummy,
        default: Bogus[Type] = _dummy,
        id: Bogus[TypeVarId | int] = _dummy,
        line: int = _dummy_int,
        column: int = _dummy_int,
        **kwargs: Any,
    ) -> TypeVarType:
        return TypeVarType(
            name=self.name,
            fullname=self.fullname,
            id=self.id if id is _dummy else id,
            values=self.values if values is _dummy else values,
            upper_bound=self.upper_bound if upper_bound is _dummy else upper_bound,
            default=self.default if default is _dummy else default,
            variance=self.variance,
            line=self.line if line == _dummy_int else line,
            column=self.column if column == _dummy_int else column,
        )

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_type_var(self)

    def __hash__(self) -> int:
        return hash((self.id, self.upper_bound, tuple(self.values)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TypeVarType):
            return NotImplemented
        return (
            self.id == other.id
            and self.upper_bound == other.upper_bound
            and self.values == other.values
        )

    def serialize(self) -> JsonDict:
        assert not self.id.is_meta_var()
        return {
            ".class": "TypeVarType",
            "name": self.name,
            "fullname": self.fullname,
            "id": self.id.raw_id,
            "namespace": self.id.namespace,
            "values": [v.serialize() for v in self.values],
            "upper_bound": self.upper_bound.serialize(),
            "default": self.default.serialize(),
            "variance": self.variance,
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> TypeVarType:
        assert data[".class"] == "TypeVarType"
        return TypeVarType(
            name=data["name"],
            fullname=data["fullname"],
            id=TypeVarId(data["id"], namespace=data["namespace"]),
            values=[deserialize_type(v) for v in data["values"]],
            upper_bound=deserialize_type(data["upper_bound"]),
            default=deserialize_type(data["default"]),
            variance=data["variance"],
        )


class ParamSpecFlavor:
    # Simple ParamSpec reference such as "P"
    BARE: Final = 0
    # P.args
    ARGS: Final = 1
    # P.kwargs
    KWARGS: Final = 2


class ParamSpecType(TypeVarLikeType):
    """Type that refers to a ParamSpec.

    A ParamSpec is a type variable that represents the parameter
    types, names and kinds of a callable (i.e., the signature without
    the return type).

    This can be one of these forms
     * P (ParamSpecFlavor.BARE)
     * P.args (ParamSpecFlavor.ARGS)
     * P.kwargs (ParamSpecFLavor.KWARGS)

    The upper_bound is really used as a fallback type -- it's shared
    with TypeVarType for simplicity. It can't be specified by the user
    and the value is directly derived from the flavor (currently
    always just 'object').
    """

    __slots__ = ("flavor", "prefix")

    flavor: int
    prefix: Parameters

    def __init__(
        self,
        name: str,
        fullname: str,
        id: TypeVarId | int,
        flavor: int,
        upper_bound: Type,
        default: Type,
        *,
        line: int = -1,
        column: int = -1,
        prefix: Parameters | None = None,
    ) -> None:
        super().__init__(name, fullname, id, upper_bound, default, line=line, column=column)
        self.flavor = flavor
        self.prefix = prefix or Parameters([], [], [])

    def with_flavor(self, flavor: int) -> ParamSpecType:
        return ParamSpecType(
            self.name,
            self.fullname,
            self.id,
            flavor,
            upper_bound=self.upper_bound,
            default=self.default,
            prefix=self.prefix,
        )

    def copy_modified(
        self,
        *,
        id: Bogus[TypeVarId | int] = _dummy,
        flavor: int = _dummy_int,
        prefix: Bogus[Parameters] = _dummy,
        default: Bogus[Type] = _dummy,
        **kwargs: Any,
    ) -> ParamSpecType:
        return ParamSpecType(
            self.name,
            self.fullname,
            id if id is not _dummy else self.id,
            flavor if flavor != _dummy_int else self.flavor,
            self.upper_bound,
            default=default if default is not _dummy else self.default,
            line=self.line,
            column=self.column,
            prefix=prefix if prefix is not _dummy else self.prefix,
        )

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_param_spec(self)

    def name_with_suffix(self) -> str:
        n = self.name
        if self.flavor == ParamSpecFlavor.ARGS:
            return f"{n}.args"
        elif self.flavor == ParamSpecFlavor.KWARGS:
            return f"{n}.kwargs"
        return n

    def __hash__(self) -> int:
        return hash((self.id, self.flavor, self.prefix))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ParamSpecType):
            return NotImplemented
        # Upper bound can be ignored, since it's determined by flavor.
        return self.id == other.id and self.flavor == other.flavor and self.prefix == other.prefix

    def serialize(self) -> JsonDict:
        assert not self.id.is_meta_var()
        return {
            ".class": "ParamSpecType",
            "name": self.name,
            "fullname": self.fullname,
            "id": self.id.raw_id,
            "flavor": self.flavor,
            "upper_bound": self.upper_bound.serialize(),
            "default": self.default.serialize(),
            "prefix": self.prefix.serialize(),
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> ParamSpecType:
        assert data[".class"] == "ParamSpecType"
        return ParamSpecType(
            data["name"],
            data["fullname"],
            data["id"],
            data["flavor"],
            deserialize_type(data["upper_bound"]),
            deserialize_type(data["default"]),
            prefix=Parameters.deserialize(data["prefix"]),
        )


class TypeVarTupleType(TypeVarLikeType):
    """Type that refers to a TypeVarTuple.

    See PEP646 for more information.
    """

    __slots__ = ("tuple_fallback", "min_len")

    def __init__(
        self,
        name: str,
        fullname: str,
        id: TypeVarId | int,
        upper_bound: Type,
        tuple_fallback: Instance,
        default: Type,
        *,
        line: int = -1,
        column: int = -1,
        min_len: int = 0,
    ) -> None:
        super().__init__(name, fullname, id, upper_bound, default, line=line, column=column)
        self.tuple_fallback = tuple_fallback
        # This value is not settable by a user. It is an internal-only thing to support
        # len()-narrowing of variadic tuples.
        self.min_len = min_len

    def serialize(self) -> JsonDict:
        assert not self.id.is_meta_var()
        return {
            ".class": "TypeVarTupleType",
            "name": self.name,
            "fullname": self.fullname,
            "id": self.id.raw_id,
            "upper_bound": self.upper_bound.serialize(),
            "tuple_fallback": self.tuple_fallback.serialize(),
            "default": self.default.serialize(),
            "min_len": self.min_len,
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> TypeVarTupleType:
        assert data[".class"] == "TypeVarTupleType"
        return TypeVarTupleType(
            data["name"],
            data["fullname"],
            data["id"],
            deserialize_type(data["upper_bound"]),
            Instance.deserialize(data["tuple_fallback"]),
            deserialize_type(data["default"]),
            min_len=data["min_len"],
        )

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_type_var_tuple(self)

    def __hash__(self) -> int:
        return hash((self.id, self.min_len))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TypeVarTupleType):
            return NotImplemented
        return self.id == other.id and self.min_len == other.min_len

    def copy_modified(
        self,
        *,
        id: Bogus[TypeVarId | int] = _dummy,
        upper_bound: Bogus[Type] = _dummy,
        default: Bogus[Type] = _dummy,
        min_len: Bogus[int] = _dummy,
        **kwargs: Any,
    ) -> TypeVarTupleType:
        return TypeVarTupleType(
            self.name,
            self.fullname,
            self.id if id is _dummy else id,
            self.upper_bound if upper_bound is _dummy else upper_bound,
            self.tuple_fallback,
            self.default if default is _dummy else default,
            line=self.line,
            column=self.column,
            min_len=self.min_len if min_len is _dummy else min_len,
        )


class UnboundType(ProperType):
    """Instance type that has not been bound during semantic analysis."""

    __slots__ = ("name", "args", "optional", "empty_tuple_index")

    def __init__(
        self,
        name: str | None,
        args: Sequence[Type] | None = None,
        line: int = -1,
        column: int = -1,
        optional: bool = False,
        empty_tuple_index: bool = False,
    ) -> None:
        super().__init__(line, column)
        if not args:
            args = []
        assert name is not None
        self.name = name
        self.args = tuple(args)
        # Should this type be wrapped in an Optional?
        self.optional = optional
        # Special case for X[()]
        self.empty_tuple_index = empty_tuple_index

    def copy_modified(self, args: Bogus[Sequence[Type] | None] = _dummy) -> UnboundType:
        if args is _dummy:
            args = self.args
        return UnboundType(
            name=self.name,
            args=args,
            line=self.line,
            column=self.column,
            optional=self.optional,
            empty_tuple_index=self.empty_tuple_index,
        )

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_unbound_type(self)

    def __hash__(self) -> int:
        return hash((self.name, self.optional, tuple(self.args)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UnboundType):
            return NotImplemented
        return (
            self.name == other.name and self.optional == other.optional and self.args == other.args
        )

    def serialize(self) -> JsonDict:
        return {
            ".class": "UnboundType",
            "name": self.name,
            "args": [a.serialize() for a in self.args],
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> UnboundType:
        assert data[".class"] == "UnboundType"
        return UnboundType(data["name"], [deserialize_type(a) for a in data["args"]])


class CallableArgument(ProperType):
    """Represents a Arg(type, 'name') inside a Callable's type list.

    Note that this is a synthetic type for helping parse ASTs, not a real type.
    """

    __slots__ = ("typ", "name", "constructor")

    typ: Type
    name: str | None
    constructor: str | None

    def __init__(
        self,
        typ: Type,
        name: str | None,
        constructor: str | None,
        line: int = -1,
        column: int = -1,
    ) -> None:
        super().__init__(line, column)
        self.typ = typ
        self.name = name
        self.constructor = constructor

    def accept(self, visitor: TypeVisitor[T]) -> T:
        assert isinstance(visitor, SyntheticTypeVisitor)
        ret: T = visitor.visit_callable_argument(self)
        return ret

    def serialize(self) -> JsonDict:
        assert False, "Synthetic types don't serialize"


class TypeList(ProperType):
    """Information about argument types and names [...].

    This is used for the arguments of a Callable type, i.e. for
    [arg, ...] in Callable[[arg, ...], ret]. This is not a real type
    but a syntactic AST construct. UnboundTypes can also have TypeList
    types before they are processed into Callable types.
    """

    __slots__ = ("items",)

    items: list[Type]

    def __init__(self, items: list[Type], line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.items = items

    def accept(self, visitor: TypeVisitor[T]) -> T:
        assert isinstance(visitor, SyntheticTypeVisitor)
        ret: T = visitor.visit_type_list(self)
        return ret

    def serialize(self) -> JsonDict:
        assert False, "Synthetic types don't serialize"

    def __hash__(self) -> int:
        return hash(tuple(self.items))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TypeList) and self.items == other.items


class UnpackType(ProperType):
    """Type operator Unpack from PEP646. Can be either with Unpack[]
    or unpacking * syntax.

    The inner type should be either a TypeVarTuple, or a variable length tuple.
    In an exceptional case of callable star argument it can be a fixed length tuple.

    Note: the above restrictions are only guaranteed by normalizations after semantic
    analysis, if your code needs to handle UnpackType *during* semantic analysis, it is
    wild west, technically anything can be present in the wrapped type.
    """

    __slots__ = ["type", "from_star_syntax"]

    def __init__(
        self, typ: Type, line: int = -1, column: int = -1, from_star_syntax: bool = False
    ) -> None:
        super().__init__(line, column)
        self.type = typ
        self.from_star_syntax = from_star_syntax

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_unpack_type(self)

    def serialize(self) -> JsonDict:
        return {".class": "UnpackType", "type": self.type.serialize()}

    @classmethod
    def deserialize(cls, data: JsonDict) -> UnpackType:
        assert data[".class"] == "UnpackType"
        typ = data["type"]
        return UnpackType(deserialize_type(typ))

    def __hash__(self) -> int:
        return hash(self.type)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UnpackType) and self.type == other.type


class AnyType(ProperType):
    """The type 'Any'."""

    __slots__ = ("type_of_any", "source_any", "missing_import_name")

    def __init__(
        self,
        type_of_any: int,
        source_any: AnyType | None = None,
        missing_import_name: str | None = None,
        line: int = -1,
        column: int = -1,
    ) -> None:
        super().__init__(line, column)
        self.type_of_any = type_of_any
        # If this Any was created as a result of interacting with another 'Any', record the source
        # and use it in reports.
        self.source_any = source_any
        if source_any and source_any.source_any:
            self.source_any = source_any.source_any

        if source_any is None:
            self.missing_import_name = missing_import_name
        else:
            self.missing_import_name = source_any.missing_import_name

        # Only unimported type anys and anys from other anys should have an import name
        assert missing_import_name is None or type_of_any in (
            TypeOfAny.from_unimported_type,
            TypeOfAny.from_another_any,
        )
        # Only Anys that come from another Any can have source_any.
        assert type_of_any != TypeOfAny.from_another_any or source_any is not None
        # We should not have chains of Anys.
        assert not self.source_any or self.source_any.type_of_any != TypeOfAny.from_another_any

    @property
    def is_from_error(self) -> bool:
        return self.type_of_any == TypeOfAny.from_error

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_any(self)

    def copy_modified(
        self,
        # Mark with Bogus because _dummy is just an object (with type Any)
        type_of_any: int = _dummy_int,
        original_any: Bogus[AnyType | None] = _dummy,
    ) -> AnyType:
        if type_of_any == _dummy_int:
            type_of_any = self.type_of_any
        if original_any is _dummy:
            original_any = self.source_any
        return AnyType(
            type_of_any=type_of_any,
            source_any=original_any,
            missing_import_name=self.missing_import_name,
            line=self.line,
            column=self.column,
        )

    def __hash__(self) -> int:
        return hash(AnyType)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AnyType)

    def serialize(self) -> JsonDict:
        return {
            ".class": "AnyType",
            "type_of_any": self.type_of_any,
            "source_any": self.source_any.serialize() if self.source_any is not None else None,
            "missing_import_name": self.missing_import_name,
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> AnyType:
        assert data[".class"] == "AnyType"
        source = data["source_any"]
        return AnyType(
            data["type_of_any"],
            AnyType.deserialize(source) if source is not None else None,
            data["missing_import_name"],
        )


class UninhabitedType(ProperType):
    """This type has no members.

    This type is the bottom type.
    With strict Optional checking, it is the only common subtype between all
    other types, which allows `meet` to be well defined.  Without strict
    Optional checking, NoneType fills this role.

    In general, for any type T:
        join(UninhabitedType, T) = T
        meet(UninhabitedType, T) = UninhabitedType
        is_subtype(UninhabitedType, T) = True
    """

    __slots__ = ("ambiguous", "is_noreturn")

    is_noreturn: bool  # Does this come from a NoReturn?  Purely for error messages.
    # It is important to track whether this is an actual NoReturn type, or just a result
    # of ambiguous type inference, in the latter case we don't want to mark a branch as
    # unreachable in binder.
    ambiguous: bool  # Is this a result of inference for a variable without constraints?

    def __init__(self, is_noreturn: bool = False, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.is_noreturn = is_noreturn
        self.ambiguous = False

    def can_be_true_default(self) -> bool:
        return False

    def can_be_false_default(self) -> bool:
        return False

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_uninhabited_type(self)

    def __hash__(self) -> int:
        return hash(UninhabitedType)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UninhabitedType)

    def serialize(self) -> JsonDict:
        return {".class": "UninhabitedType", "is_noreturn": self.is_noreturn}

    @classmethod
    def deserialize(cls, data: JsonDict) -> UninhabitedType:
        assert data[".class"] == "UninhabitedType"
        return UninhabitedType(is_noreturn=data["is_noreturn"])


class NoneType(ProperType):
    """The type of 'None'.

    This type can be written by users as 'None'.
    """

    __slots__ = ()

    def __init__(self, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)

    def can_be_true_default(self) -> bool:
        return False

    def __hash__(self) -> int:
        return hash(NoneType)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NoneType)

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_none_type(self)

    def serialize(self) -> JsonDict:
        return {".class": "NoneType"}

    @classmethod
    def deserialize(cls, data: JsonDict) -> NoneType:
        assert data[".class"] == "NoneType"
        return NoneType()

    def is_singleton_type(self) -> bool:
        return True


# NoneType used to be called NoneTyp so to avoid needlessly breaking
# external plugins we keep that alias here.
NoneTyp = NoneType


class ErasedType(ProperType):
    """Placeholder for an erased type.

    This is used during type inference. This has the special property that
    it is ignored during type inference.
    """

    __slots__ = ()

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_erased_type(self)


class DeletedType(ProperType):
    """Type of deleted variables.

    These can be used as lvalues but not rvalues.
    """

    __slots__ = ("source",)

    source: str | None  # May be None; name that generated this value

    def __init__(self, source: str | None = None, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self.source = source

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_deleted_type(self)

    def serialize(self) -> JsonDict:
        return {".class": "DeletedType", "source": self.source}

    @classmethod
    def deserialize(cls, data: JsonDict) -> DeletedType:
        assert data[".class"] == "DeletedType"
        return DeletedType(data["source"])


# Fake TypeInfo to be used as a placeholder during Instance de-serialization.
NOT_READY: Final = mypy.nodes.FakeInfo("De-serialization failure: TypeInfo not fixed")


class ExtraAttrs:
    """Summary of module attributes and types.

    This is used for instances of types.ModuleType, because they can have different
    attributes per instance, and for type narrowing with hasattr() checks.
    """

    def __init__(
        self,
        attrs: dict[str, Type],
        immutable: set[str] | None = None,
        mod_name: str | None = None,
    ) -> None:
        self.attrs = attrs
        if immutable is None:
            immutable = set()
        self.immutable = immutable
        self.mod_name = mod_name

    def __hash__(self) -> int:
        return hash((tuple(self.attrs.items()), tuple(sorted(self.immutable))))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExtraAttrs):
            return NotImplemented
        return self.attrs == other.attrs and self.immutable == other.immutable

    def copy(self) -> ExtraAttrs:
        return ExtraAttrs(self.attrs.copy(), self.immutable.copy(), self.mod_name)

    def __repr__(self) -> str:
        return f"ExtraAttrs({self.attrs!r}, {self.immutable!r}, {self.mod_name!r})"


class Instance(ProperType):
    """An instance type of form C[T1, ..., Tn].

    The list of type variables may be empty.

    Several types have fallbacks to `Instance`, because in Python everything is an object
    and this concept is impossible to express without intersection types. We therefore use
    fallbacks for all "non-special" (like UninhabitedType, ErasedType etc) types.
    """

    __slots__ = ("type", "args", "invalid", "type_ref", "last_known_value", "_hash", "extra_attrs")

    def __init__(
        self,
        typ: mypy.nodes.TypeInfo,
        args: Sequence[Type],
        line: int = -1,
        column: int = -1,
        *,
        last_known_value: LiteralType | None = None,
        extra_attrs: ExtraAttrs | None = None,
    ) -> None:
        super().__init__(line, column)
        self.type = typ
        self.args = tuple(args)
        self.type_ref: str | None = None

        # True if recovered after incorrect number of type arguments error
        self.invalid = False

        # This field keeps track of the underlying Literal[...] value associated with
        # this instance, if one is known.
        #
        # This field is set whenever possible within expressions, but is erased upon
        # variable assignment (see erasetype.remove_instance_last_known_values) unless
        # the variable is declared to be final.
        #
        # For example, consider the following program:
        #
        #     a = 1
        #     b: Final[int] = 2
        #     c: Final = 3
        #     print(a + b + c + 4)
        #
        # The 'Instance' objects associated with the expressions '1', '2', '3', and '4' will
        # have last_known_values of type Literal[1], Literal[2], Literal[3], and Literal[4]
        # respectively. However, the Instance object assigned to 'a' and 'b' will have their
        # last_known_value erased: variable 'a' is mutable; variable 'b' was declared to be
        # specifically an int.
        #
        # Or more broadly, this field lets this Instance "remember" its original declaration
        # when applicable. We want this behavior because we want implicit Final declarations
        # to act pretty much identically with constants: we should be able to replace any
        # places where we use some Final variable with the original value and get the same
        # type-checking behavior. For example, we want this program:
        #
        #    def expects_literal(x: Literal[3]) -> None: pass
        #    var: Final = 3
        #    expects_literal(var)
        #
        # ...to type-check in the exact same way as if we had written the program like this:
        #
        #    def expects_literal(x: Literal[3]) -> None: pass
        #    expects_literal(3)
        #
        # In order to make this work (especially with literal types), we need var's type
        # (an Instance) to remember the "original" value.
        #
        # Preserving this value within expressions is useful for similar reasons.
        #
        # Currently most of mypy will ignore this field and will continue to treat this type like
        # a regular Instance. We end up using this field only when we are explicitly within a
        # Literal context.
        self.last_known_value = last_known_value

        # Cached hash value
        self._hash = -1

        # Additional attributes defined per instance of this type. For example modules
        # have different attributes per instance of types.ModuleType. This is intended
        # to be "short-lived", we don't serialize it, and even don't store as variable type.
        self.extra_attrs = extra_attrs

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_instance(self)

    def __hash__(self) -> int:
        if self._hash == -1:
            self._hash = hash((self.type, self.args, self.last_known_value, self.extra_attrs))
        return self._hash

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Instance):
            return NotImplemented
        return (
            self.type == other.type
            and self.args == other.args
            and self.last_known_value == other.last_known_value
            and self.extra_attrs == other.extra_attrs
        )

    def serialize(self) -> JsonDict | str:
        assert self.type is not None
        type_ref = self.type.fullname
        if not self.args and not self.last_known_value:
            return type_ref
        data: JsonDict = {".class": "Instance"}
        data["type_ref"] = type_ref
        data["args"] = [arg.serialize() for arg in self.args]
        if self.last_known_value is not None:
            data["last_known_value"] = self.last_known_value.serialize()
        return data

    @classmethod
    def deserialize(cls, data: JsonDict | str) -> Instance:
        if isinstance(data, str):
            inst = Instance(NOT_READY, [])
            inst.type_ref = data
            return inst
        assert data[".class"] == "Instance"
        args: list[Type] = []
        if "args" in data:
            args_list = data["args"]
            assert isinstance(args_list, list)
            args = [deserialize_type(arg) for arg in args_list]
        inst = Instance(NOT_READY, args)
        inst.type_ref = data["type_ref"]  # Will be fixed up by fixup.py later.
        if "last_known_value" in data:
            inst.last_known_value = LiteralType.deserialize(data["last_known_value"])
        return inst

    def copy_modified(
        self,
        *,
        args: Bogus[list[Type]] = _dummy,
        last_known_value: Bogus[LiteralType | None] = _dummy,
    ) -> Instance:
        new = Instance(
            self.type,
            args if args is not _dummy else self.args,
            self.line,
            self.column,
            last_known_value=(
                last_known_value if last_known_value is not _dummy else self.last_known_value
            ),
        )
        # We intentionally don't copy the extra_attrs here, so they will be erased.
        new.can_be_true = self.can_be_true
        new.can_be_false = self.can_be_false
        return new

    def copy_with_extra_attr(self, name: str, typ: Type) -> Instance:
        if self.extra_attrs:
            existing_attrs = self.extra_attrs.copy()
        else:
            existing_attrs = ExtraAttrs({}, set(), None)
        existing_attrs.attrs[name] = typ
        new = self.copy_modified()
        new.extra_attrs = existing_attrs
        return new

    def is_singleton_type(self) -> bool:
        # TODO:
        # Also make this return True if the type corresponds to NotImplemented?
        return (
            self.type.is_enum
            and len(self.get_enum_values()) == 1
            or self.type.fullname in {"builtins.ellipsis", "types.EllipsisType"}
        )

    def get_enum_values(self) -> list[str]:
        """Return the list of values for an Enum."""
        return [
            name for name, sym in self.type.names.items() if isinstance(sym.node, mypy.nodes.Var)
        ]


class FunctionLike(ProperType):
    """Abstract base class for function types."""

    __slots__ = ("fallback",)

    fallback: Instance

    def __init__(self, line: int = -1, column: int = -1) -> None:
        super().__init__(line, column)
        self._can_be_false = False

    @abstractmethod
    def is_type_obj(self) -> bool:
        pass

    @abstractmethod
    def type_object(self) -> mypy.nodes.TypeInfo:
        pass

    @property
    @abstractmethod
    def items(self) -> list[CallableType]:
        pass

    @abstractmethod
    def with_name(self, name: str) -> FunctionLike:
        pass

    @abstractmethod
    def get_name(self) -> str | None:
        pass


class FormalArgument(NamedTuple):
    name: str | None
    pos: int | None
    typ: Type
    required: bool


class Parameters(ProperType):
    """Type that represents the parameters to a function.

    Used for ParamSpec analysis. Note that by convention we handle this
    type as a Callable without return type, not as a "tuple with names",
    so that it behaves contravariantly, in particular [x: int] <: [int].
    """

    __slots__ = (
        "arg_types",
        "arg_kinds",
        "arg_names",
        "min_args",
        "is_ellipsis_args",
        # TODO: variables don't really belong here, but they are used to allow hacky support
        # for forall . Foo[[x: T], T] by capturing generic callable with ParamSpec, see #15909
        "variables",
        "imprecise_arg_kinds",
    )

    def __init__(
        self,
        arg_types: Sequence[Type],
        arg_kinds: list[ArgKind],
        arg_names: Sequence[str | None],
        *,
        variables: Sequence[TypeVarLikeType] | None = None,
        is_ellipsis_args: bool = False,
        imprecise_arg_kinds: bool = False,
        line: int = -1,
        column: int = -1,
    ) -> None:
        super().__init__(line, column)
        self.arg_types = list(arg_types)
        self.arg_kinds = arg_kinds
        self.arg_names = list(arg_names)
        assert len(arg_types) == len(arg_kinds) == len(arg_names)
        assert not any(isinstance(t, Parameters) for t in arg_types)
        self.min_args = arg_kinds.count(ARG_POS)
        self.is_ellipsis_args = is_ellipsis_args
        self.variables = variables or []
        self.imprecise_arg_kinds = imprecise_arg_kinds

    def copy_modified(
        self,
        arg_types: Bogus[Sequence[Type]] = _dummy,
        arg_kinds: Bogus[list[ArgKind]] = _dummy,
        arg_names: Bogus[Sequence[str | None]] = _dummy,
        *,
        variables: Bogus[Sequence[TypeVarLikeType]] = _dummy,
        is_ellipsis_args: Bogus[bool] = _dummy,
        imprecise_arg_kinds: Bogus[bool] = _dummy,
    ) -> Parameters:
        return Parameters(
            arg_types=arg_types if arg_types is not _dummy else self.arg_types,
            arg_kinds=arg_kinds if arg_kinds is not _dummy else self.arg_kinds,
            arg_names=arg_names if arg_names is not _dummy else self.arg_names,
            is_ellipsis_args=(
                is_ellipsis_args if is_ellipsis_args is not _dummy else self.is_ellipsis_args
            ),
            variables=variables if variables is not _dummy else self.variables,
            imprecise_arg_kinds=(
                imprecise_arg_kinds
                if imprecise_arg_kinds is not _dummy
                else self.imprecise_arg_kinds
            ),
        )

    # TODO: here is a lot of code duplication with Callable type, fix this.
    def var_arg(self) -> FormalArgument | None:
        """The formal argument for *args."""
        for position, (type, kind) in enumerate(zip(self.arg_types, self.arg_kinds)):
            if kind == ARG_STAR:
                return FormalArgument(None, position, type, False)
        return None

    def kw_arg(self) -> FormalArgument | None:
        """The formal argument for **kwargs."""
        for position, (type, kind) in enumerate(zip(self.arg_types, self.arg_kinds)):
            if kind == ARG_STAR2:
                return FormalArgument(None, position, type, False)
        return None

    def formal_arguments(self, include_star_args: bool = False) -> list[FormalArgument]:
        """Yields the formal arguments corresponding to this callable, ignoring *arg and **kwargs.

        To handle *args and **kwargs, use the 'callable.var_args' and 'callable.kw_args' fields,
        if they are not None.

        If you really want to include star args in the yielded output, set the
        'include_star_args' parameter to 'True'."""
        args = []
        done_with_positional = False
        for i in range(len(self.arg_types)):
            kind = self.arg_kinds[i]
            if kind.is_named() or kind.is_star():
                done_with_positional = True
            if not include_star_args and kind.is_star():
                continue

            required = kind.is_required()
            pos = None if done_with_positional else i
            arg = FormalArgument(self.arg_names[i], pos, self.arg_types[i], required)
            args.append(arg)
        return args

    def argument_by_name(self, name: str | None) -> FormalArgument | None:
        if name is None:
            return None
        seen_star = False
        for i, (arg_name, kind, typ) in enumerate(
            zip(self.arg_names, self.arg_kinds, self.arg_types)
        ):
            # No more positional arguments after these.
            if kind.is_named() or kind.is_star():
                seen_star = True
            if kind.is_star():
                continue
            if arg_name == name:
                position = None if seen_star else i
                return FormalArgument(name, position, typ, kind.is_required())
        return self.try_synthesizing_arg_from_kwarg(name)

    def argument_by_position(self, position: int | None) -> FormalArgument | None:
        if position is None:
            return None
        if position >= len(self.arg_names):
            return self.try_synthesizing_arg_from_vararg(position)
        name, kind, typ = (
            self.arg_names[position],
            self.arg_kinds[position],
            self.arg_types[position],
        )
        if kind.is_positional():
            return FormalArgument(name, position, typ, kind == ARG_POS)
        else:
            return self.try_synthesizing_arg_from_vararg(position)

    def try_synthesizing_arg_from_kwarg(self, name: str | None) -> FormalArgument | None:
        kw_arg = self.kw_arg()
        if kw_arg is not None:
            return FormalArgument(name, None, kw_arg.typ, False)
        else:
            return None

    def try_synthesizing_arg_from_vararg(self, position: int | None) -> FormalArgument | None:
        var_arg = self.var_arg()
        if var_arg is not None:
            return FormalArgument(None, position, var_arg.typ, False)
        else:
            return None

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_parameters(self)

    def serialize(self) -> JsonDict:
        return {
            ".class": "Parameters",
            "arg_types": [t.serialize() for t in self.arg_types],
            "arg_kinds": [int(x.value) for x in self.arg_kinds],
            "arg_names": self.arg_names,
            "variables": [tv.serialize() for tv in self.variables],
            "imprecise_arg_kinds": self.imprecise_arg_kinds,
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> Parameters:
        assert data[".class"] == "Parameters"
        return Parameters(
            [deserialize_type(t) for t in data["arg_types"]],
            [ArgKind(x) for x in data["arg_kinds"]],
            data["arg_names"],
            variables=[cast(TypeVarLikeType, deserialize_type(v)) for v in data["variables"]],
            imprecise_arg_kinds=data["imprecise_arg_kinds"],
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.is_ellipsis_args,
                tuple(self.arg_types),
                tuple(self.arg_names),
                tuple(self.arg_kinds),
            )
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (Parameters, CallableType)):
            return (
                self.arg_types == other.arg_types
                and self.arg_names == other.arg_names
                and self.arg_kinds == other.arg_kinds
                and self.is_ellipsis_args == other.is_ellipsis_args
            )
        else:
            return NotImplemented


CT = TypeVar("CT", bound="CallableType")


class CallableType(FunctionLike):
    """Type of a non-overloaded callable object (such as function)."""

    __slots__ = (
        "arg_types",  # Types of function arguments
        "arg_kinds",  # ARG_ constants
        "arg_names",  # Argument names; None if not a keyword argument
        "min_args",  # Minimum number of arguments; derived from arg_kinds
        "ret_type",  # Return value type
        "name",  # Name (may be None; for error messages and plugins)
        "definition",  # For error messages.  May be None.
        "variables",  # Type variables for a generic function
        "is_ellipsis_args",  # Is this Callable[..., t] (with literal '...')?
        "implicit",  # Was this type implicitly generated instead of explicitly
        # specified by the user?
        "special_sig",  # Non-None for signatures that require special handling
        # (currently only value is 'dict' for a signature similar to
        # 'dict')
        "from_type_type",  # Was this callable generated by analyzing Type[...]
        # instantiation?
        "bound_args",  # Bound type args, mostly unused but may be useful for
        # tools that consume mypy ASTs
        "def_extras",  # Information about original definition we want to serialize.
        # This is used for more detailed error messages.
        "type_guard",  # T, if -> TypeGuard[T] (ret_type is bool in this case).
        "type_is",  # T, if -> TypeIs[T] (ret_type is bool in this case).
        "from_concatenate",  # whether this callable is from a concatenate object
        # (this is used for error messages)
        "imprecise_arg_kinds",
        "unpack_kwargs",  # Was an Unpack[...] with **kwargs used to define this callable?
    )

    def __init__(
        self,
        # maybe this should be refactored to take a Parameters object
        arg_types: Sequence[Type],
        arg_kinds: list[ArgKind],
        arg_names: Sequence[str | None],
        ret_type: Type,
        fallback: Instance,
        name: str | None = None,
        definition: SymbolNode | None = None,
        variables: Sequence[TypeVarLikeType] | None = None,
        line: int = -1,
        column: int = -1,
        is_ellipsis_args: bool = False,
        implicit: bool = False,
        special_sig: str | None = None,
        from_type_type: bool = False,
        bound_args: Sequence[Type | None] = (),
        def_extras: dict[str, Any] | None = None,
        type_guard: Type | None = None,
        type_is: Type | None = None,
        from_concatenate: bool = False,
        imprecise_arg_kinds: bool = False,
        unpack_kwargs: bool = False,
    ) -> None:
        super().__init__(line, column)
        assert len(arg_types) == len(arg_kinds) == len(arg_names)
        for t, k in zip(arg_types, arg_kinds):
            if isinstance(t, ParamSpecType):
                assert not t.prefix.arg_types
                # TODO: should we assert that only ARG_STAR contain ParamSpecType?
                # See testParamSpecJoin, that relies on passing e.g `P.args` as plain argument.
        if variables is None:
            variables = []
        self.arg_types = list(arg_types)
        self.arg_kinds = arg_kinds
        self.arg_names = list(arg_names)
        self.min_args = arg_kinds.count(ARG_POS)
        self.ret_type = ret_type
        self.fallback = fallback
        assert not name or "<bound method" not in name
        self.name = name
        self.definition = definition
        self.variables = variables
        self.is_ellipsis_args = is_ellipsis_args
        self.implicit = implicit
        self.special_sig = special_sig
        self.from_type_type = from_type_type
        self.from_concatenate = from_concatenate
        self.imprecise_arg_kinds = imprecise_arg_kinds
        if not bound_args:
            bound_args = ()
        self.bound_args = bound_args
        if def_extras:
            self.def_extras = def_extras
        elif isinstance(definition, FuncDef):
            # This information would be lost if we don't have definition
            # after serialization, but it is useful in error messages.
            # TODO: decide how to add more info here (file, line, column)
            # without changing interface hash.
            first_arg: str | None = None
            if definition.arg_names and definition.info and not definition.is_static:
                if getattr(definition, "arguments", None):
                    first_arg = definition.arguments[0].variable.name
                else:
                    first_arg = definition.arg_names[0]
            self.def_extras = {"first_arg": first_arg}
        else:
            self.def_extras = {}
        self.type_guard = type_guard
        self.type_is = type_is
        self.unpack_kwargs = unpack_kwargs

    def copy_modified(
        self: CT,
        arg_types: Bogus[Sequence[Type]] = _dummy,
        arg_kinds: Bogus[list[ArgKind]] = _dummy,
        arg_names: Bogus[Sequence[str | None]] = _dummy,
        ret_type: Bogus[Type] = _dummy,
        fallback: Bogus[Instance] = _dummy,
        name: Bogus[str | None] = _dummy,
        definition: Bogus[SymbolNode] = _dummy,
        variables: Bogus[Sequence[TypeVarLikeType]] = _dummy,
        line: int = _dummy_int,
        column: int = _dummy_int,
        is_ellipsis_args: Bogus[bool] = _dummy,
        implicit: Bogus[bool] = _dummy,
        special_sig: Bogus[str | None] = _dummy,
        from_type_type: Bogus[bool] = _dummy,
        bound_args: Bogus[list[Type | None]] = _dummy,
        def_extras: Bogus[dict[str, Any]] = _dummy,
        type_guard: Bogus[Type | None] = _dummy,
        type_is: Bogus[Type | None] = _dummy,
        from_concatenate: Bogus[bool] = _dummy,
        imprecise_arg_kinds: Bogus[bool] = _dummy,
        unpack_kwargs: Bogus[bool] = _dummy,
    ) -> CT:
        modified = CallableType(
            arg_types=arg_types if arg_types is not _dummy else self.arg_types,
            arg_kinds=arg_kinds if arg_kinds is not _dummy else self.arg_kinds,
            arg_names=arg_names if arg_names is not _dummy else self.arg_names,
            ret_type=ret_type if ret_type is not _dummy else self.ret_type,
            fallback=fallback if fallback is not _dummy else self.fallback,
            name=name if name is not _dummy else self.name,
            definition=definition if definition is not _dummy else self.definition,
            variables=variables if variables is not _dummy else self.variables,
            line=line if line != _dummy_int else self.line,
            column=column if column != _dummy_int else self.column,
            is_ellipsis_args=(
                is_ellipsis_args if is_ellipsis_args is not _dummy else self.is_ellipsis_args
            ),
            implicit=implicit if implicit is not _dummy else self.implicit,
            special_sig=special_sig if special_sig is not _dummy else self.special_sig,
            from_type_type=from_type_type if from_type_type is not _dummy else self.from_type_type,
            bound_args=bound_args if bound_args is not _dummy else self.bound_args,
            def_extras=def_extras if def_extras is not _dummy else dict(self.def_extras),
            type_guard=type_guard if type_guard is not _dummy else self.type_guard,
            type_is=type_is if type_is is not _dummy else self.type_is,
            from_concatenate=(
                from_concatenate if from_concatenate is not _dummy else self.from_concatenate
            ),
            imprecise_arg_kinds=(
                imprecise_arg_kinds
                if imprecise_arg_kinds is not _dummy
                else self.imprecise_arg_kinds
            ),
            unpack_kwargs=unpack_kwargs if unpack_kwargs is not _dummy else self.unpack_kwargs,
        )
        # Optimization: Only NewTypes are supported as subtypes since
        # the class is effectively final, so we can use a cast safely.
        return cast(CT, modified)

    def var_arg(self) -> FormalArgument | None:
        """The formal argument for *args."""
        for position, (type, kind) in enumerate(zip(self.arg_types, self.arg_kinds)):
            if kind == ARG_STAR:
                return FormalArgument(None, position, type, False)
        return None

    def kw_arg(self) -> FormalArgument | None:
        """The formal argument for **kwargs."""
        for position, (type, kind) in enumerate(zip(self.arg_types, self.arg_kinds)):
            if kind == ARG_STAR2:
                return FormalArgument(None, position, type, False)
        return None

    @property
    def is_var_arg(self) -> bool:
        """Does this callable have a *args argument?"""
        return ARG_STAR in self.arg_kinds

    @property
    def is_kw_arg(self) -> bool:
        """Does this callable have a **kwargs argument?"""
        return ARG_STAR2 in self.arg_kinds

    def is_type_obj(self) -> bool:
        return self.fallback.type.is_metaclass() and not isinstance(
            get_proper_type(self.ret_type), UninhabitedType
        )

    def type_object(self) -> mypy.nodes.TypeInfo:
        assert self.is_type_obj()
        ret = get_proper_type(self.ret_type)
        if isinstance(ret, TypeVarType):
            ret = get_proper_type(ret.upper_bound)
        if isinstance(ret, TupleType):
            ret = ret.partial_fallback
        if isinstance(ret, TypedDictType):
            ret = ret.fallback
        assert isinstance(ret, Instance)
        return ret.type

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_callable_type(self)

    def with_name(self, name: str) -> CallableType:
        """Return a copy of this type with the specified name."""
        return self.copy_modified(ret_type=self.ret_type, name=name)

    def get_name(self) -> str | None:
        return self.name

    def max_possible_positional_args(self) -> int:
        """Returns maximum number of positional arguments this method could possibly accept.

        This takes into account *arg and **kwargs but excludes keyword-only args."""
        if self.is_var_arg or self.is_kw_arg:
            return sys.maxsize
        return sum(kind.is_positional() for kind in self.arg_kinds)

    def formal_arguments(self, include_star_args: bool = False) -> list[FormalArgument]:
        """Return a list of the formal arguments of this callable, ignoring *arg and **kwargs.

        To handle *args and **kwargs, use the 'callable.var_args' and 'callable.kw_args' fields,
        if they are not None.

        If you really want to include star args in the yielded output, set the
        'include_star_args' parameter to 'True'."""
        args = []
        done_with_positional = False
        for i in range(len(self.arg_types)):
            kind = self.arg_kinds[i]
            if kind.is_named() or kind.is_star():
                done_with_positional = True
            if not include_star_args and kind.is_star():
                continue

            required = kind.is_required()
            pos = None if done_with_positional else i
            arg = FormalArgument(self.arg_names[i], pos, self.arg_types[i], required)
            args.append(arg)
        return args

    def argument_by_name(self, name: str | None) -> FormalArgument | None:
        if name is None:
            return None
        seen_star = False
        for i, (arg_name, kind, typ) in enumerate(
            zip(self.arg_names, self.arg_kinds, self.arg_types)
        ):
            # No more positional arguments after these.
            if kind.is_named() or kind.is_star():
                seen_star = True
            if kind.is_star():
                continue
            if arg_name == name:
                position = None if seen_star else i
                return FormalArgument(name, position, typ, kind.is_required())
        return self.try_synthesizing_arg_from_kwarg(name)

    def argument_by_position(self, position: int | None) -> FormalArgument | None:
        if position is None:
            return None
        if position >= len(self.arg_names):
            return self.try_synthesizing_arg_from_vararg(position)
        name, kind, typ = (
            self.arg_names[position],
            self.arg_kinds[position],
            self.arg_types[position],
        )
        if kind.is_positional():
            return FormalArgument(name, position, typ, kind == ARG_POS)
        else:
            return self.try_synthesizing_arg_from_vararg(position)

    def try_synthesizing_arg_from_kwarg(self, name: str | None) -> FormalArgument | None:
        kw_arg = self.kw_arg()
        if kw_arg is not None:
            return FormalArgument(name, None, kw_arg.typ, False)
        else:
            return None

    def try_synthesizing_arg_from_vararg(self, position: int | None) -> FormalArgument | None:
        var_arg = self.var_arg()
        if var_arg is not None:
            return FormalArgument(None, position, var_arg.typ, False)
        else:
            return None

    @property
    def items(self) -> list[CallableType]:
        return [self]

    def is_generic(self) -> bool:
        return bool(self.variables)

    def type_var_ids(self) -> list[TypeVarId]:
        a: list[TypeVarId] = []
        for tv in self.variables:
            a.append(tv.id)
        return a

    def param_spec(self) -> ParamSpecType | None:
        """Return ParamSpec if callable can be called with one.

        A Callable accepting ParamSpec P args (*args, **kwargs) must have the
        two final parameters like this: *args: P.args, **kwargs: P.kwargs.
        """
        if len(self.arg_types) < 2:
            return None
        if self.arg_kinds[-2] != ARG_STAR or self.arg_kinds[-1] != ARG_STAR2:
            return None
        arg_type = self.arg_types[-2]
        if not isinstance(arg_type, ParamSpecType):
            return None

        # Prepend prefix for def f(prefix..., *args: P.args, **kwargs: P.kwargs) -> ...
        # TODO: confirm that all arg kinds are positional
        prefix = Parameters(self.arg_types[:-2], self.arg_kinds[:-2], self.arg_names[:-2])
        return arg_type.copy_modified(flavor=ParamSpecFlavor.BARE, prefix=prefix)

    def with_unpacked_kwargs(self) -> NormalizedCallableType:
        if not self.unpack_kwargs:
            return cast(NormalizedCallableType, self)
        last_type = get_proper_type(self.arg_types[-1])
        assert isinstance(last_type, TypedDictType)
        extra_kinds = [
            ArgKind.ARG_NAMED if name in last_type.required_keys else ArgKind.ARG_NAMED_OPT
            for name in last_type.items
        ]
        new_arg_kinds = self.arg_kinds[:-1] + extra_kinds
        new_arg_names = self.arg_names[:-1] + list(last_type.items)
        new_arg_types = self.arg_types[:-1] + list(last_type.items.values())
        return NormalizedCallableType(
            self.copy_modified(
                arg_kinds=new_arg_kinds,
                arg_names=new_arg_names,
                arg_types=new_arg_types,
                unpack_kwargs=False,
            )
        )

    def with_normalized_var_args(self) -> Self:
        var_arg = self.var_arg()
        if not var_arg or not isinstance(var_arg.typ, UnpackType):
            return self
        unpacked = get_proper_type(var_arg.typ.type)
        if not isinstance(unpacked, TupleType):
            # Note that we don't normalize *args: *tuple[X, ...] -> *args: X,
            # this should be done once in semanal_typeargs.py for user-defined types,
            # and we ourselves should never construct such type.
            return self
        unpack_index = find_unpack_in_list(unpacked.items)
        if unpack_index == 0 and len(unpacked.items) > 1:
            # Already normalized.
            return self

        # Boilerplate:
        var_arg_index = self.arg_kinds.index(ARG_STAR)
        types_prefix = self.arg_types[:var_arg_index]
        kinds_prefix = self.arg_kinds[:var_arg_index]
        names_prefix = self.arg_names[:var_arg_index]
        types_suffix = self.arg_types[var_arg_index + 1 :]
        kinds_suffix = self.arg_kinds[var_arg_index + 1 :]
        names_suffix = self.arg_names[var_arg_index + 1 :]
        no_name: str | None = None  # to silence mypy

        # Now we have something non-trivial to do.
        if unpack_index is None:
            # Plain *Tuple[X, Y, Z] -> replace with ARG_POS completely
            types_middle = unpacked.items
            kinds_middle = [ARG_POS] * len(unpacked.items)
            names_middle = [no_name] * len(unpacked.items)
        else:
            # *Tuple[X, *Ts, Y, Z] or *Tuple[X, *tuple[T, ...], X, Z], here
            # we replace the prefix by ARG_POS (this is how some places expect
            # Callables to be represented)
            nested_unpack = unpacked.items[unpack_index]
            assert isinstance(nested_unpack, UnpackType)
            nested_unpacked = get_proper_type(nested_unpack.type)
            if unpack_index == len(unpacked.items) - 1:
                # Normalize also single item tuples like
                #   *args: *Tuple[*tuple[X, ...]] -> *args: X
                #   *args: *Tuple[*Ts] -> *args: *Ts
                # This may be not strictly necessary, but these are very verbose.
                if isinstance(nested_unpacked, Instance):
                    assert nested_unpacked.type.fullname == "builtins.tuple"
                    new_unpack = nested_unpacked.args[0]
                else:
                    if not isinstance(nested_unpacked, TypeVarTupleType):
                        # We found a non-nomralized tuple type, this means this method
                        # is called during semantic analysis (e.g. from get_proper_type())
                        # there is no point in normalizing callables at this stage.
                        return self
                    new_unpack = nested_unpack
            else:
                new_unpack = UnpackType(
                    unpacked.copy_modified(items=unpacked.items[unpack_index:])
                )
            types_middle = unpacked.items[:unpack_index] + [new_unpack]
            kinds_middle = [ARG_POS] * unpack_index + [ARG_STAR]
            names_middle = [no_name] * unpack_index + [self.arg_names[var_arg_index]]
        return self.copy_modified(
            arg_types=types_prefix + types_middle + types_suffix,
            arg_kinds=kinds_prefix + kinds_middle + kinds_suffix,
            arg_names=names_prefix + names_middle + names_suffix,
        )

    def __hash__(self) -> int:
        # self.is_type_obj() will fail if self.fallback.type is a FakeInfo
        if isinstance(self.fallback.type, FakeInfo):
            is_type_obj = 2
        else:
            is_type_obj = self.is_type_obj()
        return hash(
            (
                self.ret_type,
                is_type_obj,
                self.is_ellipsis_args,
                self.name,
                tuple(self.arg_types),
                tuple(self.arg_names),
                tuple(self.arg_kinds),
                self.fallback,
            )
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CallableType):
            return (
                self.ret_type == other.ret_type
                and self.arg_types == other.arg_types
                and self.arg_names == other.arg_names
                and self.arg_kinds == other.arg_kinds
                and self.name == other.name
                and self.is_type_obj() == other.is_type_obj()
                and self.is_ellipsis_args == other.is_ellipsis_args
                and self.fallback == other.fallback
            )
        else:
            return NotImplemented

    def serialize(self) -> JsonDict:
        # TODO: As an optimization, leave out everything related to
        # generic functions for non-generic functions.
        return {
            ".class": "CallableType",
            "arg_types": [t.serialize() for t in self.arg_types],
            "arg_kinds": [int(x.value) for x in self.arg_kinds],
            "arg_names": self.arg_names,
            "ret_type": self.ret_type.serialize(),
            "fallback": self.fallback.serialize(),
            "name": self.name,
            # We don't serialize the definition (only used for error messages).
            "variables": [v.serialize() for v in self.variables],
            "is_ellipsis_args": self.is_ellipsis_args,
            "implicit": self.implicit,
            "bound_args": [(None if t is None else t.serialize()) for t in self.bound_args],
            "def_extras": dict(self.def_extras),
            "type_guard": self.type_guard.serialize() if self.type_guard is not None else None,
            "type_is": (self.type_is.serialize() if self.type_is is not None else None),
            "from_concatenate": self.from_concatenate,
            "imprecise_arg_kinds": self.imprecise_arg_kinds,
            "unpack_kwargs": self.unpack_kwargs,
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> CallableType:
        assert data[".class"] == "CallableType"
        # TODO: Set definition to the containing SymbolNode?
        return CallableType(
            [deserialize_type(t) for t in data["arg_types"]],
            [ArgKind(x) for x in data["arg_kinds"]],
            data["arg_names"],
            deserialize_type(data["ret_type"]),
            Instance.deserialize(data["fallback"]),
            name=data["name"],
            variables=[cast(TypeVarLikeType, deserialize_type(v)) for v in data["variables"]],
            is_ellipsis_args=data["is_ellipsis_args"],
            implicit=data["implicit"],
            bound_args=[(None if t is None else deserialize_type(t)) for t in data["bound_args"]],
            def_extras=data["def_extras"],
            type_guard=(
                deserialize_type(data["type_guard"]) if data["type_guard"] is not None else None
            ),
            type_is=(deserialize_type(data["type_is"]) if data["type_is"] is not None else None),
            from_concatenate=data["from_concatenate"],
            imprecise_arg_kinds=data["imprecise_arg_kinds"],
            unpack_kwargs=data["unpack_kwargs"],
        )


# This is a little safety net to prevent reckless special-casing of callables
# that can potentially break Unpack[...] with **kwargs.
# TODO: use this in more places in checkexpr.py etc?
NormalizedCallableType = NewType("NormalizedCallableType", CallableType)


class Overloaded(FunctionLike):
    """Overloaded function type T1, ... Tn, where each Ti is CallableType.

    The variant to call is chosen based on static argument
    types. Overloaded function types can only be defined in stub
    files, and thus there is no explicit runtime dispatch
    implementation.
    """

    __slots__ = ("_items",)

    _items: list[CallableType]  # Must not be empty

    def __init__(self, items: list[CallableType]) -> None:
        super().__init__(items[0].line, items[0].column)
        self._items = items
        self.fallback = items[0].fallback

    @property
    def items(self) -> list[CallableType]:
        return self._items

    def name(self) -> str | None:
        return self.get_name()

    def is_type_obj(self) -> bool:
        # All the items must have the same type object status, so it's
        # sufficient to query only (any) one of them.
        return self._items[0].is_type_obj()

    def type_object(self) -> mypy.nodes.TypeInfo:
        # All the items must have the same type object, so it's sufficient to
        # query only (any) one of them.
        return self._items[0].type_object()

    def with_name(self, name: str) -> Overloaded:
        ni: list[CallableType] = []
        for it in self._items:
            ni.append(it.with_name(name))
        return Overloaded(ni)

    def get_name(self) -> str | None:
        return self._items[0].name

    def with_unpacked_kwargs(self) -> Overloaded:
        if any(i.unpack_kwargs for i in self.items):
            return Overloaded([i.with_unpacked_kwargs() for i in self.items])
        return self

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_overloaded(self)

    def __hash__(self) -> int:
        return hash(tuple(self.items))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Overloaded):
            return NotImplemented
        return self.items == other.items

    def serialize(self) -> JsonDict:
        return {".class": "Overloaded", "items": [t.serialize() for t in self.items]}

    @classmethod
    def deserialize(cls, data: JsonDict) -> Overloaded:
        assert data[".class"] == "Overloaded"
        return Overloaded([CallableType.deserialize(t) for t in data["items"]])


class TupleType(ProperType):
    """The tuple type Tuple[T1, ..., Tn] (at least one type argument).

    Instance variables:
        items: Tuple item types
        partial_fallback: The (imprecise) underlying instance type that is used
            for non-tuple methods. This is generally builtins.tuple[Any, ...] for
            regular tuples, but it's different for named tuples and classes with
            a tuple base class. Use mypy.typeops.tuple_fallback to calculate the
            precise fallback type derived from item types.
        implicit: If True, derived from a tuple expression (t,....) instead of Tuple[t, ...]
    """

    __slots__ = ("items", "partial_fallback", "implicit")

    items: list[Type]
    partial_fallback: Instance
    implicit: bool

    def __init__(
        self,
        items: list[Type],
        fallback: Instance,
        line: int = -1,
        column: int = -1,
        implicit: bool = False,
    ) -> None:
        super().__init__(line, column)
        self.partial_fallback = fallback
        self.items = items
        self.implicit = implicit

    def can_be_true_default(self) -> bool:
        if self.can_be_any_bool():
            # Corner case: it is a `NamedTuple` with `__bool__` method defined.
            # It can be anything: both `True` and `False`.
            return True
        return self.length() > 0

    def can_be_false_default(self) -> bool:
        if self.can_be_any_bool():
            # Corner case: it is a `NamedTuple` with `__bool__` method defined.
            # It can be anything: both `True` and `False`.
            return True
        if self.length() == 0:
            return True
        if self.length() > 1:
            return False
        # Special case tuple[*Ts] may or may not be false.
        item = self.items[0]
        if not isinstance(item, UnpackType):
            return False
        if not isinstance(item.type, TypeVarTupleType):
            # Non-normalized tuple[int, ...] can be false.
            return True
        return item.type.min_len == 0

    def can_be_any_bool(self) -> bool:
        return bool(
            self.partial_fallback.type
            and self.partial_fallback.type.fullname != "builtins.tuple"
            and self.partial_fallback.type.names.get("__bool__")
        )

    def length(self) -> int:
        return len(self.items)

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_tuple_type(self)

    def __hash__(self) -> int:
        return hash((tuple(self.items), self.partial_fallback))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TupleType):
            return NotImplemented
        return self.items == other.items and self.partial_fallback == other.partial_fallback

    def serialize(self) -> JsonDict:
        return {
            ".class": "TupleType",
            "items": [t.serialize() for t in self.items],
            "partial_fallback": self.partial_fallback.serialize(),
            "implicit": self.implicit,
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> TupleType:
        assert data[".class"] == "TupleType"
        return TupleType(
            [deserialize_type(t) for t in data["items"]],
            Instance.deserialize(data["partial_fallback"]),
            implicit=data["implicit"],
        )

    def copy_modified(
        self, *, fallback: Instance | None = None, items: list[Type] | None = None
    ) -> TupleType:
        if fallback is None:
            fallback = self.partial_fallback
        if items is None:
            items = self.items
        return TupleType(items, fallback, self.line, self.column)

    def slice(
        self, begin: int | None, end: int | None, stride: int | None, *, fallback: Instance | None
    ) -> TupleType | None:
        if fallback is None:
            fallback = self.partial_fallback

        if any(isinstance(t, UnpackType) for t in self.items):
            total = len(self.items)
            unpack_index = find_unpack_in_list(self.items)
            assert unpack_index is not None
            if begin is None and end is None:
                # We special-case this to support reversing variadic tuples.
                # General support for slicing is tricky, so we handle only simple cases.
                if stride == -1:
                    slice_items = self.items[::-1]
                elif stride is None or stride == 1:
                    slice_items = self.items
                else:
                    return None
            elif (begin is None or unpack_index >= begin >= 0) and (
                end is not None and unpack_index >= end >= 0
            ):
                # Start and end are in the prefix, everything works in this case.
                slice_items = self.items[begin:end:stride]
            elif (begin is not None and unpack_index - total < begin < 0) and (
                end is None or unpack_index - total < end < 0
            ):
                # Start and end are in the suffix, everything works in this case.
                slice_items = self.items[begin:end:stride]
            elif (begin is None or unpack_index >= begin >= 0) and (
                end is None or unpack_index - total < end < 0
            ):
                # Start in the prefix, end in the suffix, we can support only trivial strides.
                if stride is None or stride == 1:
                    slice_items = self.items[begin:end:stride]
                else:
                    return None
            elif (begin is not None and unpack_index - total < begin < 0) and (
                end is not None and unpack_index >= end >= 0
            ):
                # Start in the suffix, end in the prefix, we can support only trivial strides.
                if stride is None or stride == -1:
                    slice_items = self.items[begin:end:stride]
                else:
                    return None
            else:
                # TODO: there some additional cases we can support for homogeneous variadic
                # items, we can "eat away" finite number of items.
                return None
        else:
            slice_items = self.items[begin:end:stride]
        return TupleType(slice_items, fallback, self.line, self.column, self.implicit)


class TypedDictType(ProperType):
    """Type of TypedDict object {'k1': v1, ..., 'kn': vn}.

    A TypedDict object is a dictionary with specific string (literal) keys. Each
    key has a value with a distinct type that depends on the key. TypedDict objects
    are normal dict objects at runtime.

    A TypedDictType can be either named or anonymous. If it's anonymous, its
    fallback will be typing_extensions._TypedDict (Instance). _TypedDict is a subclass
    of Mapping[str, object] and defines all non-mapping dict methods that TypedDict
    supports. Some dict methods are unsafe and not supported. _TypedDict isn't defined
    at runtime.

    If a TypedDict is named, its fallback will be an Instance of the named type
    (ex: "Point") whose TypeInfo has a typeddict_type that is anonymous. This
    is similar to how named tuples work.

    TODO: The fallback structure is perhaps overly complicated.
    """

    __slots__ = ("items", "required_keys", "fallback")

    items: dict[str, Type]  # item_name -> item_type
    required_keys: set[str]
    fallback: Instance

    def __init__(
        self,
        items: dict[str, Type],
        required_keys: set[str],
        fallback: Instance,
        line: int = -1,
        column: int = -1,
    ) -> None:
        super().__init__(line, column)
        self.items = items
        self.required_keys = required_keys
        self.fallback = fallback
        self.can_be_true = len(self.items) > 0
        self.can_be_false = len(self.required_keys) == 0

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_typeddict_type(self)

    def __hash__(self) -> int:
        return hash((frozenset(self.items.items()), self.fallback, frozenset(self.required_keys)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TypedDictType):
            return NotImplemented

        return (
            frozenset(self.items.keys()) == frozenset(other.items.keys())
            and all(
                left_item_type == right_item_type
                for (_, left_item_type, right_item_type) in self.zip(other)
            )
            and self.fallback == other.fallback
            and self.required_keys == other.required_keys
        )

    def serialize(self) -> JsonDict:
        return {
            ".class": "TypedDictType",
            "items": [[n, t.serialize()] for (n, t) in self.items.items()],
            "required_keys": sorted(self.required_keys),
            "fallback": self.fallback.serialize(),
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> TypedDictType:
        assert data[".class"] == "TypedDictType"
        return TypedDictType(
            {n: deserialize_type(t) for (n, t) in data["items"]},
            set(data["required_keys"]),
            Instance.deserialize(data["fallback"]),
        )

    @property
    def is_final(self) -> bool:
        return self.fallback.type.is_final

    def is_anonymous(self) -> bool:
        return self.fallback.type.fullname in TPDICT_FB_NAMES

    def as_anonymous(self) -> TypedDictType:
        if self.is_anonymous():
            return self
        assert self.fallback.type.typeddict_type is not None
        return self.fallback.type.typeddict_type.as_anonymous()

    def copy_modified(
        self,
        *,
        fallback: Instance | None = None,
        item_types: list[Type] | None = None,
        item_names: list[str] | None = None,
        required_keys: set[str] | None = None,
    ) -> TypedDictType:
        if fallback is None:
            fallback = self.fallback
        if item_types is None:
            items = self.items
        else:
            items = dict(zip(self.items, item_types))
        if required_keys is None:
            required_keys = self.required_keys
        if item_names is not None:
            items = {k: v for (k, v) in items.items() if k in item_names}
            required_keys &= set(item_names)
        return TypedDictType(items, required_keys, fallback, self.line, self.column)

    def create_anonymous_fallback(self) -> Instance:
        anonymous = self.as_anonymous()
        return anonymous.fallback

    def names_are_wider_than(self, other: TypedDictType) -> bool:
        return len(other.items.keys() - self.items.keys()) == 0

    def zip(self, right: TypedDictType) -> Iterable[tuple[str, Type, Type]]:
        left = self
        for item_name, left_item_type in left.items.items():
            right_item_type = right.items.get(item_name)
            if right_item_type is not None:
                yield (item_name, left_item_type, right_item_type)

    def zipall(self, right: TypedDictType) -> Iterable[tuple[str, Type | None, Type | None]]:
        left = self
        for item_name, left_item_type in left.items.items():
            right_item_type = right.items.get(item_name)
            yield (item_name, left_item_type, right_item_type)
        for item_name, right_item_type in right.items.items():
            if item_name in left.items:
                continue
            yield (item_name, None, right_item_type)


class RawExpressionType(ProperType):
    """A synthetic type representing some arbitrary expression that does not cleanly
    translate into a type.

    This synthetic type is only used at the beginning stages of semantic analysis
    and should be completely removing during the process for mapping UnboundTypes to
    actual types: we turn it into its "node" argument, a LiteralType, or an AnyType.

    For example, suppose `Foo[1]` is initially represented as the following:

        UnboundType(
            name='Foo',
            args=[
                RawExpressionType(value=1, base_type_name='builtins.int'),
            ],
        )

    As we perform semantic analysis, this type will transform into one of two
    possible forms.

    If 'Foo' was an alias for 'Literal' all along, this type is transformed into:

        LiteralType(value=1, fallback=int_instance_here)

    Alternatively, if 'Foo' is an unrelated class, we report an error and instead
    produce something like this:

        Instance(type=typeinfo_for_foo, args=[AnyType(TypeOfAny.from_error))

    If the "note" field is not None, the provided note will be reported alongside the
    error at this point.

    Note: if "literal_value" is None, that means this object is representing some
    expression that cannot possibly be a parameter of Literal[...]. For example,
    "Foo[3j]" would be represented as:

        UnboundType(
            name='Foo',
            args=[
                RawExpressionType(value=None, base_type_name='builtins.complex'),
            ],
        )
    """

    __slots__ = ("literal_value", "base_type_name", "note", "node")

    def __init__(
        self,
        literal_value: LiteralValue | None,
        base_type_name: str,
        line: int = -1,
        column: int = -1,
        note: str | None = None,
        node: Type | None = None,
    ) -> None:
        super().__init__(line, column)
        self.literal_value = literal_value
        self.base_type_name = base_type_name
        self.note = note
        self.node = node

    def simple_name(self) -> str:
        return self.base_type_name.replace("builtins.", "")

    def accept(self, visitor: TypeVisitor[T]) -> T:
        assert isinstance(visitor, SyntheticTypeVisitor)
        ret: T = visitor.visit_raw_expression_type(self)
        return ret

    def copy_modified(self, node: Type | None) -> RawExpressionType:
        return RawExpressionType(
            literal_value=self.literal_value,
            base_type_name=self.base_type_name,
            line=self.line,
            column=self.column,
            note=self.note,
            node=node,
        )

    def resolve_string_annotation(self) -> Type:
        if self.node is not None:
            return self.node.resolve_string_annotation()
        return self

    def serialize(self) -> JsonDict:
        assert False, "Synthetic types don't serialize"

    def __hash__(self) -> int:
        return hash((self.literal_value, self.base_type_name))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RawExpressionType):
            return (
                self.base_type_name == other.base_type_name
                and self.literal_value == other.literal_value
                and self.node == other.node
            )
        else:
            return NotImplemented


class LiteralType(ProperType):
    """The type of a Literal instance. Literal[Value]

    A Literal always consists of:

    1. A native Python object corresponding to the contained inner value
    2. A fallback for this Literal. The fallback also corresponds to the
       parent type this Literal subtypes.

    For example, 'Literal[42]' is represented as
    'LiteralType(value=42, fallback=instance_of_int)'

    As another example, `Literal[Color.RED]` (where Color is an enum) is
    represented as `LiteralType(value="RED", fallback=instance_of_color)'.
    """

    __slots__ = ("value", "fallback", "_hash")

    def __init__(
        self, value: LiteralValue, fallback: Instance, line: int = -1, column: int = -1
    ) -> None:
        super().__init__(line, column)
        self.value = value
        self.fallback = fallback
        self._hash = -1  # Cached hash value

    def can_be_false_default(self) -> bool:
        return not self.value

    def can_be_true_default(self) -> bool:
        return bool(self.value)

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_literal_type(self)

    def __hash__(self) -> int:
        if self._hash == -1:
            self._hash = hash((self.value, self.fallback))
        return self._hash

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LiteralType):
            return self.fallback == other.fallback and self.value == other.value
        else:
            return NotImplemented

    def is_enum_literal(self) -> bool:
        return self.fallback.type.is_enum

    def value_repr(self) -> str:
        """Returns the string representation of the underlying type.

        This function is almost equivalent to running `repr(self.value)`,
        except it includes some additional logic to correctly handle cases
        where the value is a string, byte string, a unicode string, or an enum.
        """
        raw = repr(self.value)
        fallback_name = self.fallback.type.fullname

        # If this is backed by an enum,
        if self.is_enum_literal():
            return f"{fallback_name}.{self.value}"

        if fallback_name == "builtins.bytes":
            # Note: 'builtins.bytes' only appears in Python 3, so we want to
            # explicitly prefix with a "b"
            return "b" + raw
        else:
            # 'builtins.str' could mean either depending on context, but either way
            # we don't prefix: it's the "native" string. And of course, if value is
            # some other type, we just return that string repr directly.
            return raw

    def serialize(self) -> JsonDict | str:
        return {
            ".class": "LiteralType",
            "value": self.value,
            "fallback": self.fallback.serialize(),
        }

    @classmethod
    def deserialize(cls, data: JsonDict) -> LiteralType:
        assert data[".class"] == "LiteralType"
        return LiteralType(value=data["value"], fallback=Instance.deserialize(data["fallback"]))

    def is_singleton_type(self) -> bool:
        return self.is_enum_literal() or isinstance(self.value, bool)


class UnionType(ProperType):
    """The union type Union[T1, ..., Tn] (at least one type argument)."""

    __slots__ = ("items", "is_evaluated", "uses_pep604_syntax")

    def __init__(
        self,
        items: Sequence[Type],
        line: int = -1,
        column: int = -1,
        is_evaluated: bool = True,
        uses_pep604_syntax: bool = False,
    ) -> None:
        super().__init__(line, column)
        # We must keep this false to avoid crashes during semantic analysis.
        # TODO: maybe switch this to True during type-checking pass?
        self.items = flatten_nested_unions(items, handle_type_alias_type=False)
        # is_evaluated should be set to false for type comments and string literals
        self.is_evaluated = is_evaluated
        # uses_pep604_syntax is True if Union uses OR syntax (X | Y)
        self.uses_pep604_syntax = uses_pep604_syntax

    def can_be_true_default(self) -> bool:
        return any(item.can_be_true for item in self.items)

    def can_be_false_default(self) -> bool:
        return any(item.can_be_false for item in self.items)

    def __hash__(self) -> int:
        return hash(frozenset(self.items))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UnionType):
            return NotImplemented
        return frozenset(self.items) == frozenset(other.items)

    @overload
    @staticmethod
    def make_union(
        items: Sequence[ProperType], line: int = -1, column: int = -1
    ) -> ProperType: ...

    @overload
    @staticmethod
    def make_union(items: Sequence[Type], line: int = -1, column: int = -1) -> Type: ...

    @staticmethod
    def make_union(items: Sequence[Type], line: int = -1, column: int = -1) -> Type:
        if len(items) > 1:
            return UnionType(items, line, column)
        elif len(items) == 1:
            return items[0]
        else:
            return UninhabitedType()

    def length(self) -> int:
        return len(self.items)

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_union_type(self)

    def relevant_items(self) -> list[Type]:
        """Removes NoneTypes from Unions when strict Optional checking is off."""
        if state.strict_optional:
            return self.items
        else:
            return [i for i in self.items if not isinstance(get_proper_type(i), NoneType)]

    def serialize(self) -> JsonDict:
        return {".class": "UnionType", "items": [t.serialize() for t in self.items]}

    @classmethod
    def deserialize(cls, data: JsonDict) -> UnionType:
        assert data[".class"] == "UnionType"
        return UnionType([deserialize_type(t) for t in data["items"]])


class PartialType(ProperType):
    """Type such as List[?] where type arguments are unknown, or partial None type.

    These are used for inferring types in multiphase initialization such as this:

      x = []       # x gets a partial type List[?], as item type is unknown
      x.append(1)  # partial type gets replaced with normal type List[int]

    Or with None:

      x = None  # x gets a partial type None
      if c:
          x = 1  # Infer actual type int for x
    """

    __slots__ = ("type", "var", "value_type")

    # None for the 'None' partial type; otherwise a generic class
    type: mypy.nodes.TypeInfo | None
    var: mypy.nodes.Var
    # For partial defaultdict[K, V], the type V (K is unknown). If V is generic,
    # the type argument is Any and will be replaced later.
    value_type: Instance | None

    def __init__(
        self,
        type: mypy.nodes.TypeInfo | None,
        var: mypy.nodes.Var,
        value_type: Instance | None = None,
    ) -> None:
        super().__init__()
        self.type = type
        self.var = var
        self.value_type = value_type

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_partial_type(self)


class EllipsisType(ProperType):
    """The type ... (ellipsis).

    This is not a real type but a syntactic AST construct, used in Callable[..., T], for example.

    A semantically analyzed type will never have ellipsis types.
    """

    __slots__ = ()

    def accept(self, visitor: TypeVisitor[T]) -> T:
        assert isinstance(visitor, SyntheticTypeVisitor)
        ret: T = visitor.visit_ellipsis_type(self)
        return ret

    def serialize(self) -> JsonDict:
        assert False, "Synthetic types don't serialize"


class TypeType(ProperType):
    """For types like Type[User].

    This annotates variables that are class objects, constrained by
    the type argument.  See PEP 484 for more details.

    We may encounter expressions whose values are specific classes;
    those are represented as callables (possibly overloaded)
    corresponding to the class's constructor's signature and returning
    an instance of that class.  The difference with Type[C] is that
    those callables always represent the exact class given as the
    return type; Type[C] represents any class that's a subclass of C,
    and C may also be a type variable or a union (or Any).

    Many questions around subtype relationships between Type[C1] and
    def(...) -> C2 are answered by looking at the subtype
    relationships between C1 and C2, since Type[] is considered
    covariant.

    There's an unsolved problem with constructor signatures (also
    unsolved in PEP 484): calling a variable whose type is Type[C]
    assumes the constructor signature for C, even though a subclass of
    C might completely change the constructor signature.  For now we
    just assume that users of Type[C] are careful not to do that (in
    the future we might detect when they are violating that
    assumption).
    """

    __slots__ = ("item",)

    # This can't be everything, but it can be a class reference,
    # a generic class instance, a union, Any, a type variable...
    item: ProperType

    def __init__(
        self,
        item: Bogus[Instance | AnyType | TypeVarType | TupleType | NoneType | CallableType],
        *,
        line: int = -1,
        column: int = -1,
    ) -> None:
        """To ensure Type[Union[A, B]] is always represented as Union[Type[A], Type[B]], item of
        type UnionType must be handled through make_normalized static method.
        """
        super().__init__(line, column)
        self.item = item

    @staticmethod
    def make_normalized(item: Type, *, line: int = -1, column: int = -1) -> ProperType:
        item = get_proper_type(item)
        if isinstance(item, UnionType):
            return UnionType.make_union(
                [TypeType.make_normalized(union_item) for union_item in item.items],
                line=line,
                column=column,
            )
        return TypeType(item, line=line, column=column)  # type: ignore[arg-type]

    def accept(self, visitor: TypeVisitor[T]) -> T:
        return visitor.visit_type_type(self)

    def __hash__(self) -> int:
        return hash(self.item)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TypeType):
            return NotImplemented
        return self.item == other.item

    def serialize(self) -> JsonDict:
        return {".class": "TypeType", "item": self.item.serialize()}

    @classmethod
    def deserialize(cls, data: JsonDict) -> Type:
        assert data[".class"] == "TypeType"
        return TypeType.make_normalized(deserialize_type(data["item"]))


class PlaceholderType(ProperType):
    """Temporary, yet-unknown type during semantic analysis.

    This is needed when there's a reference to a type before the real symbol
    table entry of the target type is available (specifically, we use a
    temporary PlaceholderNode symbol node). Consider this example:

      class str(Sequence[str]): ...

    We use a PlaceholderType for the 'str' in 'Sequence[str]' since we can't create
    a TypeInfo for 'str' until all base classes have been resolved. We'll soon
    perform another analysis iteration which replaces the base class with a complete
    type without any placeholders. After semantic analysis, no placeholder types must
    exist.
    """

    __slots__ = ("fullname", "args")

    def __init__(self, fullname: str | None, args: list[Type], line: int) -> None:
        super().__init__(line)
        self.fullname = fullname  # Must be a valid full name of an actual node (or None).
        self.args = args

    def accept(self, visitor: TypeVisitor[T]) -> T:
        assert isinstance(visitor, SyntheticTypeVisitor)
        ret: T = visitor.visit_placeholder_type(self)
        return ret

    def __hash__(self) -> int:
        return hash((self.fullname, tuple(self.args)))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlaceholderType):
            return NotImplemented
        return self.fullname == other.fullname and self.args == other.args

    def serialize(self) -> str:
        # We should never get here since all placeholders should be replaced
        # during semantic analysis.
        assert False, f"Internal error: unresolved placeholder type {self.fullname}"


@overload
def get_proper_type(typ: None) -> None: ...


@overload
def get_proper_type(typ: Type) -> ProperType: ...


def get_proper_type(typ: Type | None) -> ProperType | None:
    """Get the expansion of a type alias type.

    If the type is already a proper type, this is a no-op. Use this function
    wherever a decision is made on a call like e.g. 'if isinstance(typ, UnionType): ...',
    because 'typ' in this case may be an alias to union. Note: if after making the decision
    on the isinstance() call you pass on the original type (and not one of its components)
    it is recommended to *always* pass on the unexpanded alias.
    """
    if typ is None:
        return None
    if isinstance(typ, TypeGuardedType):  # type: ignore[misc]
        typ = typ.type_guard
    while isinstance(typ, TypeAliasType):
        typ = typ._expand_once()
    # TODO: store the name of original type alias on this type, so we can show it in errors.
    return cast(ProperType, typ)


@overload
def get_proper_types(types: list[Type] | tuple[Type, ...]) -> list[ProperType]:  # type: ignore[overload-overlap]
    ...


@overload
def get_proper_types(
    types: list[Type | None] | tuple[Type | None, ...]
) -> list[ProperType | None]: ...


def get_proper_types(
    types: list[Type] | list[Type | None] | tuple[Type | None, ...]
) -> list[ProperType] | list[ProperType | None]:
    if isinstance(types, list):
        typelist = types
        # Optimize for the common case so that we don't need to allocate anything
        if not any(
            isinstance(t, (TypeAliasType, TypeGuardedType)) for t in typelist  # type: ignore[misc]
        ):
            return cast("list[ProperType]", typelist)
        return [get_proper_type(t) for t in typelist]
    else:
        return [get_proper_type(t) for t in types]


# We split off the type visitor base classes to another module
# to make it easier to gradually get modules working with mypyc.
# Import them here, after the types are defined.
# This is intended as a re-export also.
from mypy.type_visitor import (
    ALL_STRATEGY as ALL_STRATEGY,
    ANY_STRATEGY as ANY_STRATEGY,
    BoolTypeQuery as BoolTypeQuery,
    SyntheticTypeVisitor as SyntheticTypeVisitor,
    TypeQuery as TypeQuery,
    TypeTranslator as TypeTranslator,
    TypeVisitor as TypeVisitor,
)
from mypy.typetraverser import TypeTraverserVisitor


class TypeStrVisitor(SyntheticTypeVisitor[str]):
    """Visitor for pretty-printing types into strings.

    This is mostly for debugging/testing.

    Do not preserve original formatting.

    Notes:
     - Represent unbound types as Foo? or Foo?[...].
     - Represent the NoneType type as None.
    """

    def __init__(self, id_mapper: IdMapper | None = None, *, options: Options) -> None:
        self.id_mapper = id_mapper
        self.any_as_dots = False
        self.options = options

    def visit_unbound_type(self, t: UnboundType) -> str:
        s = t.name + "?"
        if t.args:
            s += f"[{self.list_str(t.args)}]"
        return s

    def visit_type_list(self, t: TypeList) -> str:
        return f"<TypeList {self.list_str(t.items)}>"

    def visit_callable_argument(self, t: CallableArgument) -> str:
        typ = t.typ.accept(self)
        if t.name is None:
            return f"{t.constructor}({typ})"
        else:
            return f"{t.constructor}({typ}, {t.name})"

    def visit_any(self, t: AnyType) -> str:
        if self.any_as_dots and t.type_of_any == TypeOfAny.special_form:
            return "..."
        return "Any"

    def visit_none_type(self, t: NoneType) -> str:
        return "None"

    def visit_uninhabited_type(self, t: UninhabitedType) -> str:
        return "Never"

    def visit_erased_type(self, t: ErasedType) -> str:
        return "<Erased>"

    def visit_deleted_type(self, t: DeletedType) -> str:
        if t.source is None:
            return "<Deleted>"
        else:
            return f"<Deleted '{t.source}'>"

    def visit_instance(self, t: Instance) -> str:
        if t.last_known_value and not t.args:
            # Instances with a literal fallback should never be generic. If they are,
            # something went wrong so we fall back to showing the full Instance repr.
            s = f"{t.last_known_value.accept(self)}?"
        else:
            s = t.type.fullname or t.type.name or "<???>"

        if t.args:
            if t.type.fullname == "builtins.tuple":
                assert len(t.args) == 1
                s += f"[{self.list_str(t.args)}, ...]"
            else:
                s += f"[{self.list_str(t.args)}]"
        elif t.type.has_type_var_tuple_type and len(t.type.type_vars) == 1:
            s += "[()]"
        if self.id_mapper:
            s += f"<{self.id_mapper.id(t.type)}>"
        return s

    def visit_type_var(self, t: TypeVarType) -> str:
        if t.name is None:
            # Anonymous type variable type (only numeric id).
            s = f"`{t.id}"
        else:
            # Named type variable type.
            s = f"{t.name}`{t.id}"
        if self.id_mapper and t.upper_bound:
            s += f"(upper_bound={t.upper_bound.accept(self)})"
        if t.has_default():
            s += f" = {t.default.accept(self)}"
        return s

    def visit_param_spec(self, t: ParamSpecType) -> str:
        # prefixes are displayed as Concatenate
        s = ""
        if t.prefix.arg_types:
            s += f"[{self.list_str(t.prefix.arg_types)}, **"
        if t.name is None:
            # Anonymous type variable type (only numeric id).
            s += f"`{t.id}"
        else:
            # Named type variable type.
            s += f"{t.name_with_suffix()}`{t.id}"
        if t.prefix.arg_types:
            s += "]"
        if t.has_default():
            s += f" = {t.default.accept(self)}"
        return s

    def visit_parameters(self, t: Parameters) -> str:
        # This is copied from visit_callable -- is there a way to decrease duplication?
        if t.is_ellipsis_args:
            return "..."

        s = ""
        bare_asterisk = False
        for i in range(len(t.arg_types)):
            if s != "":
                s += ", "
            if t.arg_kinds[i].is_named() and not bare_asterisk:
                s += "*, "
                bare_asterisk = True
            if t.arg_kinds[i] == ARG_STAR:
                s += "*"
            if t.arg_kinds[i] == ARG_STAR2:
                s += "**"
            name = t.arg_names[i]
            if name:
                s += f"{name}: "
            r = t.arg_types[i].accept(self)

            s += r

            if t.arg_kinds[i].is_optional():
                s += " ="

        return f"[{s}]"

    def visit_type_var_tuple(self, t: TypeVarTupleType) -> str:
        if t.name is None:
            # Anonymous type variable type (only numeric id).
            s = f"`{t.id}"
        else:
            # Named type variable type.
            s = f"{t.name}`{t.id}"
        if t.has_default():
            s += f" = {t.default.accept(self)}"
        return s

    def visit_callable_type(self, t: CallableType) -> str:
        param_spec = t.param_spec()
        if param_spec is not None:
            num_skip = 2
        else:
            num_skip = 0

        s = ""
        asterisk = False
        for i in range(len(t.arg_types) - num_skip):
            if s != "":
                s += ", "
            if t.arg_kinds[i].is_named() and not asterisk:
                s += "*, "
                asterisk = True
            if t.arg_kinds[i] == ARG_STAR:
                s += "*"
                asterisk = True
            if t.arg_kinds[i] == ARG_STAR2:
                s += "**"
            name = t.arg_names[i]
            if name:
                s += name + ": "
            type_str = t.arg_types[i].accept(self)
            if t.arg_kinds[i] == ARG_STAR2 and t.unpack_kwargs:
                type_str = f"Unpack[{type_str}]"
            s += type_str
            if t.arg_kinds[i].is_optional():
                s += " ="

        if param_spec is not None:
            n = param_spec.name
            if s:
                s += ", "
            s += f"*{n}.args, **{n}.kwargs"
            if param_spec.has_default():
                s += f" = {param_spec.default.accept(self)}"

        s = f"({s})"

        if not isinstance(get_proper_type(t.ret_type), NoneType):
            if t.type_guard is not None:
                s += f" -> TypeGuard[{t.type_guard.accept(self)}]"
            elif t.type_is is not None:
                s += f" -> TypeIs[{t.type_is.accept(self)}]"
            else:
                s += f" -> {t.ret_type.accept(self)}"

        if t.variables:
            vs = []
            for var in t.variables:
                if isinstance(var, TypeVarType):
                    # We reimplement TypeVarType.__repr__ here in order to support id_mapper.
                    if var.values:
                        vals = f"({', '.join(val.accept(self) for val in var.values)})"
                        vs.append(f"{var.name} in {vals}")
                    elif not is_named_instance(var.upper_bound, "builtins.object"):
                        vs.append(
                            f"{var.name} <: {var.upper_bound.accept(self)}{f' = {var.default.accept(self)}' if var.has_default() else ''}"
                        )
                    else:
                        vs.append(
                            f"{var.name}{f' = {var.default.accept(self)}' if var.has_default()  else ''}"
                        )
                else:
                    # For other TypeVarLikeTypes, use the name and default
                    vs.append(
                        f"{var.name}{f' = {var.default.accept(self)}' if var.has_default() else ''}"
                    )
            s = f"[{', '.join(vs)}] {s}"

        return f"def {s}"

    def visit_overloaded(self, t: Overloaded) -> str:
        a = []
        for i in t.items:
            a.append(i.accept(self))
        return f"Overload({', '.join(a)})"

    def visit_tuple_type(self, t: TupleType) -> str:
        s = self.list_str(t.items) or "()"
        tuple_name = "tuple" if self.options.use_lowercase_names() else "Tuple"
        if t.partial_fallback and t.partial_fallback.type:
            fallback_name = t.partial_fallback.type.fullname
            if fallback_name != "builtins.tuple":
                return f"{tuple_name}[{s}, fallback={t.partial_fallback.accept(self)}]"
        return f"{tuple_name}[{s}]"

    def visit_typeddict_type(self, t: TypedDictType) -> str:
        def item_str(name: str, typ: str) -> str:
            if name in t.required_keys:
                return f"{name!r}: {typ}"
            else:
                return f"{name!r}?: {typ}"

        s = (
            "{"
            + ", ".join(item_str(name, typ.accept(self)) for name, typ in t.items.items())
            + "}"
        )
        prefix = ""
        if t.fallback and t.fallback.type:
            if t.fallback.type.fullname not in TPDICT_FB_NAMES:
                prefix = repr(t.fallback.type.fullname) + ", "
        return f"TypedDict({prefix}{s})"

    def visit_raw_expression_type(self, t: RawExpressionType) -> str:
        if t.node is not None:
            return t.node.accept(self)
        return repr(t.literal_value)

    def visit_literal_type(self, t: LiteralType) -> str:
        return f"Literal[{t.value_repr()}]"

    def visit_union_type(self, t: UnionType) -> str:
        s = self.list_str(t.items)
        return f"Union[{s}]"

    def visit_partial_type(self, t: PartialType) -> str:
        if t.type is None:
            return "<partial None>"
        else:
            return "<partial {}[{}]>".format(t.type.name, ", ".join(["?"] * len(t.type.type_vars)))

    def visit_ellipsis_type(self, t: EllipsisType) -> str:
        return "..."

    def visit_type_type(self, t: TypeType) -> str:
        if self.options.use_lowercase_names():
            type_name = "type"
        else:
            type_name = "Type"
        return f"{type_name}[{t.item.accept(self)}]"

    def visit_placeholder_type(self, t: PlaceholderType) -> str:
        return f"<placeholder {t.fullname}>"

    def visit_type_alias_type(self, t: TypeAliasType) -> str:
        if t.alias is not None:
            unrolled, recursed = t._partial_expansion()
            self.any_as_dots = recursed
            type_str = unrolled.accept(self)
            self.any_as_dots = False
            return type_str
        return "<alias (unfixed)>"

    def visit_unpack_type(self, t: UnpackType) -> str:
        return f"Unpack[{t.type.accept(self)}]"

    def list_str(self, a: Iterable[Type]) -> str:
        """Convert items of an array to strings (pretty-print types)
        and join the results with commas.
        """
        res = []
        for t in a:
            res.append(t.accept(self))
        return ", ".join(res)


class TrivialSyntheticTypeTranslator(TypeTranslator, SyntheticTypeVisitor[Type]):
    """A base class for type translators that need to be run during semantic analysis."""

    def visit_placeholder_type(self, t: PlaceholderType) -> Type:
        return t

    def visit_callable_argument(self, t: CallableArgument) -> Type:
        return t

    def visit_ellipsis_type(self, t: EllipsisType) -> Type:
        return t

    def visit_raw_expression_type(self, t: RawExpressionType) -> Type:
        if t.node is not None:
            node = t.node.accept(self)
            return t.copy_modified(node=node)
        return t

    def visit_type_list(self, t: TypeList) -> Type:
        return t


class UnrollAliasVisitor(TrivialSyntheticTypeTranslator):
    def __init__(self, initial_aliases: set[TypeAliasType]) -> None:
        self.recursed = False
        self.initial_aliases = initial_aliases

    def visit_type_alias_type(self, t: TypeAliasType) -> Type:
        if t in self.initial_aliases:
            self.recursed = True
            return AnyType(TypeOfAny.special_form)
        # Create a new visitor on encountering a new type alias, so that an alias like
        #     A = Tuple[B, B]
        #     B = int
        # will not be detected as recursive on the second encounter of B.
        subvisitor = UnrollAliasVisitor(self.initial_aliases | {t})
        result = get_proper_type(t).accept(subvisitor)
        if subvisitor.recursed:
            self.recursed = True
        return result


def is_named_instance(t: Type, fullnames: str | tuple[str, ...]) -> TypeGuard[Instance]:
    if not isinstance(fullnames, tuple):
        fullnames = (fullnames,)

    t = get_proper_type(t)
    return isinstance(t, Instance) and t.type.fullname in fullnames


class LocationSetter(TypeTraverserVisitor):
    # TODO: Should we update locations of other Type subclasses?
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def visit_instance(self, typ: Instance) -> None:
        typ.line = self.line
        typ.column = self.column
        super().visit_instance(typ)


class HasTypeVars(BoolTypeQuery):
    def __init__(self) -> None:
        super().__init__(ANY_STRATEGY)
        self.skip_alias_target = True

    def visit_type_var(self, t: TypeVarType) -> bool:
        return True

    def visit_type_var_tuple(self, t: TypeVarTupleType) -> bool:
        return True

    def visit_param_spec(self, t: ParamSpecType) -> bool:
        return True


def has_type_vars(typ: Type) -> bool:
    """Check if a type contains any type variables (recursively)."""
    return typ.accept(HasTypeVars())


class HasRecursiveType(BoolTypeQuery):
    def __init__(self) -> None:
        super().__init__(ANY_STRATEGY)

    def visit_type_alias_type(self, t: TypeAliasType) -> bool:
        return t.is_recursive or self.query_types(t.args)


# Use singleton since this is hot (note: call reset() before using)
_has_recursive_type: Final = HasRecursiveType()


def has_recursive_types(typ: Type) -> bool:
    """Check if a type contains any recursive aliases (recursively)."""
    _has_recursive_type.reset()
    return typ.accept(_has_recursive_type)


def split_with_prefix_and_suffix(
    types: tuple[Type, ...], prefix: int, suffix: int
) -> tuple[tuple[Type, ...], tuple[Type, ...], tuple[Type, ...]]:
    if len(types) <= prefix + suffix:
        types = extend_args_for_prefix_and_suffix(types, prefix, suffix)
    if suffix:
        return types[:prefix], types[prefix:-suffix], types[-suffix:]
    else:
        return types[:prefix], types[prefix:], ()


def extend_args_for_prefix_and_suffix(
    types: tuple[Type, ...], prefix: int, suffix: int
) -> tuple[Type, ...]:
    """Extend list of types by eating out from variadic tuple to satisfy prefix and suffix."""
    idx = None
    item = None
    for i, t in enumerate(types):
        if isinstance(t, UnpackType):
            p_type = get_proper_type(t.type)
            if isinstance(p_type, Instance) and p_type.type.fullname == "builtins.tuple":
                item = p_type.args[0]
                idx = i
                break

    if idx is None:
        return types
    assert item is not None
    if idx < prefix:
        start = (item,) * (prefix - idx)
    else:
        start = ()
    if len(types) - idx - 1 < suffix:
        end = (item,) * (suffix - len(types) + idx + 1)
    else:
        end = ()
    return types[:idx] + start + (types[idx],) + end + types[idx + 1 :]


def flatten_nested_unions(
    types: Sequence[Type], handle_type_alias_type: bool = True
) -> list[Type]:
    """Flatten nested unions in a type list."""
    if not isinstance(types, list):
        typelist = list(types)
    else:
        typelist = cast("list[Type]", types)

    # Fast path: most of the time there is nothing to flatten
    if not any(isinstance(t, (TypeAliasType, UnionType)) for t in typelist):  # type: ignore[misc]
        return typelist

    flat_items: list[Type] = []
    for t in typelist:
        tp = get_proper_type(t) if handle_type_alias_type else t
        if isinstance(tp, ProperType) and isinstance(tp, UnionType):
            flat_items.extend(
                flatten_nested_unions(tp.items, handle_type_alias_type=handle_type_alias_type)
            )
        else:
            # Must preserve original aliases when possible.
            flat_items.append(t)
    return flat_items


def find_unpack_in_list(items: Sequence[Type]) -> int | None:
    unpack_index: int | None = None
    for i, item in enumerate(items):
        if isinstance(item, UnpackType):
            # We cannot fail here, so we must check this in an earlier
            # semanal phase.
            # Funky code here avoids mypyc narrowing the type of unpack_index.
            old_index = unpack_index
            assert old_index is None
            # Don't return so that we can also sanity check there is only one.
            unpack_index = i
    return unpack_index


def flatten_nested_tuples(types: Sequence[Type]) -> list[Type]:
    """Recursively flatten TupleTypes nested with Unpack.

    For example this will transform
        Tuple[A, Unpack[Tuple[B, Unpack[Tuple[C, D]]]]]
    into
        Tuple[A, B, C, D]
    """
    res = []
    for typ in types:
        if not isinstance(typ, UnpackType):
            res.append(typ)
            continue
        p_type = get_proper_type(typ.type)
        if not isinstance(p_type, TupleType):
            res.append(typ)
            continue
        res.extend(flatten_nested_tuples(p_type.items))
    return res


def is_literal_type(typ: ProperType, fallback_fullname: str, value: LiteralValue) -> bool:
    """Check if this type is a LiteralType with the given fallback type and value."""
    if isinstance(typ, Instance) and typ.last_known_value:
        typ = typ.last_known_value
    return (
        isinstance(typ, LiteralType)
        and typ.fallback.type.fullname == fallback_fullname
        and typ.value == value
    )


names: Final = globals().copy()
names.pop("NOT_READY", None)
deserialize_map: Final = {
    key: obj.deserialize
    for key, obj in names.items()
    if isinstance(obj, type) and issubclass(obj, Type) and obj is not Type
}


def callable_with_ellipsis(any_type: AnyType, ret_type: Type, fallback: Instance) -> CallableType:
    """Construct type Callable[..., ret_type]."""
    return CallableType(
        [any_type, any_type],
        [ARG_STAR, ARG_STAR2],
        [None, None],
        ret_type=ret_type,
        fallback=fallback,
        is_ellipsis_args=True,
    )


def remove_dups(types: list[T]) -> list[T]:
    if len(types) <= 1:
        return types
    # Get unique elements in order of appearance
    all_types: set[T] = set()
    new_types: list[T] = []
    for t in types:
        if t not in all_types:
            new_types.append(t)
            all_types.add(t)
    return new_types


def type_vars_as_args(type_vars: Sequence[TypeVarLikeType]) -> tuple[Type, ...]:
    """Represent type variables as they would appear in a type argument list."""
    args: list[Type] = []
    for tv in type_vars:
        if isinstance(tv, TypeVarTupleType):
            args.append(UnpackType(tv))
        else:
            args.append(tv)
    return tuple(args)


# This cyclic import is unfortunate, but to avoid it we would need to move away all uses
# of get_proper_type() from types.py. Majority of them have been removed, but few remaining
# are quite tricky to get rid of, but ultimately we want to do it at some point.
from mypy.expandtype import ExpandTypeVisitor


class InstantiateAliasVisitor(ExpandTypeVisitor):
    def visit_union_type(self, t: UnionType) -> Type:
        # Unlike regular expand_type(), we don't do any simplification for unions,
        # not even removing strict duplicates. There are three reasons for this:
        #   * get_proper_type() is a very hot function, even slightest slow down will
        #     cause a perf regression
        #   * We want to preserve this historical behaviour, to avoid possible
        #     regressions
        #   * Simplifying unions may (indirectly) call get_proper_type(), causing
        #     infinite recursion.
        return TypeTranslator.visit_union_type(self, t)
