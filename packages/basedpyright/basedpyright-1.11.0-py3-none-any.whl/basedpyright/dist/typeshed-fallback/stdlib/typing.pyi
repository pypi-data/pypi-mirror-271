# Since this module defines "overload" it is not recognized by Ruff as typing.overload
# ruff: noqa: F811
# TODO: The collections import is required, otherwise mypy crashes.
# https://github.com/python/mypy/issues/16744
import collections  # noqa: F401  # pyright: ignore
import sys
import typing_extensions
from _collections_abc import dict_items, dict_keys, dict_values
from _typeshed import IdentityFunction, ReadableBuffer, SupportsKeysAndGetItem
from abc import ABCMeta, abstractmethod
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from re import Match as Match, Pattern as Pattern
from types import (
    BuiltinFunctionType,
    CodeType,
    FrameType,
    FunctionType,
    MethodDescriptorType,
    MethodType,
    MethodWrapperType,
    ModuleType,
    TracebackType,
    WrapperDescriptorType,
)
from typing_extensions import Never as _Never, ParamSpec as _ParamSpec

if sys.version_info >= (3, 10):
    from types import UnionType
if sys.version_info >= (3, 9):
    from types import GenericAlias

__all__ = [
    "AbstractSet",
    "Any",
    "AnyStr",
    "AsyncContextManager",
    "AsyncGenerator",
    "AsyncIterable",
    "AsyncIterator",
    "Awaitable",
    "ByteString",
    "Callable",
    "ChainMap",
    "ClassVar",
    "Collection",
    "Container",
    "ContextManager",
    "Coroutine",
    "Counter",
    "DefaultDict",
    "Deque",
    "Dict",
    "Final",
    "FrozenSet",
    "Generator",
    "Generic",
    "Hashable",
    "ItemsView",
    "Iterable",
    "Iterator",
    "KeysView",
    "List",
    "Literal",
    "Mapping",
    "MappingView",
    "MutableMapping",
    "MutableSequence",
    "MutableSet",
    "NamedTuple",
    "NewType",
    "Optional",
    "Protocol",
    "Reversible",
    "Sequence",
    "Set",
    "Sized",
    "SupportsAbs",
    "SupportsBytes",
    "SupportsComplex",
    "SupportsFloat",
    "SupportsIndex",
    "SupportsInt",
    "SupportsRound",
    "Text",
    "Tuple",
    "Type",
    "TypeVar",
    "TypedDict",
    "Union",
    "ValuesView",
    "TYPE_CHECKING",
    "cast",
    "final",
    "get_args",
    "get_origin",
    "get_type_hints",
    "no_type_check",
    "no_type_check_decorator",
    "overload",
    "runtime_checkable",
    "ForwardRef",
    "NoReturn",
    "OrderedDict",
]

if sys.version_info >= (3, 9):
    __all__ += ["Annotated", "BinaryIO", "IO", "Match", "Pattern", "TextIO"]

if sys.version_info >= (3, 10):
    __all__ += ["Concatenate", "ParamSpec", "ParamSpecArgs", "ParamSpecKwargs", "TypeAlias", "TypeGuard", "is_typeddict"]

if sys.version_info >= (3, 11):
    __all__ += [
        "LiteralString",
        "Never",
        "NotRequired",
        "Required",
        "Self",
        "TypeVarTuple",
        "Unpack",
        "assert_never",
        "assert_type",
        "clear_overloads",
        "dataclass_transform",
        "get_overloads",
        "reveal_type",
    ]

if sys.version_info >= (3, 12):
    __all__ += ["TypeAliasType", "override"]

Any = object()

def final(f: _T) -> _T: ...
@final
class TypeVar:
    @property
    def __name__(self) -> str: ...
    @property
    def __bound__(self) -> Any | None: ...
    @property
    def __constraints__(self) -> tuple[Any, ...]: ...
    @property
    def __covariant__(self) -> bool: ...
    @property
    def __contravariant__(self) -> bool: ...
    if sys.version_info >= (3, 12):
        @property
        def __infer_variance__(self) -> bool: ...
        def __init__(
            self,
            name: str,
            *constraints: Any,
            bound: Any | None = None,
            covariant: bool = False,
            contravariant: bool = False,
            infer_variance: bool = False,
        ) -> None: ...
    else:
        def __init__(
            self, name: str, *constraints: Any, bound: Any | None = None, covariant: bool = False, contravariant: bool = False
        ) -> None: ...
    if sys.version_info >= (3, 10):
        def __or__(self, right: Any) -> _SpecialForm: ...
        def __ror__(self, left: Any) -> _SpecialForm: ...
    if sys.version_info >= (3, 11):
        def __typing_subst__(self, arg: Any) -> Any: ...

# Used for an undocumented mypy feature. Does not exist at runtime.
_promote = object()

# N.B. Keep this definition in sync with typing_extensions._SpecialForm
@final
class _SpecialForm:
    def __getitem__(self, parameters: Any) -> object: ...
    if sys.version_info >= (3, 10):
        def __or__(self, other: Any) -> _SpecialForm: ...
        def __ror__(self, other: Any) -> _SpecialForm: ...

Union: _SpecialForm
Generic: _SpecialForm
# Protocol is only present in 3.8 and later, but mypy needs it unconditionally
Protocol: _SpecialForm
Callable: _SpecialForm
Type: _SpecialForm
NoReturn: _SpecialForm
ClassVar: _SpecialForm

Optional: _SpecialForm
Tuple: _SpecialForm
Final: _SpecialForm

Literal: _SpecialForm
# TypedDict is a (non-subscriptable) special form.
TypedDict: object

if sys.version_info >= (3, 11):
    Self: _SpecialForm
    Never: _SpecialForm
    Unpack: _SpecialForm
    Required: _SpecialForm
    NotRequired: _SpecialForm
    LiteralString: _SpecialForm

    @final
    class TypeVarTuple:
        @property
        def __name__(self) -> str: ...
        def __init__(self, name: str) -> None: ...
        def __iter__(self) -> Any: ...
        def __typing_subst__(self, arg: Never) -> Never: ...
        def __typing_prepare_subst__(self, alias: Any, args: Any) -> tuple[Any, ...]: ...

if sys.version_info >= (3, 10):
    @final
    class ParamSpecArgs:
        @property
        def __origin__(self) -> ParamSpec: ...
        def __init__(self, origin: ParamSpec) -> None: ...
        def __eq__(self, other: object) -> bool: ...

    @final
    class ParamSpecKwargs:
        @property
        def __origin__(self) -> ParamSpec: ...
        def __init__(self, origin: ParamSpec) -> None: ...
        def __eq__(self, other: object) -> bool: ...

    @final
    class ParamSpec:
        @property
        def __name__(self) -> str: ...
        @property
        def __bound__(self) -> Any | None: ...
        @property
        def __covariant__(self) -> bool: ...
        @property
        def __contravariant__(self) -> bool: ...
        if sys.version_info >= (3, 12):
            @property
            def __infer_variance__(self) -> bool: ...
            def __init__(
                self,
                name: str,
                *,
                bound: Any | None = None,
                contravariant: bool = False,
                covariant: bool = False,
                infer_variance: bool = False,
            ) -> None: ...
        else:
            def __init__(
                self, name: str, *, bound: Any | None = None, contravariant: bool = False, covariant: bool = False
            ) -> None: ...

        @property
        def args(self) -> ParamSpecArgs: ...
        @property
        def kwargs(self) -> ParamSpecKwargs: ...
        if sys.version_info >= (3, 11):
            def __typing_subst__(self, arg: Any) -> Any: ...
            def __typing_prepare_subst__(self, alias: Any, args: Any) -> tuple[Any, ...]: ...

        def __or__(self, right: Any) -> _SpecialForm: ...
        def __ror__(self, left: Any) -> _SpecialForm: ...

    Concatenate: _SpecialForm
    TypeAlias: _SpecialForm
    TypeGuard: _SpecialForm

    class NewType:
        def __init__(self, name: str, tp: Any) -> None: ...
        if sys.version_info >= (3, 11):
            @staticmethod
            def __call__(x: _T, /) -> _T: ...
        else:
            def __call__(self, x: _T) -> _T: ...

        def __or__(self, other: Any) -> _SpecialForm: ...
        def __ror__(self, other: Any) -> _SpecialForm: ...
        __supertype__: type | NewType

else:
    def NewType(name: str, tp: Any) -> Any: ...

_F = TypeVar("_F", bound=Callable[..., Any])
_P = _ParamSpec("_P")
_T = TypeVar("_T")

# These type variables are used by the container types.
_S = TypeVar("_S")
_KT = TypeVar("_KT")  # Key type.
_VT = TypeVar("_VT")  # Value type.
_T_co = TypeVar("_T_co", covariant=True)  # Any type covariant containers.
_KT_co = TypeVar("_KT_co", covariant=True)  # Key type covariant containers.
_VT_co = TypeVar("_VT_co", covariant=True)  # Value type covariant containers.
_TC = TypeVar("_TC", bound=type[object])

def overload(func: _F) -> _F: ...
def no_type_check(arg: _F) -> _F: ...
def no_type_check_decorator(decorator: Callable[_P, _T]) -> Callable[_P, _T]: ...

# This itself is only available during type checking
def type_check_only(func_or_cls: _F) -> _F: ...

# Type aliases and type constructors

class _Alias:
    # Class for defining generic aliases for library types.
    def __getitem__(self, typeargs: Any) -> Any: ...

List = _Alias()
Dict = _Alias()
DefaultDict = _Alias()
Set = _Alias()
FrozenSet = _Alias()
Counter = _Alias()
Deque = _Alias()
ChainMap = _Alias()

OrderedDict = _Alias()

if sys.version_info >= (3, 9):
    Annotated: _SpecialForm

# Predefined type variables.
AnyStr = TypeVar("AnyStr", str, bytes)  # noqa: Y001

class _ProtocolMeta(ABCMeta):
    if sys.version_info >= (3, 12):
        def __init__(cls, *args: Any, **kwargs: Any) -> None: ...

# Abstract base classes.

def runtime_checkable(cls: _TC) -> _TC: ...
@runtime_checkable
class SupportsInt(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __int__(self) -> int: ...

@runtime_checkable
class SupportsFloat(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __float__(self) -> float: ...

@runtime_checkable
class SupportsComplex(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __complex__(self) -> complex: ...

@runtime_checkable
class SupportsBytes(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __bytes__(self) -> bytes: ...

@runtime_checkable
class SupportsIndex(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __index__(self) -> int: ...

@runtime_checkable
class SupportsAbs(Protocol[_T_co]):
    @abstractmethod
    def __abs__(self) -> _T_co: ...

@runtime_checkable
class SupportsRound(Protocol[_T_co]):
    @overload
    @abstractmethod
    def __round__(self) -> int: ...
    @overload
    @abstractmethod
    def __round__(self, ndigits: int, /) -> _T_co: ...

@runtime_checkable
class Sized(Protocol, metaclass=ABCMeta):
    @abstractmethod
    def __len__(self) -> int: ...

@runtime_checkable
class Hashable(Protocol, metaclass=ABCMeta):
    # TODO: This is special, in that a subclass of a hashable class may not be hashable
    #   (for example, list vs. object). It's not obvious how to represent this. This class
    #   is currently mostly useless for static checking.
    @abstractmethod
    def __hash__(self) -> int: ...

@runtime_checkable
class Iterable(Protocol[_T_co]):
    @abstractmethod
    def __iter__(self) -> Iterator[_T_co]: ...

@runtime_checkable
class Iterator(Iterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __next__(self) -> _T_co: ...
    def __iter__(self) -> Iterator[_T_co]: ...

@runtime_checkable
class Reversible(Iterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __reversed__(self) -> Iterator[_T_co]: ...

_YieldT_co = TypeVar("_YieldT_co", covariant=True)
_SendT_contra = TypeVar("_SendT_contra", contravariant=True)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True)

class Generator(Iterator[_YieldT_co], Generic[_YieldT_co, _SendT_contra, _ReturnT_co]):
    def __next__(self) -> _YieldT_co: ...
    @abstractmethod
    def send(self, value: _SendT_contra, /) -> _YieldT_co: ...
    @overload
    @abstractmethod
    def throw(
        self, typ: type[BaseException], val: BaseException | object = None, tb: TracebackType | None = None, /
    ) -> _YieldT_co: ...
    @overload
    @abstractmethod
    def throw(self, typ: BaseException, val: None = None, tb: TracebackType | None = None, /) -> _YieldT_co: ...
    def close(self) -> None: ...
    def __iter__(self) -> Generator[_YieldT_co, _SendT_contra, _ReturnT_co]: ...
    @property
    def gi_code(self) -> CodeType: ...
    @property
    def gi_frame(self) -> FrameType: ...
    @property
    def gi_running(self) -> bool: ...
    @property
    def gi_yieldfrom(self) -> Generator[Any, Any, Any] | None: ...

# NOTE: Technically we would like this to be able to accept a second parameter as well, just
#   like it's counterpart in contextlib, however `typing._SpecialGenericAlias` enforces the
#   correct number of arguments at runtime, so we would be hiding runtime errors.
@runtime_checkable
class ContextManager(AbstractContextManager[_T_co, bool | None], Protocol[_T_co]): ...

# NOTE: Technically we would like this to be able to accept a second parameter as well, just
#   like it's counterpart in contextlib, however `typing._SpecialGenericAlias` enforces the
#   correct number of arguments at runtime, so we would be hiding runtime errors.
@runtime_checkable
class AsyncContextManager(AbstractAsyncContextManager[_T_co, bool | None], Protocol[_T_co]): ...

@runtime_checkable
class Awaitable(Protocol[_T_co]):
    @abstractmethod
    def __await__(self) -> Generator[Any, None, _T_co]: ...

class Coroutine(Awaitable[_ReturnT_co], Generic[_YieldT_co, _SendT_contra, _ReturnT_co]):
    __name__: str
    __qualname__: str
    @property
    def cr_await(self) -> Any | None: ...
    @property
    def cr_code(self) -> CodeType: ...
    @property
    def cr_frame(self) -> FrameType | None: ...
    @property
    def cr_running(self) -> bool: ...
    @abstractmethod
    def send(self, value: _SendT_contra, /) -> _YieldT_co: ...
    @overload
    @abstractmethod
    def throw(
        self, typ: type[BaseException], val: BaseException | object = None, tb: TracebackType | None = None, /
    ) -> _YieldT_co: ...
    @overload
    @abstractmethod
    def throw(self, typ: BaseException, val: None = None, tb: TracebackType | None = None, /) -> _YieldT_co: ...
    @abstractmethod
    def close(self) -> None: ...

# NOTE: This type does not exist in typing.py or PEP 484 but mypy needs it to exist.
# The parameters correspond to Generator, but the 4th is the original type.
@type_check_only
class AwaitableGenerator(
    Awaitable[_ReturnT_co],
    Generator[_YieldT_co, _SendT_contra, _ReturnT_co],
    Generic[_YieldT_co, _SendT_contra, _ReturnT_co, _S],
    metaclass=ABCMeta,
): ...

@runtime_checkable
class AsyncIterable(Protocol[_T_co]):
    @abstractmethod
    def __aiter__(self) -> AsyncIterator[_T_co]: ...

@runtime_checkable
class AsyncIterator(AsyncIterable[_T_co], Protocol[_T_co]):
    @abstractmethod
    def __anext__(self) -> Awaitable[_T_co]: ...
    def __aiter__(self) -> AsyncIterator[_T_co]: ...

class AsyncGenerator(AsyncIterator[_YieldT_co], Generic[_YieldT_co, _SendT_contra]):
    def __anext__(self) -> Awaitable[_YieldT_co]: ...
    @abstractmethod
    def asend(self, value: _SendT_contra, /) -> Awaitable[_YieldT_co]: ...
    @overload
    @abstractmethod
    def athrow(
        self, typ: type[BaseException], val: BaseException | object = None, tb: TracebackType | None = None, /
    ) -> Awaitable[_YieldT_co]: ...
    @overload
    @abstractmethod
    def athrow(self, typ: BaseException, val: None = None, tb: TracebackType | None = None, /) -> Awaitable[_YieldT_co]: ...
    def aclose(self) -> Awaitable[None]: ...
    @property
    def ag_await(self) -> Any: ...
    @property
    def ag_code(self) -> CodeType: ...
    @property
    def ag_frame(self) -> FrameType: ...
    @property
    def ag_running(self) -> bool: ...

@runtime_checkable
class Container(Protocol[_T_co]):
    # This is generic more on vibes than anything else
    @abstractmethod
    def __contains__(self, x: object, /) -> bool: ...

@runtime_checkable
class Collection(Iterable[_T_co], Container[_T_co], Protocol[_T_co]):
    # Implement Sized (but don't have it as a base class).
    @abstractmethod
    def __len__(self) -> int: ...

class Sequence(Collection[_T_co], Reversible[_T_co]):
    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> _T_co: ...
    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> Sequence[_T_co]: ...
    # Mixin methods
    def index(self, value: Any, start: int = 0, stop: int = ...) -> int: ...
    def count(self, value: Any) -> int: ...
    def __contains__(self, value: object) -> bool: ...
    def __iter__(self) -> Iterator[_T_co]: ...
    def __reversed__(self) -> Iterator[_T_co]: ...

class MutableSequence(Sequence[_T]):
    @abstractmethod
    def insert(self, index: int, value: _T) -> None: ...
    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> _T: ...
    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> MutableSequence[_T]: ...
    @overload
    @abstractmethod
    def __setitem__(self, index: int, value: _T) -> None: ...
    @overload
    @abstractmethod
    def __setitem__(self, index: slice, value: Iterable[_T]) -> None: ...
    @overload
    @abstractmethod
    def __delitem__(self, index: int) -> None: ...
    @overload
    @abstractmethod
    def __delitem__(self, index: slice) -> None: ...
    # Mixin methods
    def append(self, value: _T) -> None: ...
    def clear(self) -> None: ...
    def extend(self, values: Iterable[_T]) -> None: ...
    def reverse(self) -> None: ...
    def pop(self, index: int = -1) -> _T: ...
    def remove(self, value: _T) -> None: ...
    def __iadd__(self, values: Iterable[_T]) -> typing_extensions.Self: ...

class AbstractSet(Collection[_T_co]):
    @abstractmethod
    def __contains__(self, x: object) -> bool: ...
    def _hash(self) -> int: ...
    # Mixin methods
    def __le__(self, other: AbstractSet[Any]) -> bool: ...
    def __lt__(self, other: AbstractSet[Any]) -> bool: ...
    def __gt__(self, other: AbstractSet[Any]) -> bool: ...
    def __ge__(self, other: AbstractSet[Any]) -> bool: ...
    def __and__(self, other: AbstractSet[Any]) -> AbstractSet[_T_co]: ...
    def __or__(self, other: AbstractSet[_T]) -> AbstractSet[_T_co | _T]: ...
    def __sub__(self, other: AbstractSet[Any]) -> AbstractSet[_T_co]: ...
    def __xor__(self, other: AbstractSet[_T]) -> AbstractSet[_T_co | _T]: ...
    def __eq__(self, other: object) -> bool: ...
    def isdisjoint(self, other: Iterable[Any]) -> bool: ...

class MutableSet(AbstractSet[_T]):
    @abstractmethod
    def add(self, value: _T) -> None: ...
    @abstractmethod
    def discard(self, value: _T) -> None: ...
    # Mixin methods
    def clear(self) -> None: ...
    def pop(self) -> _T: ...
    def remove(self, value: _T) -> None: ...
    def __ior__(self, it: AbstractSet[_T]) -> typing_extensions.Self: ...  # type: ignore[override,misc]
    def __iand__(self, it: AbstractSet[Any]) -> typing_extensions.Self: ...
    def __ixor__(self, it: AbstractSet[_T]) -> typing_extensions.Self: ...  # type: ignore[override,misc]
    def __isub__(self, it: AbstractSet[Any]) -> typing_extensions.Self: ...

class MappingView(Sized):
    def __init__(self, mapping: Mapping[Any, Any]) -> None: ...  # undocumented
    def __len__(self) -> int: ...

class ItemsView(MappingView, AbstractSet[tuple[_KT_co, _VT_co]], Generic[_KT_co, _VT_co]):
    def __init__(self, mapping: Mapping[_KT_co, _VT_co]) -> None: ...  # undocumented
    def __and__(self, other: Iterable[Any]) -> set[tuple[_KT_co, _VT_co]]: ...
    def __rand__(self, other: Iterable[_T]) -> set[_T]: ...
    def __contains__(self, item: object) -> bool: ...
    def __iter__(self) -> Iterator[tuple[_KT_co, _VT_co]]: ...
    def __reversed__(self) -> Iterator[tuple[_KT_co, _VT_co]]: ...
    def __or__(self, other: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...
    def __ror__(self, other: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...
    def __sub__(self, other: Iterable[Any]) -> set[tuple[_KT_co, _VT_co]]: ...
    def __rsub__(self, other: Iterable[_T]) -> set[_T]: ...
    def __xor__(self, other: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...
    def __rxor__(self, other: Iterable[_T]) -> set[tuple[_KT_co, _VT_co] | _T]: ...

class KeysView(MappingView, AbstractSet[_KT_co]):
    def __init__(self, mapping: Mapping[_KT_co, Any]) -> None: ...  # undocumented
    def __and__(self, other: Iterable[Any]) -> set[_KT_co]: ...
    def __rand__(self, other: Iterable[_T]) -> set[_T]: ...
    def __contains__(self, key: object) -> bool: ...
    def __iter__(self) -> Iterator[_KT_co]: ...
    def __reversed__(self) -> Iterator[_KT_co]: ...
    def __or__(self, other: Iterable[_T]) -> set[_KT_co | _T]: ...
    def __ror__(self, other: Iterable[_T]) -> set[_KT_co | _T]: ...
    def __sub__(self, other: Iterable[Any]) -> set[_KT_co]: ...
    def __rsub__(self, other: Iterable[_T]) -> set[_T]: ...
    def __xor__(self, other: Iterable[_T]) -> set[_KT_co | _T]: ...
    def __rxor__(self, other: Iterable[_T]) -> set[_KT_co | _T]: ...

class ValuesView(MappingView, Collection[_VT_co]):
    def __init__(self, mapping: Mapping[Any, _VT_co]) -> None: ...  # undocumented
    def __contains__(self, value: object) -> bool: ...
    def __iter__(self) -> Iterator[_VT_co]: ...
    def __reversed__(self) -> Iterator[_VT_co]: ...

class Mapping(Collection[_KT], Generic[_KT, _VT_co]):
    # TODO: We wish the key type could also be covariant, but that doesn't work,
    # see discussion in https://github.com/python/typing/pull/273.
    @abstractmethod
    def __getitem__(self, key: _KT, /) -> _VT_co: ...
    # Mixin methods
    @overload
    def get(self, key: _KT, /) -> _VT_co | None: ...
    @overload
    def get(self, key: _KT, /, default: _VT_co | _T) -> _VT_co | _T: ...
    def items(self) -> ItemsView[_KT, _VT_co]: ...
    def keys(self) -> KeysView[_KT]: ...
    def values(self) -> ValuesView[_VT_co]: ...
    def __contains__(self, key: object, /) -> bool: ...
    def __eq__(self, other: object, /) -> bool: ...

class MutableMapping(Mapping[_KT, _VT]):
    @abstractmethod
    def __setitem__(self, key: _KT, value: _VT, /) -> None: ...
    @abstractmethod
    def __delitem__(self, key: _KT, /) -> None: ...
    def clear(self) -> None: ...
    @overload
    def pop(self, key: _KT, /) -> _VT: ...
    @overload
    def pop(self, key: _KT, /, default: _VT) -> _VT: ...
    @overload
    def pop(self, key: _KT, /, default: _T) -> _VT | _T: ...
    def popitem(self) -> tuple[_KT, _VT]: ...
    # This overload should be allowed only if the value type is compatible with None.
    #
    # Keep the following methods in line with MutableMapping.setdefault, modulo positional-only differences:
    # -- collections.OrderedDict.setdefault
    # -- collections.ChainMap.setdefault
    # -- weakref.WeakKeyDictionary.setdefault
    @overload
    def setdefault(self: MutableMapping[_KT, _T | None], key: _KT, default: None = None, /) -> _T | None: ...
    @overload
    def setdefault(self, key: _KT, default: _VT, /) -> _VT: ...
    # 'update' used to take a Union, but using overloading is better.
    # The second overloaded type here is a bit too general, because
    # Mapping[tuple[_KT, _VT], W] is a subclass of Iterable[tuple[_KT, _VT]],
    # but will always have the behavior of the first overloaded type
    # at runtime, leading to keys of a mix of types _KT and tuple[_KT, _VT].
    # We don't currently have any way of forcing all Mappings to use
    # the first overload, but by using overloading rather than a Union,
    # mypy will commit to using the first overload when the argument is
    # known to be a Mapping with unknown type parameters, which is closer
    # to the behavior we want. See mypy issue  #1430.
    #
    # Various mapping classes have __ior__ methods that should be kept roughly in line with .update():
    # -- dict.__ior__
    # -- os._Environ.__ior__
    # -- collections.UserDict.__ior__
    # -- collections.ChainMap.__ior__
    # -- peewee.attrdict.__add__
    # -- peewee.attrdict.__iadd__
    # -- weakref.WeakValueDictionary.__ior__
    # -- weakref.WeakKeyDictionary.__ior__
    @overload
    def update(self, m: SupportsKeysAndGetItem[_KT, _VT], /, **kwargs: _VT) -> None: ...
    @overload
    def update(self, m: Iterable[tuple[_KT, _VT]], /, **kwargs: _VT) -> None: ...
    @overload
    def update(self, **kwargs: _VT) -> None: ...

Text = str

TYPE_CHECKING: bool

# In stubs, the arguments of the IO class are marked as positional-only.
# This differs from runtime, but better reflects the fact that in reality
# classes deriving from IO use different names for the arguments.
class IO(Iterator[AnyStr]):
    # At runtime these are all abstract properties,
    # but making them abstract in the stub is hugely disruptive, for not much gain.
    # See #8726
    @property
    def mode(self) -> str: ...
    # Usually str, but may be bytes if a bytes path was passed to open(). See #10737.
    # If PEP 696 becomes available, we may want to use a defaulted TypeVar here.
    @property
    def name(self) -> str | Any: ...
    @abstractmethod
    def close(self) -> None: ...
    @property
    def closed(self) -> bool: ...
    @abstractmethod
    def fileno(self) -> int: ...
    @abstractmethod
    def flush(self) -> None: ...
    @abstractmethod
    def isatty(self) -> bool: ...
    @abstractmethod
    def read(self, n: int = -1, /) -> AnyStr: ...
    @abstractmethod
    def readable(self) -> bool: ...
    @abstractmethod
    def readline(self, limit: int = -1, /) -> AnyStr: ...
    @abstractmethod
    def readlines(self, hint: int = -1, /) -> list[AnyStr]: ...
    @abstractmethod
    def seek(self, offset: int, whence: int = 0, /) -> int: ...
    @abstractmethod
    def seekable(self) -> bool: ...
    @abstractmethod
    def tell(self) -> int: ...
    @abstractmethod
    def truncate(self, size: int | None = None, /) -> int: ...
    @abstractmethod
    def writable(self) -> bool: ...
    @abstractmethod
    @overload
    def write(self: IO[str], s: str, /) -> int: ...
    @abstractmethod
    @overload
    def write(self: IO[bytes], s: ReadableBuffer, /) -> int: ...
    @abstractmethod
    @overload
    def write(self, s: AnyStr, /) -> int: ...
    @abstractmethod
    @overload
    def writelines(self: IO[str], lines: Iterable[str], /) -> None: ...
    @abstractmethod
    @overload
    def writelines(self: IO[bytes], lines: Iterable[ReadableBuffer], /) -> None: ...
    @abstractmethod
    @overload
    def writelines(self, lines: Iterable[AnyStr], /) -> None: ...
    @abstractmethod
    def __next__(self) -> AnyStr: ...
    @abstractmethod
    def __iter__(self) -> Iterator[AnyStr]: ...
    @abstractmethod
    def __enter__(self) -> IO[AnyStr]: ...
    @abstractmethod
    def __exit__(
        self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None, /
    ) -> None: ...

class BinaryIO(IO[bytes]):
    @abstractmethod
    def __enter__(self) -> BinaryIO: ...

class TextIO(IO[str]):
    # See comment regarding the @properties in the `IO` class
    @property
    def buffer(self) -> BinaryIO: ...
    @property
    def encoding(self) -> str: ...
    @property
    def errors(self) -> str | None: ...
    @property
    def line_buffering(self) -> int: ...  # int on PyPy, bool on CPython
    @property
    def newlines(self) -> Any: ...  # None, str or tuple
    @abstractmethod
    def __enter__(self) -> TextIO: ...

ByteString: typing_extensions.TypeAlias = bytes | bytearray | memoryview

# Functions

_get_type_hints_obj_allowed_types: typing_extensions.TypeAlias = (  # noqa: Y042
    object
    | Callable[..., Any]
    | FunctionType
    | BuiltinFunctionType
    | MethodType
    | ModuleType
    | WrapperDescriptorType
    | MethodWrapperType
    | MethodDescriptorType
)

if sys.version_info >= (3, 9):
    def get_type_hints(
        obj: _get_type_hints_obj_allowed_types,
        globalns: dict[str, Any] | None = None,
        localns: dict[str, Any] | None = None,
        include_extras: bool = False,
    ) -> dict[str, Any]: ...

else:
    def get_type_hints(
        obj: _get_type_hints_obj_allowed_types, globalns: dict[str, Any] | None = None, localns: dict[str, Any] | None = None
    ) -> dict[str, Any]: ...

def get_args(tp: Any) -> tuple[Any, ...]: ...

if sys.version_info >= (3, 10):
    @overload
    def get_origin(tp: ParamSpecArgs | ParamSpecKwargs) -> ParamSpec: ...
    @overload
    def get_origin(tp: UnionType) -> type[UnionType]: ...

if sys.version_info >= (3, 9):
    @overload
    def get_origin(tp: GenericAlias) -> type: ...
    @overload
    def get_origin(tp: Any) -> Any | None: ...

else:
    def get_origin(tp: Any) -> Any | None: ...

@overload
def cast(typ: type[_T], val: Any) -> _T: ...
@overload
def cast(typ: str, val: Any) -> Any: ...
@overload
def cast(typ: object, val: Any) -> Any: ...

if sys.version_info >= (3, 11):
    def reveal_type(obj: _T, /) -> _T: ...
    def assert_never(arg: Never, /) -> Never: ...
    def assert_type(val: _T, typ: Any, /) -> _T: ...
    def clear_overloads() -> None: ...
    def get_overloads(func: Callable[..., object]) -> Sequence[Callable[..., object]]: ...
    def dataclass_transform(
        *,
        eq_default: bool = True,
        order_default: bool = False,
        kw_only_default: bool = False,
        frozen_default: bool = False,  # on 3.11, runtime accepts it as part of kwargs
        field_specifiers: tuple[type[Any] | Callable[..., Any], ...] = (),
        **kwargs: Any,
    ) -> IdentityFunction: ...

# Type constructors

class NamedTuple(tuple[Any, ...]):
    if sys.version_info < (3, 9):
        _field_types: ClassVar[dict[str, type]]
    _field_defaults: ClassVar[dict[str, Any]]
    _fields: ClassVar[tuple[str, ...]]
    # __orig_bases__ sometimes exists on <3.12, but not consistently
    # So we only add it to the stub on 3.12+.
    if sys.version_info >= (3, 12):
        __orig_bases__: ClassVar[tuple[Any, ...]]

    @overload
    def __init__(self, typename: str, fields: Iterable[tuple[str, Any]], /) -> None: ...
    @overload
    @typing_extensions.deprecated(
        "Creating a typing.NamedTuple using keyword arguments is deprecated and support will be removed in Python 3.15"
    )
    def __init__(self, typename: str, fields: None = None, /, **kwargs: Any) -> None: ...
    @classmethod
    def _make(cls, iterable: Iterable[Any]) -> typing_extensions.Self: ...
    def _asdict(self) -> dict[str, Any]: ...
    def _replace(self, **kwargs: Any) -> typing_extensions.Self: ...

# Internal mypy fallback type for all typed dicts (does not exist at runtime)
# N.B. Keep this mostly in sync with typing_extensions._TypedDict/mypy_extensions._TypedDict
@type_check_only
class _TypedDict(Mapping[str, object], metaclass=ABCMeta):
    __total__: ClassVar[bool]
    if sys.version_info >= (3, 9):
        __required_keys__: ClassVar[frozenset[str]]
        __optional_keys__: ClassVar[frozenset[str]]
    # __orig_bases__ sometimes exists on <3.12, but not consistently,
    # so we only add it to the stub on 3.12+
    if sys.version_info >= (3, 12):
        __orig_bases__: ClassVar[tuple[Any, ...]]

    def copy(self) -> typing_extensions.Self: ...
    # Using Never so that only calls using mypy plugin hook that specialize the signature
    # can go through.
    def setdefault(self, k: _Never, default: object) -> object: ...
    # Mypy plugin hook for 'pop' expects that 'default' has a type variable type.
    def pop(self, k: _Never, default: _T = ...) -> object: ...  # pyright: ignore[reportInvalidTypeVarUse]
    def update(self: _T, m: _T, /) -> None: ...
    def __delitem__(self, k: _Never) -> None: ...
    def items(self) -> dict_items[str, object]: ...
    def keys(self) -> dict_keys[str, object]: ...
    def values(self) -> dict_values[str, object]: ...
    if sys.version_info >= (3, 9):
        @overload
        def __or__(self, value: typing_extensions.Self, /) -> typing_extensions.Self: ...
        @overload
        def __or__(self, value: dict[str, Any], /) -> dict[str, object]: ...
        @overload
        def __ror__(self, value: typing_extensions.Self, /) -> typing_extensions.Self: ...
        @overload
        def __ror__(self, value: dict[str, Any], /) -> dict[str, object]: ...
        # supposedly incompatible definitions of __or__ and __ior__
        def __ior__(self, value: typing_extensions.Self, /) -> typing_extensions.Self: ...  # type: ignore[misc]

@final
class ForwardRef:
    __forward_arg__: str
    __forward_code__: CodeType
    __forward_evaluated__: bool
    __forward_value__: Any | None
    __forward_is_argument__: bool
    __forward_is_class__: bool
    __forward_module__: Any | None
    if sys.version_info >= (3, 9):
        # The module and is_class arguments were added in later Python 3.9 versions.
        def __init__(self, arg: str, is_argument: bool = True, module: Any | None = None, *, is_class: bool = False) -> None: ...
    else:
        def __init__(self, arg: str, is_argument: bool = True) -> None: ...

    if sys.version_info >= (3, 9):
        def _evaluate(
            self, globalns: dict[str, Any] | None, localns: dict[str, Any] | None, recursive_guard: frozenset[str]
        ) -> Any | None: ...
    else:
        def _evaluate(self, globalns: dict[str, Any] | None, localns: dict[str, Any] | None) -> Any | None: ...

    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    if sys.version_info >= (3, 11):
        def __or__(self, other: Any) -> _SpecialForm: ...
        def __ror__(self, other: Any) -> _SpecialForm: ...

if sys.version_info >= (3, 10):
    def is_typeddict(tp: object) -> bool: ...

def _type_repr(obj: object) -> str: ...

if sys.version_info >= (3, 12):
    def override(method: _F, /) -> _F: ...
    @final
    class TypeAliasType:
        def __init__(
            self, name: str, value: Any, *, type_params: tuple[TypeVar | ParamSpec | TypeVarTuple, ...] = ()
        ) -> None: ...
        @property
        def __value__(self) -> Any: ...
        @property
        def __type_params__(self) -> tuple[TypeVar | ParamSpec | TypeVarTuple, ...]: ...
        @property
        def __parameters__(self) -> tuple[Any, ...]: ...
        @property
        def __name__(self) -> str: ...
        # It's writable on types, but not on instances of TypeAliasType.
        @property
        def __module__(self) -> str | None: ...  # type: ignore[override]
        def __getitem__(self, parameters: Any) -> Any: ...
        def __or__(self, right: Any) -> _SpecialForm: ...
        def __ror__(self, left: Any) -> _SpecialForm: ...

if sys.version_info >= (3, 13):
    def is_protocol(tp: type, /) -> bool: ...
    def get_protocol_members(tp: type, /) -> frozenset[str]: ...
