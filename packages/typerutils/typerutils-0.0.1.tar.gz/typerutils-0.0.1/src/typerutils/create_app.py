from typing import Optional, Type

from typer import Typer
from typer.core import TyperGroup

from typerutils.groups import NaturalOrderGroup


def create_app(
    add_completion=False,
    no_args_is_help=True,
    context_settings=dict(help_option_names=["-h", "--help"]),
    cls: Optional[Type[TyperGroup]] = NaturalOrderGroup,
) -> Typer:
    """
    Create a Typer app with sane defaults.

    - add_completion disabled
    - no_args_is_help enabled
    - context_settings with short and long help flags
    - commands display in the natural order they were defined
    """
    return Typer(
        add_completion=add_completion,
        no_args_is_help=no_args_is_help,
        context_settings=context_settings,
        cls=cls,
    )
