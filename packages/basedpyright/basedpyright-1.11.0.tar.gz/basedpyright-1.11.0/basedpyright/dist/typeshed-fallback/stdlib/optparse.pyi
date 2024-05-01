from _typeshed import Incomplete
from abc import abstractmethod
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import IO, Any, AnyStr, Literal, overload

__all__ = [
    "Option",
    "make_option",
    "SUPPRESS_HELP",
    "SUPPRESS_USAGE",
    "Values",
    "OptionContainer",
    "OptionGroup",
    "OptionParser",
    "HelpFormatter",
    "IndentedHelpFormatter",
    "TitledHelpFormatter",
    "OptParseError",
    "OptionError",
    "OptionConflictError",
    "OptionValueError",
    "BadOptionError",
    "check_choice",
]

NO_DEFAULT: tuple[str, ...]
SUPPRESS_HELP: str
SUPPRESS_USAGE: str

def check_builtin(option: Option, opt, value: str): ...
def check_choice(option: Option, opt, value: str) -> str: ...

class OptParseError(Exception):
    msg: str
    def __init__(self, msg: str) -> None: ...

class BadOptionError(OptParseError):
    opt_str: str
    def __init__(self, opt_str: str) -> None: ...

class AmbiguousOptionError(BadOptionError):
    possibilities: Iterable[str]
    def __init__(self, opt_str: str, possibilities: Sequence[str]) -> None: ...

class OptionError(OptParseError):
    option_id: str
    def __init__(self, msg: str, option: Option) -> None: ...

class OptionConflictError(OptionError): ...
class OptionValueError(OptParseError): ...

class HelpFormatter:
    NO_DEFAULT_VALUE: str
    _long_opt_fmt: str
    _short_opt_fmt: str
    current_indent: int
    default_tag: str
    help_position: int
    help_width: int | Any  # initialized as None and computed later as int when storing option strings
    indent_increment: int
    level: int
    max_help_position: int
    option_strings: dict[Option, str]
    parser: OptionParser
    short_first: Incomplete
    width: int
    def __init__(self, indent_increment: int, max_help_position: int, width: int | None, short_first: int) -> None: ...
    def dedent(self) -> None: ...
    def expand_default(self, option: Option) -> str: ...
    def format_description(self, description: str | None) -> str: ...
    def format_epilog(self, epilog: str | None) -> str: ...
    @abstractmethod
    def format_heading(self, heading: str) -> str: ...
    def format_option(self, option: Option) -> str: ...
    def format_option_strings(self, option: Option) -> str: ...
    @abstractmethod
    def format_usage(self, usage: str) -> str: ...
    def indent(self) -> None: ...
    def set_long_opt_delimiter(self, delim: str) -> None: ...
    def set_parser(self, parser: OptionParser) -> None: ...
    def set_short_opt_delimiter(self, delim: str) -> None: ...
    def store_option_strings(self, parser: OptionParser) -> None: ...

class IndentedHelpFormatter(HelpFormatter):
    def __init__(
        self, indent_increment: int = 2, max_help_position: int = 24, width: int | None = None, short_first: int = 1
    ) -> None: ...
    def format_heading(self, heading: str) -> str: ...
    def format_usage(self, usage: str) -> str: ...

class TitledHelpFormatter(HelpFormatter):
    def __init__(
        self, indent_increment: int = 0, max_help_position: int = 24, width: int | None = None, short_first: int = 0
    ) -> None: ...
    def format_heading(self, heading: str) -> str: ...
    def format_usage(self, usage: str) -> str: ...

class Option:
    ACTIONS: tuple[str, ...]
    ALWAYS_TYPED_ACTIONS: tuple[str, ...]
    ATTRS: list[str]
    CHECK_METHODS: list[Callable[..., Incomplete]] | None
    CONST_ACTIONS: tuple[str, ...]
    STORE_ACTIONS: tuple[str, ...]
    TYPED_ACTIONS: tuple[str, ...]
    TYPES: tuple[str, ...]
    TYPE_CHECKER: dict[str, Callable[[Option, str, Incomplete], Any]]
    _long_opts: list[str]
    _short_opts: list[str]
    action: str
    dest: str | None
    default: Incomplete
    nargs: int
    type: Incomplete
    callback: Callable[..., Incomplete] | None
    callback_args: tuple[Incomplete, ...] | None
    callback_kwargs: dict[str, Incomplete] | None
    help: str | None
    metavar: str | None
    def __init__(self, *opts: str | None, **attrs) -> None: ...
    def _check_action(self) -> None: ...
    def _check_callback(self) -> None: ...
    def _check_choice(self) -> None: ...
    def _check_const(self) -> None: ...
    def _check_dest(self) -> None: ...
    def _check_nargs(self) -> None: ...
    def _check_opt_strings(self, opts: Iterable[str | None]) -> list[str]: ...
    def _check_type(self) -> None: ...
    def _set_attrs(self, attrs: dict[str, Incomplete]) -> None: ...
    def _set_opt_strings(self, opts: Iterable[str]) -> None: ...
    def check_value(self, opt: str, value): ...
    def convert_value(self, opt: str, value): ...
    def get_opt_string(self) -> str: ...
    def process(self, opt, value, values, parser: OptionParser) -> int: ...
    def take_action(self, action: str, dest: str, opt, value, values, parser: OptionParser) -> int: ...
    def takes_value(self) -> bool: ...

make_option = Option

class OptionContainer:
    _long_opt: dict[str, Option]
    _short_opt: dict[str, Option]
    conflict_handler: str
    defaults: dict[str, Incomplete]
    description: str | None
    option_class: type[Option]
    def __init__(
        self, option_class: type[Option], conflict_handler: Literal["error", "resolve"], description: str | None
    ) -> None: ...
    def _check_conflict(self, option: Option) -> None: ...
    def _create_option_mappings(self) -> None: ...
    def _share_option_mappings(self, parser: OptionParser) -> None: ...
    @overload
    def add_option(self, opt: Option) -> Option: ...
    @overload
    def add_option(self, arg: str, /, *args: str | None, **kwargs) -> Option: ...
    def add_options(self, option_list: Iterable[Option]) -> None: ...
    def destroy(self) -> None: ...
    def format_option_help(self, formatter: HelpFormatter) -> str: ...
    def format_description(self, formatter: HelpFormatter) -> str: ...
    def format_help(self, formatter: HelpFormatter) -> str: ...
    def get_description(self) -> str | None: ...
    def get_option(self, opt_str: str) -> Option | None: ...
    def has_option(self, opt_str: str) -> bool: ...
    def remove_option(self, opt_str: str) -> None: ...
    def set_conflict_handler(self, handler: Literal["error", "resolve"]) -> None: ...
    def set_description(self, description: str | None) -> None: ...

class OptionGroup(OptionContainer):
    option_list: list[Option]
    parser: OptionParser
    title: str
    def __init__(self, parser: OptionParser, title: str, description: str | None = None) -> None: ...
    def _create_option_list(self) -> None: ...
    def set_title(self, title: str) -> None: ...

class Values:
    def __init__(self, defaults: Mapping[str, Incomplete] | None = None) -> None: ...
    def _update(self, dict: Mapping[str, Incomplete], mode) -> None: ...
    def _update_careful(self, dict: Mapping[str, Incomplete]) -> None: ...
    def _update_loose(self, dict: Mapping[str, Incomplete]) -> None: ...
    def ensure_value(self, attr: str, value): ...
    def read_file(self, filename: str, mode: str = "careful") -> None: ...
    def read_module(self, modname: str, mode: str = "careful") -> None: ...
    def __getattr__(self, name: str): ...
    def __setattr__(self, name: str, value, /) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class OptionParser(OptionContainer):
    allow_interspersed_args: bool
    epilog: str | None
    formatter: HelpFormatter
    largs: list[str] | None
    option_groups: list[OptionGroup]
    option_list: list[Option]
    process_default_values: bool
    prog: str | None
    rargs: list[str] | None
    standard_option_list: list[Option]
    usage: str | None
    values: Values | None
    version: str
    def __init__(
        self,
        usage: str | None = None,
        option_list: Iterable[Option] | None = None,
        option_class: type[Option] = ...,
        version: str | None = None,
        conflict_handler: str = "error",
        description: str | None = None,
        formatter: HelpFormatter | None = None,
        add_help_option: bool = True,
        prog: str | None = None,
        epilog: str | None = None,
    ) -> None: ...
    def _add_help_option(self) -> None: ...
    def _add_version_option(self) -> None: ...
    def _create_option_list(self) -> None: ...
    def _get_all_options(self) -> list[Option]: ...
    def _get_args(self, args: Iterable[Incomplete]) -> list[Incomplete]: ...
    def _init_parsing_state(self) -> None: ...
    def _match_long_opt(self, opt: str) -> str: ...
    def _populate_option_list(self, option_list: Iterable[Option], add_help: bool = True) -> None: ...
    def _process_args(self, largs: list[Incomplete], rargs: list[Incomplete], values: Values) -> None: ...
    def _process_long_opt(self, rargs: list[Incomplete], values) -> None: ...
    def _process_short_opts(self, rargs: list[Incomplete], values) -> None: ...
    @overload
    def add_option_group(self, opt_group: OptionGroup, /) -> OptionGroup: ...
    @overload
    def add_option_group(self, *args, **kwargs) -> OptionGroup: ...
    def check_values(self, values: Values, args: list[str]) -> tuple[Values, list[str]]: ...
    def disable_interspersed_args(self) -> None: ...
    def enable_interspersed_args(self) -> None: ...
    def error(self, msg: str) -> None: ...
    def exit(self, status: int = 0, msg: str | None = None) -> None: ...
    def expand_prog_name(self, s: str) -> str: ...
    def format_epilog(self, formatter: HelpFormatter) -> str: ...
    def format_help(self, formatter: HelpFormatter | None = None) -> str: ...
    def format_option_help(self, formatter: HelpFormatter | None = None) -> str: ...
    def get_default_values(self) -> Values: ...
    def get_option_group(self, opt_str: str) -> OptionGroup | None: ...
    def get_prog_name(self) -> str: ...
    def get_usage(self) -> str: ...
    def get_version(self) -> str: ...
    @overload
    def parse_args(self, args: None = None, values: Values | None = None) -> tuple[Values, list[str]]: ...
    @overload
    def parse_args(self, args: Sequence[AnyStr], values: Values | None = None) -> tuple[Values, list[AnyStr]]: ...
    def print_usage(self, file: IO[str] | None = None) -> None: ...
    def print_help(self, file: IO[str] | None = None) -> None: ...
    def print_version(self, file: IO[str] | None = None) -> None: ...
    def set_default(self, dest, value) -> None: ...
    def set_defaults(self, **kwargs) -> None: ...
    def set_process_default_values(self, process) -> None: ...
    def set_usage(self, usage: str) -> None: ...
