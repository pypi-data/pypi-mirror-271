from _typeshed import StrOrBytesPath, StrPath
from collections.abc import Iterator
from typing_extensions import Self

from _cffi_backend import _CDataBase

from ._pygit2 import Diff, Oid, Tree
from .enums import DiffOption, FileMode
from .repository import BaseRepository
from .utils import _IntoStrArray

class Index:
    def __init__(self, path: StrOrBytesPath | None = None) -> None: ...
    @classmethod
    def from_c(cls, repo: _CDataBase, ptr: _CDataBase) -> Index: ...
    def __del__(self) -> None: ...
    def __len__(self) -> int: ...
    def __contains__(self, path: StrOrBytesPath | None) -> bool: ...
    def __getitem__(self, key: StrPath | int) -> IndexEntry: ...
    def __iter__(self) -> Iterator[IndexEntry]: ...
    def read(self, force: bool = True) -> None: ...
    def write(self) -> None: ...
    def clear(self) -> None: ...
    def read_tree(self, tree: str | Oid | Tree) -> None: ...
    def write_tree(self, repo: BaseRepository | None = None) -> Oid: ...
    def remove(self, path: StrOrBytesPath, level: int = 0) -> None: ...
    def remove_all(self, pathspecs: _IntoStrArray) -> None: ...
    def add_all(self, pathspecs: _IntoStrArray = None) -> None: ...
    def add(self, path_or_entry: IndexEntry | StrPath) -> None: ...
    def diff_to_workdir(self, flags: DiffOption = ..., context_lines: int = 3, interhunk_lines: int = 0) -> Diff: ...
    def diff_to_tree(self, tree: Tree, flags: DiffOption = ..., context_lines: int = 3, interhunk_lines: int = 0) -> Diff: ...
    @property
    def conflicts(self) -> ConflictCollection | None: ...

class IndexEntry:
    path: str
    id: Oid
    mode: FileMode
    def __init__(self, path: str, object_id: Oid, mode: FileMode) -> None: ...
    @property
    def oid(self) -> Oid: ...
    @property
    def hex(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...

class ConflictCollection:
    def __init__(self, index: Index) -> None: ...
    def __getitem__(self, path: StrOrBytesPath) -> tuple[IndexEntry, IndexEntry, IndexEntry]: ...
    def __delitem__(self, path: StrOrBytesPath) -> None: ...
    def __iter__(self) -> ConflictIterator: ...
    def __contains__(self, path: StrOrBytesPath) -> bool: ...

class ConflictIterator:
    def __init__(self, index: Index) -> None: ...
    def __del__(self) -> None: ...
    def next(self) -> tuple[IndexEntry, IndexEntry, IndexEntry]: ...
    def __next__(self) -> tuple[IndexEntry, IndexEntry, IndexEntry]: ...
    def __iter__(self) -> Self: ...
