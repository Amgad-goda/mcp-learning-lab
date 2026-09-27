from fastmcp import FastMCP
from fastmcp.server import create_proxy

mcp = FastMCP("MCP Practice Gateway")


@mcp.tool()
async def fetch() -> dict:
    """Return sample data for testing the gateway."""
    return {"data": "Hello MCP"}


@mcp.tool()
async def process(path: str) -> dict:
    """Return a sample processing result for a path."""
    return {"processed_data": f"Data has been processed at path: {path}"}


ddg_config = {
    "mcpServers": {
        "default": {
            "command": "uvx",
            "args": ["duckduckgo-mcp-server"],
        }
    }
}

terminal_config = {
    "mcpServers": {
        "default": {
            "command": "uvx",
            "args": ["mcp_agentic_terminal"],
        }
    }
}

mcp.mount(create_proxy(ddg_config), namespace="ddg")
mcp.mount(create_proxy(terminal_config), namespace="terminal")


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8040)