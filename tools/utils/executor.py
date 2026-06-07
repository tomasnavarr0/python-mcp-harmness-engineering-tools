from pathlib import Path
from typing import Protocol


class CommandExecutor(Protocol):
    def execute(self, command: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
        ...
