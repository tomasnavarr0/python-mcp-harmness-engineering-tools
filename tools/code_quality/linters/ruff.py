from tools.utils import CommandExecutor
from tools.data_models import CodeQualityRequest, CodeQualityResponse


class RuffLinter:
    @property
    def name(self) -> str:
        return "ruff"

    def is_installed(self, executor: CommandExecutor) -> bool:
        code, _, _ = executor.execute(["ruff", "--version"])
        return code == 0

    def run(self, request: CodeQualityRequest, executor: CommandExecutor) -> CodeQualityResponse:
        if not self.is_installed(executor):
            return CodeQualityResponse(
                success=False,
                output=f"CRITICAL: '{self.name}' no está instalado. Ejecuta: 'uv pip install {self.name}'.",
                missing_dependencies=[self.name]
            )
        
        command = ["ruff", "check", str(request.target_path)]
        if request.auto_fix:
            command.append("--fix")

        code, stdout, stderr = executor.execute(command)
        is_success = (code == 0)
        final_output = stdout.strip() if stdout.strip() else stderr.strip()

        return CodeQualityResponse(
            success=is_success,
            output=final_output or "✅ Ruff completó los checks exitosamente.",
            missing_dependencies=[]
        )

