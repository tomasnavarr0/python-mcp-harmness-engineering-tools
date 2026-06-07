import sys
from pathlib import Path
from tools.utils import CommandExecutor
from tools.data_models import CodeQualityRequest, CodeQualityResponse

class PymetricaAnalyzer:
    @property
    def name(self) -> str:
        return "pymetrica"

    def _get_binary(self) -> list[str]:
        venv_bin = Path(sys.executable).parent / "pymetrica.exe"
        if venv_bin.exists():
            return [str(venv_bin)]
        return [sys.executable, "-m", "pymetrica"]

    def is_installed(self, executor: CommandExecutor) -> bool:
        code, _, _ = executor.execute(self._get_binary() + ["--help"])
        return code == 0

    def run(
        self, request: CodeQualityRequest, executor: CommandExecutor
    ) -> CodeQualityResponse:
        if not self.is_installed(executor):
            return CodeQualityResponse(
                success=False,
                output=f"CRITICAL: '{self.name}' no está instalado en el .venv.",
                missing_dependencies=[self.name],
            )

        command = self._get_binary() + [
            "run-all",
            str(request.target_path),
            "--long-report",
        ]

        code, stdout, stderr = executor.execute(command)
        is_success = code == 0
        final_output = stdout.strip() if stdout.strip() else stderr.strip()

        return CodeQualityResponse(
            success=is_success,
            output=final_output or "✅ Pymetrica analizó las métricas exitosamente.",
            missing_dependencies=[],
        )