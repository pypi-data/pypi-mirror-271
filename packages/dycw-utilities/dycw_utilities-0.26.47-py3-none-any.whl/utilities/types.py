from __future__ import annotations

import datetime as dt
from collections.abc import Hashable, Mapping, Sized
from collections.abc import Set as AbstractSet
from dataclasses import dataclass
from inspect import iscoroutinefunction, isfunction
from pathlib import Path
from typing import Any, TypeGuard, TypeVar, overload

from typing_extensions import override

Number = int | float
Duration = Number | dt.timedelta
SequenceStrs = list[str] | tuple[str, ...]
IterableStrs = SequenceStrs | AbstractSet[str] | Mapping[str, Any]
PathLike = Path | str


_T = TypeVar("_T")
_U = TypeVar("_U")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")


def ensure_bool(obj: Any, /) -> bool:
    """Ensure an object is a boolean."""
    try:
        return ensure_class(obj, bool)
    except EnsureClassError as error:
        raise EnsureBoolError(obj=error.obj) from None


@dataclass(kw_only=True)
class EnsureBoolError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return f"Object {self.obj} must be a boolean; got {get_class_name(self.obj)} instead"


@overload
def ensure_class(obj: Any, cls: type[_T], /) -> _T: ...


@overload
def ensure_class(obj: Any, cls: tuple[type[_T1], type[_T2]], /) -> _T1 | _T2: ...


@overload
def ensure_class(
    obj: Any, cls: tuple[type[_T1], type[_T2], type[_T3]], /
) -> _T1 | _T2 | _T3: ...


@overload
def ensure_class(
    obj: Any, cls: tuple[type[_T1], type[_T2], type[_T3], type[_T4]], /
) -> _T1 | _T2 | _T3 | _T4: ...


@overload
def ensure_class(
    obj: Any, cls: tuple[type[_T1], type[_T2], type[_T3], type[_T4], type[_T5]], /
) -> _T1 | _T2 | _T3 | _T4 | _T5: ...


def ensure_class(obj: Any, cls: type[_T] | tuple[type[_T], ...], /) -> _T:  # type: ignore[]
    """Ensure an object is of the required class."""
    if isinstance(obj, cls):
        return obj
    raise EnsureClassError(obj=obj, cls=cls)


@dataclass(kw_only=True)
class EnsureClassError(Exception):
    obj: Any
    cls: type[Any] | tuple[type[Any], ...]

    @override
    def __str__(self) -> str:
        return f"Object {self.obj} must be an instance of {self.cls}; got {type(self.obj)}."


def ensure_date(obj: Any, /) -> dt.date:
    """Ensure an object is a date."""
    try:
        return ensure_class(obj, dt.date)
    except EnsureClassError as error:
        raise EnsureDateError(obj=error.obj) from None


@dataclass(kw_only=True)
class EnsureDateError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return (
            f"Object {self.obj} must be a date; got {get_class_name(self.obj)} instead"
        )


def ensure_datetime(obj: Any, /) -> dt.datetime:
    """Ensure an object is a datetime."""
    try:
        return ensure_class(obj, dt.datetime)
    except EnsureClassError as error:
        raise EnsureDatetimeError(obj=error.obj) from None


@dataclass(kw_only=True)
class EnsureDatetimeError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return f"Object {self.obj} must be a datetime; got {get_class_name(self.obj)} instead"


def ensure_float(obj: Any, /) -> float:
    """Ensure an object is a float."""
    try:
        return ensure_class(obj, float)
    except EnsureClassError as error:
        raise EnsureFloatError(obj=error.obj) from None


@dataclass(kw_only=True)
class EnsureFloatError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return (
            f"Object {self.obj} must be a float; got {get_class_name(self.obj)} instead"
        )


def ensure_hashable(obj: Any, /) -> Hashable:
    """Ensure an object is hashable."""
    if is_hashable(obj):
        return obj
    raise EnsureHashableError(obj=obj)


@dataclass(kw_only=True)
class EnsureHashableError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return f"Object {self.obj} must be hashable."


def ensure_int(obj: Any, /) -> int:
    """Ensure an object is an integer."""
    try:
        return ensure_class(obj, int)
    except EnsureClassError as error:
        raise EnsureIntError(obj=error.obj) from None


@dataclass(kw_only=True)
class EnsureIntError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return f"Object {self.obj} must be an integer; got {get_class_name(self.obj)} instead"


def ensure_not_none(obj: _T | None, /) -> _T:
    """Ensure an object is not None."""
    if obj is None:
        raise EnsureNotNoneError
    return obj


@dataclass(kw_only=True)
class EnsureNotNoneError(Exception):
    @override
    def __str__(self) -> str:
        return "Object must not be None."


def ensure_number(obj: Any, /) -> Number:
    """Ensure an object is a number."""
    try:
        return ensure_class(obj, Number)
    except EnsureClassError as error:
        raise EnsureNumberError(obj=error.obj) from None


@dataclass(kw_only=True)
class EnsureNumberError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return f"Object {self.obj} must be a number; got {get_class_name(self.obj)} instead"


def ensure_sized(obj: Any, /) -> Sized:
    """Ensure an object is sized."""
    if is_sized(obj):
        return obj
    raise EnsureSizedError(obj=obj)


@dataclass(kw_only=True)
class EnsureSizedError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return f"Object {self.obj} must be sized."


def ensure_sized_not_str(obj: Any, /) -> Sized:
    """Ensure an object is sized, but not a string."""
    if is_sized_not_str(obj):
        return obj
    raise EnsureSizedNotStrError(obj=obj)


@dataclass(kw_only=True)
class EnsureSizedNotStrError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return f"Object {self.obj} must be sized, but not a string."


@overload
def get_class(obj: type[_T], /) -> type[_T]: ...


@overload
def get_class(obj: _T, /) -> type[_T]: ...


def get_class(obj: _T | type[_T], /) -> type[_T]:
    """Get the class of an object, unless it is already a class."""
    return obj if isinstance(obj, type) else type(obj)


def get_class_name(obj: Any, /) -> str:
    """Get the name of the class of an object, unless it is already a class."""
    return get_class(obj).__name__


def if_not_none(x: _T | None, y: _U, /) -> _T | _U:
    """Return the first value if it is not None, else the second value."""
    return x if x is not None else y


def is_function_async(obj: Any, /) -> bool:
    """Check if a function is asynchronous."""

    if iscoroutinefunction(obj):
        return True
    if isfunction(obj):
        return False
    raise IsFunctionAsyncError(obj=obj)


@dataclass(kw_only=True)
class IsFunctionAsyncError(Exception):
    obj: Any

    @override
    def __str__(self) -> str:
        return f"Object must be a function; got {self.obj}."


def is_hashable(obj: Any, /) -> TypeGuard[Hashable]:
    """Check if an object is hashable."""
    try:
        _ = hash(obj)
    except TypeError:
        return False
    return True


def issubclass_except_bool_int(x: type[Any], y: type[Any], /) -> bool:
    """Checks for the subclass relation, except bool < int."""
    return issubclass(x, y) and not (issubclass(x, bool) and issubclass(int, y))


def is_sized(obj: Any, /) -> TypeGuard[Sized]:
    """Check if an object is sized."""
    try:
        _ = len(obj)
    except TypeError:
        return False
    return True


def is_sized_not_str(obj: Any, /) -> TypeGuard[Sized]:
    """Check if an object is sized, but not a string."""
    return is_sized(obj) and not isinstance(obj, str)


__all__ = [
    "Duration",
    "EnsureBoolError",
    "EnsureClassError",
    "EnsureDateError",
    "EnsureDatetimeError",
    "EnsureFloatError",
    "EnsureHashableError",
    "EnsureIntError",
    "EnsureNotNoneError",
    "EnsureNumberError",
    "EnsureSizedError",
    "EnsureSizedNotStrError",
    "IsFunctionAsyncError",
    "IterableStrs",
    "Number",
    "PathLike",
    "SequenceStrs",
    "ensure_bool",
    "ensure_class",
    "ensure_date",
    "ensure_datetime",
    "ensure_float",
    "ensure_hashable",
    "ensure_int",
    "ensure_not_none",
    "ensure_number",
    "ensure_sized",
    "ensure_sized_not_str",
    "get_class",
    "get_class_name",
    "if_not_none",
    "is_function_async",
    "is_hashable",
    "is_sized",
    "is_sized_not_str",
    "issubclass_except_bool_int",
]
