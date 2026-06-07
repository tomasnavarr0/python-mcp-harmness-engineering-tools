from collections.abc import Sequence

from .linters import LinterStrategy
from tools.data_models import CodeQualityRequest
from tools.utils import CommandExecutor


class CodeQualityTool:
    def __init__(self, linters: Sequence[LinterStrategy], executor: CommandExecutor):
        self._linters = linters
        self._executor = executor

    def execute_tool(self, request: CodeQualityRequest) -> dict[str, dict]:
        results = {}
        for linter in self._linters:
            response = linter.run(request, self._executor)
            results[linter.name] = response.model_dump()
        return results
