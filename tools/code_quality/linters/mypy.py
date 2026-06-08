import sys
from pathlib import Path
from tools.utils import CommandExecutor
from tools.data_models import CodeQualityRequest, CodeQualityResponse


class MypyAnalyzer:
    """Estrategia concreta para realizar análisis estático de tipos con Mypy."""

    @property
    def name(self) -> str:
        return "mypy"

    def _get_binary(self) -> list[str]:
        # Localizamos el binario directamente en el .venv del servidor MCP
        venv_bin = Path(sys.executable).parent / "mypy.exe"
        if venv_bin.exists():
            return [str(venv_bin)]
        return [sys.executable, "-m", "mypy"]

    def is_installed(self, executor: CommandExecutor) -> bool:
        # Verificamos si responde correctamente
        code, _, _ = executor.execute(self._get_binary() + ["--version"])
        return code == 0

    def run(
        self, request: CodeQualityRequest, executor: CommandExecutor
    ) -> CodeQualityResponse:
        if not self.is_installed(executor):
            return CodeQualityResponse(
                success=False,
                output=(
                    f"CRITICAL: '{self.name}' no está instalado en el .venv. "
                    f"Ejecuta: 'uv pip install {self.name}'."
                ),
                missing_dependencies=[self.name],
            )

        # Comando base para Mypy apuntando al path objetivo
        command = self._get_binary() + [
            str(request.target_path),
        ]

        code, stdout, stderr = executor.execute(command)

        # Mypy retorna:
        # 0 = Éxito total, tipos consistentes
        # >0 = Se encontraron errores de tipado
        is_success = code == 0
        final_output = stdout.strip() if stdout.strip() else stderr.strip()

        return CodeQualityResponse(
            success=is_success,
            output=final_output or "✅ Mypy completó el chequeo: no se encontraron errores de tipo.",
            missing_dependencies=[],
        )