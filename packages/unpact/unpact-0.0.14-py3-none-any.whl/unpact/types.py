import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Protocol, Tuple, TypedDict, Union, runtime_checkable

if sys.version_info < (3, 12):
    from typing_extensions import TypedDict  # noqa: F811
else:
    from typing import TypedDict

__all__ = ["ColumnDef", "ColumnFormatterType", "ColumnSpecDict"]


@runtime_checkable
class IndexFormatter(Protocol):
    def __call__(self, data: Any, index: int = ...):
        ...  # pragma: no cover


ColumnFormatterType = Union[IndexFormatter, Callable[[Any], Any], Callable[[Any, int], Any]]


class ColumnSpecDict(TypedDict, total=False):
    name: str
    formatter: ColumnFormatterType


@dataclass
class ColumnSpec:
    path: str
    name: Optional[str] = field(default=None)
    formatter: Optional[ColumnFormatterType] = field(default=None)

    @classmethod
    def from_tuple(cls, column_def: Tuple[str, ColumnSpecDict]) -> "ColumnSpec":
        path, spec = column_def
        return cls(path, **spec)

    @classmethod
    def from_str(cls, path: str) -> "ColumnSpec":
        return cls(path)

    @classmethod
    def from_def(cls, column_def: "ColumnDef") -> "ColumnSpec":
        if isinstance(column_def, str):
            return cls.from_str(column_def)

        elif isinstance(column_def, tuple):
            return cls.from_tuple(column_def)
        return column_def


ColumnDef = Union[Tuple[str, ColumnSpecDict], str, ColumnSpec]
