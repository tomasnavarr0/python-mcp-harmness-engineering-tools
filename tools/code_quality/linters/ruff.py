from tools.utils import CommandExecutor
from tools.data_models import CodeQualityRequest, CodeQualityResponse


class RuffLinter:
    @property
    def name(self) -> str:
        return "ruff"

    def is_installed(self, executor: CommandExecutor) -> bool:
        code, _, _ = executor.execute(["ruff", "--version"])
        return code == 0

    def run(
        self, request: CodeQualityRequest, executor: CommandExecutor
    ) -> CodeQualityResponse:
        if not self.is_installed(executor):
            return CodeQualityResponse(
                success=False,
                output=f"CRITICAL: '{self.name}' no está instalado. Ejecuta: 'uv pip install {self.name}'.",
                missing_dependencies=[self.name],
            )

        # POLÍTICA DE SEGURIDAD (Harmness Engineering):
        # Forzamos el análisis de todo el proyecto apuntando a la raíz (".").
        # Evitamos que el agente oculte errores al escanear solo un archivo modificado.
        target = "."

        # 1. Preparamos comandos para Linter (check) y Formatter (format) globales
        check_command = ["ruff", "check", target]
        format_command = ["ruff", "format", target]

        if request.auto_fix:
            check_command.append("--fix")
        else:
            # Si no hay auto_fix, le decimos al formatter que solo revise sin modificar
            format_command.append("--check")

        # 2. Ejecutar Linter en todo el proyecto
        check_code, check_stdout, check_stderr = executor.execute(check_command)
        check_output = (
            check_stdout.strip() if check_stdout.strip() else check_stderr.strip()
        )

        # 3. Ejecutar Formatter en todo el proyecto
        format_code, format_stdout, format_stderr = executor.execute(format_command)
        format_output = (
            format_stdout.strip() if format_stdout.strip() else format_stderr.strip()
        )

        # 4. Consolidar resultados globales
        is_success = (check_code == 0) and (format_code == 0)

        combined_output = []
        if check_output:
            combined_output.append(f"--- Linter (Check) ---\n{check_output}")
        if format_output:
            combined_output.append(f"--- Formatter ---\n{format_output}")

        final_output = "\n\n".join(combined_output)

        return CodeQualityResponse(
            success=is_success,
            output=final_output
            or "✅ Ruff completó el linter y el formato en todo el proyecto exitosamente.",
            missing_dependencies=[],
        )
