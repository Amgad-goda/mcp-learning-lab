import os 
import sys
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
# connect u to any server 

from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

mcp_server_script = (
    project_root
    / "CreatMCP"
    / "first_mcpserver_stdio.py"
)

#mcp_server_script =os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "CreatMCP","first_mcpserver_stdio.py")
# ven_path = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".venv")


async def main():
    client = MultiServerMCPClient(

    # ser conf json
    {
        "data_fetch_stdio":{
            "transport": "stdio",
            "command": sys.executable, # os.path.join(ven_path, "Scripts", "python.exe"),
            "args": [str(mcp_server_script)]
        },
        "data_fetch_http":{
                    "transport": "streamable_http",
                    "url": "http://localhost:8050/mcp"
                    
                }
    }
    )

    # list the tools 
    tools = await client.get_tools()
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(main())
        