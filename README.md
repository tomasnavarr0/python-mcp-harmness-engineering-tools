# Python MCP Harmness Engineering Tools

This project is an MCP (Model Context Protocol) server based on `FastMCP` that provides tools to improve code quality, security, and architecture in Python projects.

## 🛠️ Available Tools

The server exposes the following tools to be used by your code agent:

1. **`fix_and_lint_code`**: Runs Ruff to analyze (linter) and format (formatter) all the repository's code. It automatically finds and fixes syntax errors, unused imports, and style violations.
2. **`analyze_architecture_metrics`**: Runs Pymetrica to analyze advanced architecture and complexity metrics (Cyclomatic Complexity and Maintainability Cost) in a specific folder.
3. **`audit_code_security`**: Runs Bandit to perform an AST security analysis on the code. Detects common critical flaws such as SQL injections, hardcoded credentials, use of insecure functions, etc.
4. **`check_type_hints`**: Runs Mypy to statically validate Type Hints. Detects type inconsistencies and prevents `TypeErrors`.
5. **`audit_dependencies_vulnerabilities`**: Runs Safety to scan project dependencies against known vulnerability databases (CVEs).

## 🚀 Installation on Code Agents

To install and use this MCP server in agents (Codex, Cursor, Antigravity IDE, Claude Code) via `stdio`, you must add the corresponding configuration pointing to the `main.py` file of this project.

Make sure you have the dependencies installed in your environment (Ruff, Mypy, Bandit, Safety, FastMCP, etc.) or use a package manager like `uv`.

### Claude Code / Antigravity IDE
Add the following to your MCP configuration file (usually `mcp.json` or from the UI settings):

```json
{
  "mcpServers": {
    "harmness_tools": {
      "command": "python",
      "args": [
        "C:\\Users\\tomas\\Desktop\\projects\\python-mcp-harmness-engineering-tools\\main.py"
      ]
    }
  }
}
```
*(Note: If you use `uv`, the command would be `uv` and the arguments `["run", "main.py"]`)*

### Cursor / Codex
1. Go to **Settings** -> **Features** -> **MCP**.
2. Add a new server:
   - **Name**: `harmness_tools`
   - **Type**: `command`
   - **Command**: `python C:\Users\tomas\Desktop\projects\python-mcp-harmness-engineering-tools\main.py`

## 🐛 How to Debug

Because the MCP protocol via `stdio` uses standard output (`stdout`) for communication between the client and the server, **you cannot use a regular `print()` to debug**, as it will corrupt the JSON-RPC protocol.

To debug this server:

1. **MCP Inspector (Recommended)**:
   You can test and debug the tools in an isolated and interactive way using the official MCP inspector:
   ```bash
   npx @modelcontextprotocol/inspector python main.py
   ```
   This will start a local server and open a web interface where you can execute each tool and see exactly the requests and responses your FastMCP server generates.
