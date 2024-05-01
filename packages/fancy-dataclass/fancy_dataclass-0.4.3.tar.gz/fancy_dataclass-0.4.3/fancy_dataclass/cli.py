from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from contextlib import suppress
from dataclasses import MISSING, dataclass, fields
from enum import IntEnum
from typing import Any, Callable, ClassVar, Dict, List, Literal, Optional, Sequence, Type, TypeVar, Union, get_args, get_origin

from typing_extensions import Self

from fancy_dataclass.mixin import DataclassMixin, FieldSettings
from fancy_dataclass.utils import check_dataclass, issubclass_safe, type_is_optional


T = TypeVar('T')


@dataclass
class ArgparseDataclassFieldSettings(FieldSettings):
    """Settings for [`ArgparseDataclass`][fancy_dataclass.cli.ArgparseDataclass] fields.

    Each field may define a `metadata` dict containing any of the following entries:

    - `type`: override the dataclass field type with a different type
    - `args`: lists the command-line arguments explicitly
    - `action`: type of action taken when the argument is encountered
    - `nargs`: number of command-line arguments (use `*` for lists, `+` for non-empty lists
    - `const`: constant value required by some action/nargs combinations
    - `choices`: list of possible inputs allowed
    - `help`: help string
    - `metavar`: name for the argument in usage messages
    - `group`: name of the argument group in which to put the argument; the group will be created if it does not already exist in the parser
    - `parse_exclude`: boolean flag indicating that the field should not be included in the parser

    Note that these line up closely with the usual options that can be passed to [`ArgumentParser.add_argument`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument).

    **Positional arguments vs. options**:

    - If a field explicitly lists arguments in the `args` metadata field, the argument will be an option if the first listed argument starts with a dash, otherwise it will be a positional argument.
        - If it is an option but specifies no default value, it will be a required option.
    - If `args` are absent, the field will be an option if either (1) it specifies a default value, or (2) it is a boolean type; otherwise it is a positional argument.
    """
    type: Optional[Union[type, Callable[[Any], Any]]] = None  # can be used to define custom constructor
    args: Optional[Union[str, Sequence[str]]] = None
    action: Optional[str] = None
    nargs: Optional[Union[str, int]] = None
    const: Optional[Any] = None
    choices: Optional[Sequence[Any]] = None
    help: Optional[str] = None
    metavar: Optional[Union[str, Sequence[str]]] = None
    group: Optional[str] = None
    parse_exclude: bool = False


class ArgparseDataclass(DataclassMixin):
    """Mixin class providing a means of setting up an [`argparse`](https://docs.python.org/3/library/argparse.html) parser with the dataclass fields, and then converting the namespace of parsed arguments into an instance of the class.

    The parser's argument names and types will be derived from the dataclass's fields.

    Per-field settings can be passed into the `metadata` argument of each `dataclasses.field`. See [`ArgparseDataclassFieldSettings`][fancy_dataclass.cli.ArgparseDataclassFieldSettings] for the full list of settings."""

    __field_settings_type__ = ArgparseDataclassFieldSettings

    @classmethod
    def parser_class(cls) -> Type[ArgumentParser]:
        """Gets the type of the top-level argument parser.

        Returns:
            Type (subclass of `argparse.ArgumentParser`) to be constructed by this class"""
        return ArgumentParser

    @classmethod
    def parser_description(cls) -> Optional[str]:
        """Gets a description string for the top-level argument parser, which will be displayed by default when `--help` is passed to the parser.

        By default, uses the class's own docstring.

        Returns:
            String to be used as the program's description"""
        return cls.__doc__

    @classmethod
    def parser_kwargs(cls) -> Dict[str, Any]:
        """Gets keyword arguments that will be passed to the top-level argument parser.

        Returns:
            Keyword arguments passed upon construction of the `ArgumentParser`"""
        return {'description' : cls.parser_description()}

    @classmethod
    def parser_argument_kwarg_names(cls) -> List[str]:
        """Gets keyword argument names that will be passed when adding arguments to the argument parser.

        Returns:
            Keyword argument names passed when adding arguments to the parser"""
        return ['action', 'nargs', 'const', 'choices', 'help', 'metavar']

    @classmethod
    def new_parser(cls) -> ArgumentParser:
        """Constructs a new top-level argument parser..

        Returns:
            New top-level parser derived from the class's fields"""
        return cls.parser_class()(**cls.parser_kwargs())

    @classmethod
    def configure_argument(cls, parser: ArgumentParser, name: str) -> None:
        """Given an argument parser and a field name, configures the parser with an argument of that name.

        Attempts to provide reasonable default behavior based on the dataclass field name, type, default, and metadata.

        Subclasses may override this method to implement custom behavior.

        Args:
            parser: parser object to update with a new argument
            name: Name of the argument to configure"""
        kwargs: Dict[str, Any] = {}
        fld = cls.__dataclass_fields__[name]  # type: ignore[attr-defined]
        settings = cls._field_settings(fld).adapt_to(ArgparseDataclassFieldSettings)
        if settings.parse_exclude:  # exclude the argument from the parser
            return
        if (group_name := settings.group) is not None:  # add argument to a group instead of the main parser
            for group in getattr(parser, '_action_groups', []):  # get argument group with the given name
                if getattr(group, 'title', None) == group_name:
                    break
            else:  # group not found, so create it
                group_kwargs = {}
                if issubclass_safe(fld.type, ArgparseDataclass):  # get kwargs from nested ArgparseDataclass
                    group_kwargs = fld.type.parser_kwargs()
                group = parser.add_argument_group(group_name, **group_kwargs)
            parser = group
        if issubclass_safe(fld.type, ArgparseDataclass):
            # recursively configure a nested ArgparseDataclass field
            fld.type.configure_parser(parser)
            return
        # determine the type of the parser argument for the field
        tp = settings.type or fld.type
        action = settings.action or 'store'
        origin_type = get_origin(tp)
        if origin_type is not None:  # compound type
            if type_is_optional(tp):  # type: ignore[arg-type]
                kwargs['default'] = None
            if origin_type == ClassVar:  # by default, exclude ClassVars from the parser
                return
            tp_args = get_args(tp)
            if tp_args:  # extract the first wrapped type (should handle List/Optional/Union)
                tp = tp_args[0]
                if origin_type == Literal:  # literal options will become choices
                    tp = type(tp)
                    kwargs['choices'] = tp_args
            else:  # type cannot be inferred
                raise ValueError(f'cannot infer type of items in field {name!r}')
            if issubclass_safe(origin_type, list) and (action == 'store'):
                kwargs['nargs'] = '*'  # allow multiple arguments by default
        if issubclass_safe(tp, IntEnum):  # type: ignore[arg-type]
            # use a bare int type
            tp = int
        kwargs['type'] = tp
        # determine the default value
        if fld.default == MISSING:
            if fld.default_factory != MISSING:
                kwargs['default'] = fld.default_factory()
        else:
            kwargs['default'] = fld.default
        # get the names of the arguments associated with the field
        args = settings.args
        if args is not None:
            if isinstance(args, str):
                args = [args]
            # argument is positional if it is explicitly given without a leading dash
            positional = not args[0].startswith('-')
            if (not positional) and ('default' not in kwargs):
                # no default available, so make the field a required option
                kwargs['required'] = True
        else:
            argname = fld.name.replace('_', '-')
            positional = (tp is not bool) and ('default' not in kwargs)
            if positional:
                args = [argname]
            else:
                # use a single dash for 1-letter names
                prefix = '-' if (len(fld.name) == 1) else '--'
                args = [prefix + argname]
        if args and (not positional):
            # store the argument based on the name of the field, and not whatever flag name was provided
            kwargs['dest'] = fld.name
        if fld.type is bool:  # use boolean flag instead of an argument
            kwargs['action'] = 'store_true'
            for key in ('type', 'required'):
                with suppress(KeyError):
                    kwargs.pop(key)
        # extract additional items from metadata
        for key in cls.parser_argument_kwarg_names():
            if key in fld.metadata:
                kwargs[key] = fld.metadata[key]
        if (kwargs.get('action') == 'store_const'):
            del kwargs['type']
        parser.add_argument(*args, **kwargs)

    @classmethod
    def configure_parser(cls, parser: ArgumentParser) -> None:
        """Configures an argument parser by adding the appropriate arguments.

        By default, this will simply call [`configure_argument`][fancy_dataclass.cli.ArgparseDataclass.configure_argument] for each dataclass field.

        Args:
            parser: `ArgumentParser` to configure"""
        check_dataclass(cls)
        for fld in fields(cls):  # type: ignore[arg-type]
            cls.configure_argument(parser, fld.name)

    @classmethod
    def make_parser(cls) -> ArgumentParser:
        """Constructs an argument parser and configures it with arguments corresponding to the dataclass's fields.

        Returns:
            The configured `ArgumentParser`"""
        parser = cls.new_parser()
        cls.configure_parser(parser)
        return parser

    @classmethod
    def args_to_dict(cls, args: Namespace) -> Dict[str, Any]:
        """Converts a [`Namespace`](https://docs.python.org/3/library/argparse.html#argparse.Namespace) object to a dict that can be converted to the dataclass type.

        Override this to enable custom behavior.

        Args:
            args: `Namespace` object storing parsed arguments

        Returns:
            A dict mapping from field names to values"""
        check_dataclass(cls)
        d = {}
        for field in fields(cls):  # type: ignore[arg-type]
            nested_field = False
            if issubclass_safe(field.type, ArgparseDataclass):
                # recursively gather arguments for nested ArgparseDataclass
                val = field.type.args_to_dict(args)
                nested_field = True
            elif hasattr(args, field.name):  # extract arg from the namespace
                val = getattr(args, field.name)
            else:  # argument not present
                continue
            if nested_field:  # merge in nested ArgparseDataclass
                d.update(val)
            else:
                d[field.name] = val
        return d

    @classmethod
    def from_args(cls, args: Namespace) -> Self:
        """Constructs an [`ArgparseDataclass`][fancy_dataclass.cli.ArgparseDataclass] from a `Namespace` object.

        Args:
            args: `Namespace` object storing parsed arguments

        Returns:
            An instance of this class derived from the parsed arguments"""
        # do some basic type coercion if necessary
        d = cls.args_to_dict(args)
        for fld in fields(cls):  # type: ignore[arg-type]
            origin = get_origin(fld.type)
            if (origin is tuple) and isinstance(d.get(fld.name), list):
                d[fld.name] = tuple(d[fld.name])
        return cls(**d)

    @classmethod
    def process_args(cls, parser: ArgumentParser, args: Namespace) -> None:
        """Processes arguments from an ArgumentParser, after they are parsed.

        Override this to enable custom behavior.

        Args:
            parser: `ArgumentParser` used to parse arguments
            args: `Namespace` containing parsed arguments"""
        pass

    @classmethod
    def from_cli_args(cls, arg_list: Optional[List[str]] = None) -> Self:
        """Constructs and configures an argument parser, then parses the given command-line arguments and uses them to construct an instance of the class.

        Args:
            arg_list: List of arguments as strings (if `None`, uses `sys.argv`)

        Returns:
            An instance of this class derived from the parsed arguments"""
        parser = cls.make_parser()  # create and configure parser
        args = parser.parse_args(args = arg_list)  # parse arguments (uses sys.argv if None)
        cls.process_args(parser, args)  # process arguments
        return cls.from_args(args)


class CLIDataclass(ABC, ArgparseDataclass):
    """This subclass of [`ArgparseDataclass`][fancy_dataclass.cli.ArgparseDataclass] allows the user to execute arbitrary program logic using the parsed arguments as input.

    Subclasses should override the `run` method to implement custom behavior."""

    @abstractmethod
    def run(self) -> None:
        """Runs the main body of the program.

        Subclasses must implement this to provide custom behavior."""

    @classmethod
    def main(cls, arg_list: Optional[List[str]] = None) -> None:
        """Executes the following procedures in sequence:

        1. Constructs a new argument parser.
        2. Configures the parser with appropriate arguments.
        3. Parses command-line arguments.
        4. Post-processes the arguments.
        5. Constructs a dataclass instance from the parsed arguments.
        6. Runs the main body of the program, using the parsed arguments.

        Args:
            arg_list: List of arguments as strings (if `None`, uses `sys.argv`)"""
        obj = cls.from_cli_args(arg_list)  # steps 1-5
        obj.run()  # step 6
