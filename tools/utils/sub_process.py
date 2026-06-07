from pathlib import Path
import subprocess


class SafeSubprocessExecutor:
    def execute(self, command: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
        try:
            result = subprocess.run(
                command, cwd=cwd, capture_output=True, text=True, check=False
            )
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            return -1, "", "Executable not found"