from typing import Protocol
from tools.data_models import CodeQualityRequest, CodeQualityResponse
from tools.utils import CommandExecutor


class LinterStrategy(Protocol):
    @property
    def name(self) -> str: ...

    def is_installed(self, executor: CommandExecutor) -> bool: ...

    def run(
        self, request: CodeQualityRequest, executor: CommandExecutor
    ) -> CodeQualityResponse: ...
