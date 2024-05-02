from click.testing import Result
from typer import Typer
from typer.testing import CliRunner


def invoke(app: Typer, args: str, **kwargs) -> Result:
    runner = CliRunner()
    return runner.invoke(app, args, **kwargs)
