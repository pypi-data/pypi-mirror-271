import collections
from _typeshed import Incomplete
from types import TracebackType
from typing import Any, Literal

def encode_text(s: str) -> bytes: ...

PDFDocEncoding: dict[int, str]

def decode_text(b: bytes) -> str: ...

class PdfFormatError(RuntimeError): ...

def check_format_condition(condition, error_message) -> None: ...

class IndirectReference:
    def __bytes__(self) -> bytes: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self) -> int: ...

class IndirectObjectDef(IndirectReference): ...

class XrefTable:
    existing_entries: Incomplete
    new_entries: Incomplete
    deleted_entries: Incomplete
    reading_finished: bool
    def __init__(self) -> None: ...
    def __setitem__(self, key, value) -> None: ...
    def __getitem__(self, key): ...
    def __delitem__(self, key) -> None: ...
    def __contains__(self, key): ...
    def __len__(self) -> int: ...
    def keys(self): ...
    def write(self, f): ...

class PdfName:
    name: Incomplete
    def __init__(self, name) -> None: ...
    def name_as_str(self): ...
    def __eq__(self, other): ...
    def __hash__(self) -> int: ...
    @classmethod
    def from_pdf_stream(cls, data): ...
    allowed_chars: Incomplete
    def __bytes__(self) -> bytes: ...

class PdfArray(list[Any]):
    def __bytes__(self) -> bytes: ...

class PdfDict(collections.UserDict[bytes, Any]):
    def __setattr__(self, key: str, value) -> None: ...
    def __getattr__(self, key: str): ...
    def __bytes__(self) -> bytes: ...

class PdfBinary:
    data: Incomplete
    def __init__(self, data) -> None: ...
    def __bytes__(self) -> bytes: ...

class PdfStream:
    dictionary: Incomplete
    buf: Incomplete
    def __init__(self, dictionary, buf) -> None: ...
    def decode(self): ...

def pdf_repr(x) -> bytes: ...

class PdfParser:
    filename: Incomplete
    buf: Incomplete
    f: Incomplete
    start_offset: Incomplete
    should_close_buf: bool
    should_close_file: bool
    cached_objects: Incomplete
    file_size_total: int
    root: Incomplete
    root_ref: Incomplete
    info: Incomplete
    info_ref: Incomplete
    page_tree_root: Incomplete
    pages: Incomplete
    orig_pages: Incomplete
    pages_ref: Incomplete
    last_xref_section_offset: Incomplete
    trailer_dict: Incomplete
    xref_table: Incomplete
    def __init__(
        self,
        filename: Incomplete | None = None,
        f: Incomplete | None = None,
        buf: Incomplete | None = None,
        start_offset: int = 0,
        mode: str = "rb",
    ) -> None: ...
    def __enter__(self): ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> Literal[False]: ...
    def start_writing(self) -> None: ...
    def close_buf(self) -> None: ...
    def close(self) -> None: ...
    def seek_end(self) -> None: ...
    def write_header(self) -> None: ...
    def write_comment(self, s) -> None: ...
    def write_catalog(self): ...
    def rewrite_pages(self) -> None: ...
    def write_xref_and_trailer(self, new_root_ref: Incomplete | None = None) -> None: ...
    def write_page(self, ref, *objs, **dict_obj): ...
    def write_obj(self, ref, *objs, **dict_obj): ...
    def del_root(self) -> None: ...
    @staticmethod
    def get_buf_from_file(f): ...
    file_size_this: Incomplete
    def read_pdf_info(self) -> None: ...
    def next_object_id(self, offset: Incomplete | None = None): ...
    delimiter: bytes
    delimiter_or_ws: bytes
    whitespace: bytes
    whitespace_or_hex: bytes
    whitespace_optional: Incomplete
    whitespace_mandatory: Incomplete
    whitespace_optional_no_nl: bytes
    newline_only: bytes
    newline: Incomplete
    re_trailer_end: Incomplete
    re_trailer_prev: Incomplete
    def read_trailer(self) -> None: ...
    def read_prev_trailer(self, xref_section_offset) -> None: ...
    re_whitespace_optional: Incomplete
    re_name: Incomplete
    re_dict_start: Incomplete
    re_dict_end: Incomplete
    @classmethod
    def interpret_trailer(cls, trailer_data): ...
    re_hashes_in_name: Incomplete
    @classmethod
    def interpret_name(cls, raw, as_text: bool = False): ...
    re_null: Incomplete
    re_true: Incomplete
    re_false: Incomplete
    re_int: Incomplete
    re_real: Incomplete
    re_array_start: Incomplete
    re_array_end: Incomplete
    re_string_hex: Incomplete
    re_string_lit: Incomplete
    re_indirect_reference: Incomplete
    re_indirect_def_start: Incomplete
    re_indirect_def_end: Incomplete
    re_comment: Incomplete
    re_stream_start: Incomplete
    re_stream_end: Incomplete
    @classmethod
    def get_value(cls, data, offset, expect_indirect: Incomplete | None = None, max_nesting: int = -1): ...
    re_lit_str_token: Incomplete
    escaped_chars: Incomplete
    @classmethod
    def get_literal_string(cls, data, offset): ...
    re_xref_section_start: Incomplete
    re_xref_subsection_start: Incomplete
    re_xref_entry: Incomplete
    def read_xref_table(self, xref_section_offset): ...
    def read_indirect(self, ref, max_nesting: int = -1): ...
    def linearize_page_tree(self, node: Incomplete | None = None): ...
