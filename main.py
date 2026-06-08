import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from tools.utils import SafeSubprocessExecutor
from tools.code_quality import CodeQualityTool
from tools.data_models import CodeQualityRequest

from tools.code_quality.linters.ruff import RuffLinter
from tools.code_quality.linters.pymetrica import PymetricaAnalyzer
from tools.code_quality.linters.bandit import BanditAnalyzer
from tools.code_quality.linters.mypy import MypyAnalyzer
from tools.code_quality.linters.safety import SafetyAnalyzer

mcp = FastMCP("harmness-tools")

executor = SafeSubprocessExecutor()

# 1. Instanciamos los orquestadores por separado
ruff_orchestrator = CodeQualityTool(
    linters=[RuffLinter()], executor=executor
)
pymetrica_orchestrator = CodeQualityTool(
    linters=[PymetricaAnalyzer()], executor=executor
)
bandit_orchestrator = CodeQualityTool(
    linters=[BanditAnalyzer()], executor=executor
)
mypy_orchestrator = CodeQualityTool(
    linters=[MypyAnalyzer()], executor=executor
)
safety_orchestrator = CodeQualityTool(
    linters=[SafetyAnalyzer()], executor=executor
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
    Ejecuta Pymetrica para analizar métricas avanzadas de arquitectura y complejidad en una carpeta específica.
    Evalúa la Complejidad Ciclomática (CC) y el Costo de Mantenibilidad (MC).
    
    IMPORTANTE: NO uses "." como target_path ya que causará un error con los archivos binarios del entorno virtual.
    Debes especificar la carpeta concreta del código fuente (por ejemplo: "tools").

    Args:
        target_path: El directorio específico a analizar (ej. "tools"). No usar ".".
    """
    request = CodeQualityRequest(target_path=Path(target_path), auto_fix=False)
    results = pymetrica_orchestrator.execute_tool(request)
    return json.dumps(results, indent=2, ensure_ascii=False)


@mcp.tool()
def audit_code_security(target_path: str) -> str:
    """
    Ejecuta Bandit para realizar un análisis de seguridad AST (Abstract Syntax Tree) en el código.
    Detecta fallos críticos comunes como inyecciones SQL, strings de conexión hardcodeados, 
    uso de funciones inseguras (eval, exec), contraseñas por defecto y criptografía débil.

    Args:
        target_path: El directorio o archivo a auditar.
    """
    # Bandit es puramente informativo/auditoría, no posee auto_fix automático seguro.
    request = CodeQualityRequest(target_path=Path(target_path), auto_fix=False)

    results = bandit_orchestrator.execute_tool(request)

    return json.dumps(results, indent=2, ensure_ascii=False)


@mcp.tool()
def check_type_hints(target_path: str) -> str:
    """
    Ejecuta Mypy para validar estáticamente el tipado (Type Hints) en el código Python.
    Detecta inconsistencias de tipos asignados, firmas de funciones incompatibles, 
    retornos erróneos y previene TypeErrors antes de ejecutar el código.

    Args:
        target_path: El directorio o archivo a chequear (usa "." para escanear todo el proyecto).
    """
    # Mypy es puramente un validador de tipado, no realiza auto-correcciones directas en el archivo.
    request = CodeQualityRequest(target_path=Path(target_path), auto_fix=False)

    results = mypy_orchestrator.execute_tool(request)

    return json.dumps(results, indent=2, ensure_ascii=False)


@mcp.tool()
def audit_dependencies_vulnerabilities(target_path: str) -> str:
    """
    Ejecuta Safety para escanear las dependencias del proyecto contra bases de datos de vulnerabilidades conocidas (CVEs).
    Úsalo para verificar que librerías de terceros (como Django, Flask, Requests, etc.) no tengan fallos de seguridad.

    Args:
        target_path: Directorio raíz del proyecto o ruta a un archivo 'requirements.txt' específico.
    """
    # Safety solo reporta vulnerabilidades, no realiza modificaciones automáticas.
    request = CodeQualityRequest(target_path=Path(target_path), auto_fix=False)

    results = safety_orchestrator.execute_tool(request)

    return json.dumps(results, indent=2, ensure_ascii=False)



if __name__ == "__main__":
    mcp.run(transport="stdio")
