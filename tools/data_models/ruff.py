from pathlib import Path
from pydantic import BaseModel, Field


class CodeQualityRequest(BaseModel):
    target_path: Path = Field(description="Directorio o archivo a analizar (ej: '.', 'src/main.py')")
    auto_fix: bool = Field(default=True, description="Si es True, intenta arreglar los errores automáticamente")


class CodeQualityResponse(BaseModel):
    success: bool
    output: str
    missing_dependencies: list[str] = Field(default_factory=list)