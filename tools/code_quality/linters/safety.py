import re
import sys
from pathlib import Path
from tools.utils import CommandExecutor
from tools.data_models import CodeQualityRequest, CodeQualityResponse


class SafetyAnalyzer:
    """Estrategia concreta para auditar vulnerabilidades conocidas en las dependencias con Safety."""

    @property
    def name(self) -> str:
        return "safety"

    def _get_binary(self) -> list[str]:
        venv_bin = Path(sys.executable).parent / "safety.exe"
        if venv_bin.exists():
            return [str(venv_bin)]
        return [sys.executable, "-m", "safety"]

    def _clean_output(self, text: str) -> str:
        """Elimina códigos de color ANSI y banners de deprecación molestos."""
        if not text:
            return ""
        
        # 1. Limpiar códigos de escape ANSI (\u001b[...)
        ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
        clean_text = ansi_escape.sub('', text)
        
        # 2. Filtrar líneas del aviso de deprecación para que el agente no se confunda
        lines = clean_text.splitlines()
        filtered_lines = []
        skip_keywords = ["DEPRECATED", "switching to the new", "unsupported beyond", "+===="]
        
        for line in lines:
            if any(kw in line for kw in skip_keywords):
                continue
            filtered_lines.append(line)
            
        return "\n".join(filtered_lines).strip()

    def is_installed(self, executor: CommandExecutor) -> bool:
        code, _, _ = executor.execute(self._get_binary() + ["--help"])
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

        # Volvemos a 'check' porque permite escaneos anónimos con la DB pública
        command = self._get_binary() + ["check"]

        target = Path(request.target_path)
        if target.is_file() and target.name in ["requirements.txt", "requirements-dev.txt"]:
            command += ["--file", str(target)]

        code, stdout, stderr = executor.execute(command)

        # Safety check retorna 0 si no hay vulnerabilidades
        is_success = code == 0
        
        # Saneamos el output sucio que manda Safety antes de dárselo al agente
        raw_output = stdout.strip() if stdout.strip() else stderr.strip()
        final_output = self._get_binary_output_clean = self._clean_output(raw_output)

        return CodeQualityResponse(
            success=is_success,
            output=final_output or "✅ Safety no detectó vulnerabilidades conocidas en tus dependencias.",
            missing_dependencies=[],
        )