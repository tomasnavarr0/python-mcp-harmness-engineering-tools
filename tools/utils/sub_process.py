from pathlib import Path
import subprocess


class SafeSubprocessExecutor:
    def execute(
        self, command: list[str], cwd: Path | None = None
    ) -> tuple[int, str, str]:
        try:
            result = subprocess.run(  # nosec B603
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False,
                stdin=subprocess.DEVNULL,
            )
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            return -1, "", "Executable not found"
