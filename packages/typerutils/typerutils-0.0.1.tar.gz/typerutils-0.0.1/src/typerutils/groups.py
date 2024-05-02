from typing import List
from typer.core import TyperGroup


class NaturalOrderGroup(TyperGroup):
    def list_commands(self, ctx) -> List[str]:
        return list(self.commands.keys())
