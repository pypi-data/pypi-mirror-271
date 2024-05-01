from __future__ import annotations

import sys
import sysconfig
from typing import Any, Dict, Final

from mypy.util import unnamed_function

PREFIX: Final = "CPyPy_"  # Python wrappers
NATIVE_PREFIX: Final = "CPyDef_"  # Native functions etc.
DUNDER_PREFIX: Final = "CPyDunder_"  # Wrappers for exposing dunder methods to the API
REG_PREFIX: Final = "cpy_r_"  # Registers
STATIC_PREFIX: Final = "CPyStatic_"  # Static variables (for literals etc.)
TYPE_PREFIX: Final = "CPyType_"  # Type object struct
MODULE_PREFIX: Final = "CPyModule_"  # Cached modules
ATTR_PREFIX: Final = "_"  # Attributes

ENV_ATTR_NAME: Final = "__mypyc_env__"
NEXT_LABEL_ATTR_NAME: Final = "__mypyc_next_label__"
TEMP_ATTR_NAME: Final = "__mypyc_temp__"
LAMBDA_NAME: Final = "__mypyc_lambda__"
PROPSET_PREFIX: Final = "__mypyc_setter__"
SELF_NAME: Final = "__mypyc_self__"

# Max short int we accept as a literal is based on 32-bit platforms,
# so that we can just always emit the same code.

TOP_LEVEL_NAME: Final = "__top_level__"  # Special function representing module top level

# Maximal number of subclasses for a class to trigger fast path in isinstance() checks.
FAST_ISINSTANCE_MAX_SUBCLASSES: Final = 2

# Size of size_t, if configured.
SIZEOF_SIZE_T_SYSCONFIG: Final = sysconfig.get_config_var("SIZEOF_SIZE_T")

SIZEOF_SIZE_T: Final = (
    int(SIZEOF_SIZE_T_SYSCONFIG)
    if SIZEOF_SIZE_T_SYSCONFIG is not None
    else (sys.maxsize + 1).bit_length() // 8
)

IS_32_BIT_PLATFORM: Final = int(SIZEOF_SIZE_T) == 4

PLATFORM_SIZE = 4 if IS_32_BIT_PLATFORM else 8

# Maximum value for a short tagged integer.
MAX_SHORT_INT: Final = 2 ** (8 * int(SIZEOF_SIZE_T) - 2) - 1

# Minimum value for a short tagged integer.
MIN_SHORT_INT: Final = -(MAX_SHORT_INT) - 1

# Maximum value for a short tagged integer represented as a C integer literal.
#
# Note: Assume that the compiled code uses the same bit width as mypyc
MAX_LITERAL_SHORT_INT: Final = MAX_SHORT_INT
MIN_LITERAL_SHORT_INT: Final = -MAX_LITERAL_SHORT_INT - 1

# Description of the C type used to track the definedness of attributes and
# the presence of argument default values that have types with overlapping
# error values. Each tracked attribute/argument has a dedicated bit in the
# relevant bitmap.
BITMAP_TYPE: Final = "uint32_t"
BITMAP_BITS: Final = 32

# Runtime C library files
RUNTIME_C_FILES: Final = [
    "init.c",
    "getargs.c",
    "getargsfast.c",
    "int_ops.c",
    "float_ops.c",
    "str_ops.c",
    "bytes_ops.c",
    "list_ops.c",
    "dict_ops.c",
    "set_ops.c",
    "tuple_ops.c",
    "exc_ops.c",
    "misc_ops.c",
    "generic_ops.c",
]


JsonDict = Dict[str, Any]


def shared_lib_name(group_name: str) -> str:
    """Given a group name, return the actual name of its extension module.

    (This just adds a suffix to the final component.)
    """
    return f"{group_name}__mypyc"


def short_name(name: str) -> str:
    if name.startswith("builtins."):
        return name[9:]
    return name


def use_vectorcall(capi_version: tuple[int, int]) -> bool:
    # We can use vectorcalls to make calls on Python 3.8+ (PEP 590).
    return capi_version >= (3, 8)


def use_method_vectorcall(capi_version: tuple[int, int]) -> bool:
    # We can use a dedicated vectorcall API to call methods on Python 3.9+.
    return capi_version >= (3, 9)


def get_id_from_name(name: str, fullname: str, line: int) -> str:
    """Create a unique id for a function.

    This creates an id that is unique for any given function definition, so that it can be used as
    a dictionary key. This is usually the fullname of the function, but this is different in that
    it handles the case where the function is named '_', in which case multiple different functions
    could have the same name."""
    if unnamed_function(name):
        return f"{fullname}.{line}"
    else:
        return fullname


def short_id_from_name(func_name: str, shortname: str, line: int | None) -> str:
    if unnamed_function(func_name):
        assert line is not None
        partial_name = f"{shortname}.{line}"
    else:
        partial_name = shortname
    return partial_name


def bitmap_name(index: int) -> str:
    if index == 0:
        return "__bitmap"
    return f"__bitmap{index + 1}"
