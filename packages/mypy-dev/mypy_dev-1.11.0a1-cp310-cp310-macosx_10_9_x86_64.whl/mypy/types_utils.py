"""
This module is for (more basic) type operations that should not depend on is_subtype(),
meet_types(), join_types() etc. We don't want to keep them in mypy/types.py for two reasons:
* Reduce the size of that module.
* Reduce use of get_proper_type() in types.py to avoid cyclic imports
  expand_type <-> types, if we move get_proper_type() to the former.
"""

from __future__ import annotations

from typing import Callable, Iterable, cast

from mypy.nodes import ARG_STAR, ARG_STAR2, FuncItem, TypeAlias
from mypy.types import (
    AnyType,
    CallableType,
    Instance,
    NoneType,
    Overloaded,
    ParamSpecType,
    ProperType,
    TupleType,
    Type,
    TypeAliasType,
    TypeType,
    TypeVarType,
    UnionType,
    UnpackType,
    flatten_nested_unions,
    get_proper_type,
    get_proper_types,
)


def flatten_types(types: Iterable[Type]) -> Iterable[Type]:
    for t in types:
        tp = get_proper_type(t)
        if isinstance(tp, UnionType):
            yield from flatten_types(tp.items)
        else:
            yield t


def strip_type(typ: Type) -> Type:
    """Make a copy of type without 'debugging info' (function name)."""
    orig_typ = typ
    typ = get_proper_type(typ)
    if isinstance(typ, CallableType):
        return typ.copy_modified(name=None)
    elif isinstance(typ, Overloaded):
        return Overloaded([cast(CallableType, strip_type(item)) for item in typ.items])
    else:
        return orig_typ


def is_invalid_recursive_alias(seen_nodes: set[TypeAlias], target: Type) -> bool:
    """Flag aliases like A = Union[int, A], T = tuple[int, *T] (and similar mutual aliases).

    Such aliases don't make much sense, and cause problems in later phases.
    """
    if isinstance(target, TypeAliasType):
        if target.alias in seen_nodes:
            return True
        assert target.alias, f"Unfixed type alias {target.type_ref}"
        return is_invalid_recursive_alias(seen_nodes | {target.alias}, get_proper_type(target))
    assert isinstance(target, ProperType)
    if not isinstance(target, (UnionType, TupleType)):
        return False
    if isinstance(target, UnionType):
        return any(is_invalid_recursive_alias(seen_nodes, item) for item in target.items)
    for item in target.items:
        if isinstance(item, UnpackType):
            if is_invalid_recursive_alias(seen_nodes, item.type):
                return True
    return False


def is_bad_type_type_item(item: Type) -> bool:
    """Prohibit types like Type[Type[...]].

    Such types are explicitly prohibited by PEP 484. Also, they cause problems
    with recursive types like T = Type[T], because internal representation of
    TypeType item is normalized (i.e. always a proper type).
    """
    item = get_proper_type(item)
    if isinstance(item, TypeType):
        return True
    if isinstance(item, UnionType):
        return any(
            isinstance(get_proper_type(i), TypeType) for i in flatten_nested_unions(item.items)
        )
    return False


def is_union_with_any(tp: Type) -> bool:
    """Is this a union with Any or a plain Any type?"""
    tp = get_proper_type(tp)
    if isinstance(tp, AnyType):
        return True
    if not isinstance(tp, UnionType):
        return False
    return any(is_union_with_any(t) for t in get_proper_types(tp.items))


def is_generic_instance(tp: Type) -> bool:
    tp = get_proper_type(tp)
    return isinstance(tp, Instance) and bool(tp.args)


def is_overlapping_none(t: Type) -> bool:
    t = get_proper_type(t)
    return isinstance(t, NoneType) or (
        isinstance(t, UnionType) and any(isinstance(get_proper_type(e), NoneType) for e in t.items)
    )


def remove_optional(typ: Type) -> Type:
    typ = get_proper_type(typ)
    if isinstance(typ, UnionType):
        return UnionType.make_union(
            [t for t in typ.items if not isinstance(get_proper_type(t), NoneType)]
        )
    else:
        return typ


def is_self_type_like(typ: Type, *, is_classmethod: bool) -> bool:
    """Does this look like a self-type annotation?"""
    typ = get_proper_type(typ)
    if not is_classmethod:
        return isinstance(typ, TypeVarType)
    if not isinstance(typ, TypeType):
        return False
    return isinstance(typ.item, TypeVarType)


def store_argument_type(
    defn: FuncItem, i: int, typ: CallableType, named_type: Callable[[str, list[Type]], Instance]
) -> None:
    arg_type = typ.arg_types[i]
    if typ.arg_kinds[i] == ARG_STAR:
        if isinstance(arg_type, ParamSpecType):
            pass
        elif isinstance(arg_type, UnpackType):
            unpacked_type = get_proper_type(arg_type.type)
            if isinstance(unpacked_type, TupleType):
                # Instead of using Tuple[Unpack[Tuple[...]]], just use Tuple[...]
                arg_type = unpacked_type
            elif (
                isinstance(unpacked_type, Instance)
                and unpacked_type.type.fullname == "builtins.tuple"
            ):
                arg_type = unpacked_type
            else:
                # TODO: verify that we can only have a TypeVarTuple here.
                arg_type = TupleType(
                    [arg_type],
                    fallback=named_type("builtins.tuple", [named_type("builtins.object", [])]),
                )
        else:
            # builtins.tuple[T] is typing.Tuple[T, ...]
            arg_type = named_type("builtins.tuple", [arg_type])
    elif typ.arg_kinds[i] == ARG_STAR2:
        if not isinstance(arg_type, ParamSpecType) and not typ.unpack_kwargs:
            arg_type = named_type("builtins.dict", [named_type("builtins.str", []), arg_type])
    defn.arguments[i].variable.type = arg_type
