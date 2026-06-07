import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from tools.utils import SafeSubprocessExecutor
from tools.code_quality import RuffLinter, CodeQualityTool
from tools.data_models import CodeQualityRequest

mcp = FastMCP("harmness-tools")


executor = SafeSubprocessExecutor()
linters = [RuffLinter()]
qa_tool = CodeQualityTool(linters=linters, executor=executor)


@mcp.tool()
def analyze_code_quality(target_path: str, auto_fix: bool = False) -> str:

    request = CodeQualityRequest(target_path=Path(target_path), auto_fix=auto_fix)

    results = qa_tool.execute_tool(request)

    return json.dumps(results, indent=2, ensure_ascii=False)



if __name__ == "__main__":
    mcp.run(transport="stdio")