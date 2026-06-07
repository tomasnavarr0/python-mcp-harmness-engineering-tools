import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from tools.utils import SafeSubprocessExecutor
from tools.code_quality import CodeQualityTool
from tools.data_models import CodeQualityRequest

from tools.code_quality.linters.ruff import RuffLinter
from tools.code_quality.linters.pymetrica import PymetricaAnalyzer

mcp = FastMCP("harmness-tools")

executor = SafeSubprocessExecutor()

# 1. Instanciamos los orquestadores por separado
ruff_orchestrator = CodeQualityTool(linters=[RuffLinter()], executor=executor)
pymetrica_orchestrator = CodeQualityTool(
    linters=[PymetricaAnalyzer()], executor=executor
)


@mcp.tool()
def fix_and_lint_code() -> str:
    """
    Ejecuta Ruff para analizar (linter) y formatear (formatter) todo el código del repositorio.
    Busca y corrige automáticamente errores de sintaxis, imports no usados y violaciones de estilo.
    Úsalo SIEMPRE después de escribir o modificar código para asegurar que cumple con los estándares.
    """
    # Para Ruff forzamos la ruta "." (todo el proyecto) y auto_fix=True
    request = CodeQualityRequest(target_path=Path("."), auto_fix=True)

    results = ruff_orchestrator.execute_tool(request)

    return json.dumps(results, indent=2, ensure_ascii=False)


@mcp.tool()
def analyze_architecture_metrics(target_path: str) -> str:
    """
    Ejecuta Pymetrica para analizar métricas avanzadas de arquitectura y complejidad.
    Evalúa la Complejidad Ciclomática (CC) y el Costo de Mantenibilidad (MC).
    Úsalo para auditar si el código es demasiado complejo y necesita ser refactorizado.

    Args:
        target_path: El directorio o archivo a analizar (usa "." para escanear todo el proyecto).
    """
    # Para Pymetrica respetamos el path que elija el agente y no hay auto_fix posible
    request = CodeQualityRequest(target_path=Path(target_path), auto_fix=False)

    results = pymetrica_orchestrator.execute_tool(request)

    return json.dumps(results, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
