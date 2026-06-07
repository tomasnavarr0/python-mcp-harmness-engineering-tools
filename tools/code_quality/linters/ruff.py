import sys
from pathlib import Path
from tools.utils import CommandExecutor
from tools.data_models import CodeQualityRequest, CodeQualityResponse

class RuffLinter:
    @property
    def name(self) -> str:
        return "ruff"

    def _get_binary(self) -> list[str]:
        # Buscamos ruff.exe en la misma carpeta de Scripts donde corre este MCP
        venv_bin = Path(sys.executable).parent / "ruff.exe"
        if venv_bin.exists():
            return [str(venv_bin)]
        # Fallback seguro usando el módulo de python
        return [sys.executable, "-m", "ruff"]

    def is_installed(self, executor: CommandExecutor) -> bool:
        code, _, _ = executor.execute(self._get_binary() + ["--version"])
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

        target = "."
        binary = self._get_binary()

        # Armamos los comandos usando el binario directo del venv
        check_command = binary + ["check", target]
        format_command = binary + ["format", target]

        if request.auto_fix:
            check_command.append("--fix")
        else:
            format_command.append("--check")

        # Ejecución
        check_code, check_stdout, check_stderr = executor.execute(check_command)
        check_output = check_stdout.strip() if check_stdout.strip() else check_stderr.strip()

        format_code, format_stdout, format_stderr = executor.execute(format_command)
        format_output = format_stdout.strip() if format_stdout.strip() else format_stderr.strip()

        is_success = (check_code == 0) and (format_code == 0)

        combined_output = []
        if check_output:
            combined_output.append(f"--- Linter (Check) ---\n{check_output}")
        if format_output:
            combined_output.append(f"--- Formatter ---\n{format_output}")

        return CodeQualityResponse(
            success=is_success,
            output= "\n\n".join(combined_output) or "✅ Ruff completó con éxito.",
            missing_dependencies=[],
        )