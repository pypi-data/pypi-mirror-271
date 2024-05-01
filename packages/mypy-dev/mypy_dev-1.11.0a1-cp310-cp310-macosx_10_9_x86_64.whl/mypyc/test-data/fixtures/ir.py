# These builtins stubs are used implicitly in AST to IR generation
# test cases.

import _typeshed
from typing import (
    TypeVar, Generic, List, Iterator, Iterable, Dict, Optional, Tuple, Any, Set,
    overload, Mapping, Union, Callable, Sequence, FrozenSet, Protocol
)

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)
S = TypeVar('S')
K = TypeVar('K') # for keys in mapping
V = TypeVar('V') # for values in mapping

class __SupportsAbs(Protocol[T_co]):
    def __abs__(self) -> T_co: pass

class __SupportsDivMod(Protocol[T_contra, T_co]):
    def __divmod__(self, other: T_contra) -> T_co: ...

class __SupportsRDivMod(Protocol[T_contra, T_co]):
    def __rdivmod__(self, other: T_contra) -> T_co: ...

_M = TypeVar("_M", contravariant=True)

class __SupportsPow2(Protocol[T_contra, T_co]):
    def __pow__(self, other: T_contra) -> T_co: ...

class __SupportsPow3NoneOnly(Protocol[T_contra, T_co]):
    def __pow__(self, other: T_contra, modulo: None = ...) -> T_co: ...

class __SupportsPow3(Protocol[T_contra, _M, T_co]):
    def __pow__(self, other: T_contra, modulo: _M) -> T_co: ...

__SupportsSomeKindOfPow = Union[
    __SupportsPow2[Any, Any], __SupportsPow3NoneOnly[Any, Any] | __SupportsPow3[Any, Any, Any]
]

class object:
    def __init__(self) -> None: pass
    def __eq__(self, x: object) -> bool: pass
    def __ne__(self, x: object) -> bool: pass

class type:
    def __init__(self, o: object) -> None: ...
    __name__ : str
    __annotations__: Dict[str, Any]

class ellipsis: pass

# Primitive types are special in generated code.

class int:
    @overload
    def __init__(self) -> None: pass
    @overload
    def __init__(self, x: object, base: int = 10) -> None: pass
    def __add__(self, n: int) -> int: pass
    def __sub__(self, n: int) -> int: pass
    def __mul__(self, n: int) -> int: pass
    def __pow__(self, n: int, modulo: Optional[int] = None) -> int: pass
    def __floordiv__(self, x: int) -> int: pass
    def __truediv__(self, x: float) -> float: pass
    def __mod__(self, x: int) -> int: pass
    def __divmod__(self, x: float) -> Tuple[float, float]: pass
    def __neg__(self) -> int: pass
    def __pos__(self) -> int: pass
    def __abs__(self) -> int: pass
    def __invert__(self) -> int: pass
    def __and__(self, n: int) -> int: pass
    def __or__(self, n: int) -> int: pass
    def __xor__(self, n: int) -> int: pass
    def __lshift__(self, x: int) -> int: pass
    def __rshift__(self, x: int) -> int: pass
    def __eq__(self, n: object) -> bool: pass
    def __ne__(self, n: object) -> bool: pass
    def __lt__(self, n: int) -> bool: pass
    def __gt__(self, n: int) -> bool: pass
    def __le__(self, n: int) -> bool: pass
    def __ge__(self, n: int) -> bool: pass

class str:
    @overload
    def __init__(self) -> None: pass
    @overload
    def __init__(self, x: object) -> None: pass
    def __add__(self, x: str) -> str: pass
    def __mul__(self, x: int) -> str: pass
    def __rmul__(self, x: int) -> str: pass
    def __eq__(self, x: object) -> bool: pass
    def __ne__(self, x: object) -> bool: pass
    def __lt__(self, x: str) -> bool: ...
    def __le__(self, x: str) -> bool: ...
    def __gt__(self, x: str) -> bool: ...
    def __ge__(self, x: str) -> bool: ...
    @overload
    def __getitem__(self, i: int) -> str: pass
    @overload
    def __getitem__(self, i: slice) -> str: pass
    def __contains__(self, item: str) -> bool: pass
    def __iter__(self) -> Iterator[str]: ...
    def split(self, sep: Optional[str] = None, max: Optional[int] = None) -> List[str]: pass
    def strip (self, item: str) -> str: pass
    def join(self, x: Iterable[str]) -> str: pass
    def format(self, *args: Any, **kwargs: Any) -> str: ...
    def upper(self) -> str: ...
    def startswith(self, x: str, start: int=..., end: int=...) -> bool: ...
    def endswith(self, x: str, start: int=..., end: int=...) -> bool: ...
    def replace(self, old: str, new: str, maxcount: int=...) -> str: ...
    def encode(self, x: str=..., y: str=...) -> bytes: ...

class float:
    def __init__(self, x: object) -> None: pass
    def __add__(self, n: float) -> float: pass
    def __radd__(self, n: float) -> float: pass
    def __sub__(self, n: float) -> float: pass
    def __rsub__(self, n: float) -> float: pass
    def __mul__(self, n: float) -> float: pass
    def __truediv__(self, n: float) -> float: pass
    def __floordiv__(self, n: float) -> float: pass
    def __mod__(self, n: float) -> float: pass
    def __pow__(self, n: float) -> float: pass
    def __neg__(self) -> float: pass
    def __pos__(self) -> float: pass
    def __abs__(self) -> float: pass
    def __invert__(self) -> float: pass
    def __eq__(self, x: object) -> bool: pass
    def __ne__(self, x: object) -> bool: pass
    def __lt__(self, x: float) -> bool: ...
    def __le__(self, x: float) -> bool: ...
    def __gt__(self, x: float) -> bool: ...
    def __ge__(self, x: float) -> bool: ...

class complex:
    def __init__(self, x: object, y: object = None) -> None: pass
    def __add__(self, n: complex) -> complex: pass
    def __radd__(self, n: float) -> complex: pass
    def __sub__(self, n: complex) -> complex: pass
    def __rsub__(self, n: float) -> complex: pass
    def __mul__(self, n: complex) -> complex: pass
    def __truediv__(self, n: complex) -> complex: pass
    def __neg__(self) -> complex: pass

class bytes:
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self, x: object) -> None: ...
    def __add__(self, x: bytes) -> bytes: ...
    def __mul__(self, x: int) -> bytes: ...
    def __rmul__(self, x: int) -> bytes: ...
    def __eq__(self, x: object) -> bool: ...
    def __ne__(self, x: object) -> bool: ...
    @overload
    def __getitem__(self, i: int) -> int: ...
    @overload
    def __getitem__(self, i: slice) -> bytes: ...
    def join(self, x: Iterable[object]) -> bytes: ...
    def decode(self, x: str=..., y: str=...) -> str: ...

class bytearray:
    @overload
    def __init__(self) -> None: pass
    @overload
    def __init__(self, x: object) -> None: pass
    @overload
    def __init__(self, string: str, encoding: str, err: str = ...) -> None: pass
    def __add__(self, s: bytes) -> bytearray: ...
    def __setitem__(self, i: int, o: int) -> None: ...
    def __getitem__(self, i: int) -> int: ...
    def decode(self, x: str = ..., y: str = ...) -> str: ...

class bool(int):
    def __init__(self, o: object = ...) -> None: ...
    @overload
    def __and__(self, n: bool) -> bool: ...
    @overload
    def __and__(self, n: int) -> int: ...
    @overload
    def __or__(self, n: bool) -> bool: ...
    @overload
    def __or__(self, n: int) -> int: ...
    @overload
    def __xor__(self, n: bool) -> bool: ...
    @overload
    def __xor__(self, n: int) -> int: ...

class tuple(Generic[T_co], Sequence[T_co], Iterable[T_co]):
    def __init__(self, i: Iterable[T_co]) -> None: pass
    @overload
    def __getitem__(self, i: int) -> T_co: pass
    @overload
    def __getitem__(self, i: slice) -> Tuple[T_co, ...]: pass
    def __len__(self) -> int: pass
    def __iter__(self) -> Iterator[T_co]: ...
    def __contains__(self, item: object) -> int: ...

class function: pass

class list(Generic[T], Sequence[T], Iterable[T]):
    def __init__(self, i: Optional[Iterable[T]] = None) -> None: pass
    @overload
    def __getitem__(self, i: int) -> T: ...
    @overload
    def __getitem__(self, s: slice) -> List[T]: ...
    def __setitem__(self, i: int, o: T) -> None: pass
    def __delitem__(self, i: int) -> None: pass
    def __mul__(self, i: int) -> List[T]: pass
    def __rmul__(self, i: int) -> List[T]: pass
    def __iter__(self) -> Iterator[T]: pass
    def __len__(self) -> int: pass
    def __contains__(self, item: object) -> int: ...
    def __add__(self, x: List[T]) -> List[T]: ...
    def append(self, x: T) -> None: pass
    def pop(self, i: int = -1) -> T: pass
    def count(self, T) -> int: pass
    def extend(self, l: Iterable[T]) -> None: pass
    def insert(self, i: int, x: T) -> None: pass
    def sort(self) -> None: pass
    def reverse(self) -> None: pass
    def remove(self, o: T) -> None: pass
    def index(self, o: T) -> int: pass

class dict(Mapping[K, V]):
    @overload
    def __init__(self, **kwargs: K) -> None: ...
    @overload
    def __init__(self, map: Mapping[K, V], **kwargs: V) -> None: ...
    @overload
    def __init__(self, iterable: Iterable[Tuple[K, V]], **kwargs: V) -> None: ...
    def __getitem__(self, key: K) -> V: pass
    def __setitem__(self, k: K, v: V) -> None: pass
    def __delitem__(self, k: K) -> None: pass
    def __contains__(self, item: object) -> int: pass
    def __iter__(self) -> Iterator[K]: pass
    def __len__(self) -> int: pass
    @overload
    def update(self, __m: Mapping[K, V], **kwargs: V) -> None: pass
    @overload
    def update(self, __m: Iterable[Tuple[K, V]], **kwargs: V) -> None: ...
    @overload
    def update(self, **kwargs: V) -> None: ...
    def pop(self, x: int) -> K: pass
    def keys(self) -> Iterable[K]: pass
    def values(self) -> Iterable[V]: pass
    def items(self) -> Iterable[Tuple[K, V]]: pass
    def clear(self) -> None: pass
    def copy(self) -> Dict[K, V]: pass
    def setdefault(self, key: K, val: V = ...) -> V: pass

class set(Generic[T]):
    def __init__(self, i: Optional[Iterable[T]] = None) -> None: pass
    def __iter__(self) -> Iterator[T]: pass
    def __len__(self) -> int: pass
    def add(self, x: T) -> None: pass
    def remove(self, x: T) -> None: pass
    def discard(self, x: T) -> None: pass
    def clear(self) -> None: pass
    def pop(self) -> T: pass
    def update(self, x: Iterable[S]) -> None: pass
    def __or__(self, s: Union[Set[S], FrozenSet[S]]) -> Set[Union[T, S]]: ...
    def __xor__(self, s: Union[Set[S], FrozenSet[S]]) -> Set[Union[T, S]]: ...

class frozenset(Generic[T]):
    def __init__(self, i: Optional[Iterable[T]] = None) -> None: pass
    def __iter__(self) -> Iterator[T]: pass
    def __len__(self) -> int: pass
    def __or__(self, s: Union[Set[S], FrozenSet[S]]) -> FrozenSet[Union[T, S]]: ...
    def __xor__(self, s: Union[Set[S], FrozenSet[S]]) -> FrozenSet[Union[T, S]]: ...

class slice: pass

class range(Iterable[int]):
    def __init__(self, x: int, y: int = ..., z: int = ...) -> None: pass
    def __iter__(self) -> Iterator[int]: pass
    def __len__(self) -> int: pass
    def __next__(self) -> int: pass

class property:
    def __init__(self, fget: Optional[Callable[[Any], Any]] = ...,
                 fset: Optional[Callable[[Any, Any], None]] = ...,
                 fdel: Optional[Callable[[Any], None]] = ...,
                 doc: Optional[str] = ...) -> None: ...
    def getter(self, fget: Callable[[Any], Any]) -> property: ...
    def setter(self, fset: Callable[[Any, Any], None]) -> property: ...
    def deleter(self, fdel: Callable[[Any], None]) -> property: ...
    def __get__(self, obj: Any, type: Optional[type] = ...) -> Any: ...
    def __set__(self, obj: Any, value: Any) -> None: ...
    def __delete__(self, obj: Any) -> None: ...
    def fget(self) -> Any: ...
    def fset(self, value: Any) -> None: ...
    def fdel(self) -> None: ...

class BaseException: pass

class Exception(BaseException):
    def __init__(self, message: Optional[str] = None) -> None: pass

class Warning(Exception): pass
class UserWarning(Warning): pass
class TypeError(Exception): pass
class ValueError(Exception): pass
class AttributeError(Exception): pass
class ImportError(Exception): pass
class NameError(Exception): pass
class UnboundLocalError(NameError): pass
class LookupError(Exception): pass
class KeyError(LookupError): pass
class IndexError(LookupError): pass
class RuntimeError(Exception): pass
class UnicodeEncodeError(RuntimeError): pass
class UnicodeDecodeError(RuntimeError): pass
class NotImplementedError(RuntimeError): pass

class StopIteration(Exception):
    value: Any

class ArithmeticError(Exception): pass
class ZeroDivisionError(ArithmeticError): pass
class OverflowError(ArithmeticError): pass

class GeneratorExit(BaseException): pass

def any(i: Iterable[T]) -> bool: pass
def all(i: Iterable[T]) -> bool: pass
def sum(i: Iterable[T]) -> int: pass
def reversed(object: Sequence[T]) -> Iterator[T]: ...
def id(o: object) -> int: pass
# This type is obviously wrong but the test stubs don't have Sized anymore
def len(o: object) -> int: pass
def print(*object) -> None: pass
def isinstance(x: object, t: object) -> bool: pass
def iter(i: Iterable[T]) -> Iterator[T]: pass
@overload
def next(i: Iterator[T]) -> T: pass
@overload
def next(i: Iterator[T], default: T) -> T: pass
def hash(o: object) -> int: ...
def globals() -> Dict[str, Any]: ...
def getattr(obj: object, name: str, default: Any = None) -> Any: ...
def setattr(obj: object, name: str, value: Any) -> None: ...
def enumerate(x: Iterable[T]) -> Iterator[Tuple[int, T]]: ...
@overload
def zip(x: Iterable[T], y: Iterable[S]) -> Iterator[Tuple[T, S]]: ...
@overload
def zip(x: Iterable[T], y: Iterable[S], z: Iterable[V]) -> Iterator[Tuple[T, S, V]]: ...
def eval(e: str) -> Any: ...
def abs(x: __SupportsAbs[T]) -> T: ...
@overload
def divmod(x: __SupportsDivMod[T_contra, T_co], y: T_contra) -> T_co: ...
@overload
def divmod(x: T_contra, y: __SupportsRDivMod[T_contra, T_co]) -> T_co: ...
@overload
def pow(base: __SupportsPow2[T_contra, T_co], exp: T_contra, mod: None = None) -> T_co: ...
@overload
def pow(base: __SupportsPow3NoneOnly[T_contra, T_co], exp: T_contra, mod: None = None) -> T_co: ...
@overload
def pow(base: __SupportsPow3[T_contra, _M, T_co], exp: T_contra, mod: _M) -> T_co: ...
def exit() -> None: ...
def min(x: T, y: T) -> T: ...
def max(x: T, y: T) -> T: ...
def repr(o: object) -> str: ...
def ascii(o: object) -> str: ...
def ord(o: object) -> int: ...
def chr(i: int) -> str: ...

# Dummy definitions.
class classmethod: pass
class staticmethod: pass

NotImplemented: Any = ...
