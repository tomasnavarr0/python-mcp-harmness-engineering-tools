from tools.utils import CommandExecutor
from tools.data_models import CodeQualityRequest, CodeQualityResponse


class PymetricaAnalyzer:
    """Estrategia concreta para analizar métricas de arquitectura con Pymetrica."""

    @property
    def name(self) -> str:
        return "pymetrica"

    def is_installed(self, executor: CommandExecutor) -> bool:
        # Verificamos si la CLI de pymetrica responde
        code, _, _ = executor.execute(["pymetrica", "--help"])
        return code == 0

    def run(
        self, request: CodeQualityRequest, executor: CommandExecutor
    ) -> CodeQualityResponse:
        if not self.is_installed(executor):
            return CodeQualityResponse(
                success=False,
                output=(
                    f"CRITICAL: '{self.name}' no está instalado. "
                    f"Ejecuta: 'uv pip install {self.name}'."
                ),
                missing_dependencies=[self.name],
            )

        # Pymetrica usa el subcomando run-all para correr todas las métricas.
        # Le pasamos --long-report para que el agente obtenga todo el contexto.
        command = ["pymetrica", "run-all", str(request.target_path), "--long-report"]

        code, stdout, stderr = executor.execute(command)

        # Si el código de retorno es 0, todo salió bien
        is_success = code == 0
        final_output = stdout.strip() if stdout.strip() else stderr.strip()

        return CodeQualityResponse(
            success=is_success,
            output=final_output or "✅ Pymetrica analizó las métricas exitosamente.",
            missing_dependencies=[],
        )
