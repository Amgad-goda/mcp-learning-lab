from fastmcp import FastMCP

mcp = FastMCP()


"""Local tools for an agentic terminal.

These functions can be registered as MCP tools by an MCP server.
They run with the same filesystem permissions as the server process.
"""

import subprocess
import sys
from pathlib import Path


TIMEOUT = 30
MAX_OUTPUT = 12_000

def _run(command: str | list[str], *, shell: bool = False) -> str:
    """Run a command and return its exit code, stdout, and stderr."""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"Command timed out after {TIMEOUT} seconds."
    except OSError as exc:
        return f"Could not start command: {exc}"

    output = result.stdout + result.stderr
    if len(output) > MAX_OUTPUT:
        output = output[:MAX_OUTPUT] + "\n... output truncated"
    return f"Exit code: {result.returncode}\n{output or '(no output)'}"

@mcp.tool()
def bash(command: str) -> str:
    """Run a shell command and return its output. Use only for trusted requests."""
    return _run(command, shell=True)

@mcp.tool()
def python_code(code: str) -> str:
    """Run Python code in a separate process and return its output."""
    return _run([sys.executable, "-c", code])

@mcp.tool()
def python_file(file: str) -> str:
    """Run a Python file in a separate process and return its output."""
    path = Path(file).expanduser()
    if not path.is_file():
        return f"File not found: {path}"
    return _run([sys.executable, str(path)])

@mcp.tool()
def read_file(file: str) -> str:
    """Read a UTF-8 text file."""
    try:
        content = Path(file).expanduser().read_text(encoding="utf-8")
        if len(content) > MAX_OUTPUT:
            return content[:MAX_OUTPUT] + "\n... file truncated"
        return content
    except (OSError, UnicodeError) as exc:
        return f"Could not read file: {exc}"

@mcp.tool()
def write_file(file: str, content: str) -> str:
    """Create or overwrite a UTF-8 text file, creating parent folders if needed."""
    try:
        path = Path(file).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Wrote {path} ({len(content)} characters)."
    except OSError as exc:
        return f"Could not write file: {exc}"

@mcp.tool()
def list_directory(directory: str = ".") -> str:
    """List files and folders in a directory."""
    try:
        path = Path(directory).expanduser()
        items = sorted(path.iterdir(), key=lambda item: item.name.lower())
        lines = [f"{'DIR ' if item.is_dir() else 'FILE'} {item.name}" for item in items]
        return "\n".join(lines)[:MAX_OUTPUT] or "(empty directory)"
    except OSError as exc:
        return f"Could not list directory: {exc}"

@mcp.tool()
def current_directory() -> str:
    """Return the current working directory used by these tools."""
    return str(Path.cwd())
