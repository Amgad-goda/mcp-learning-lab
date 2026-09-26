import os 
import sys
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
# connect u to any server 


mcp_server_script = os.path.join((os.path.dirname(os.path.abspath(__file__))), "first_mcpserver_stdio.py") 

# ven_path = os.path.join((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".venv")

async def main():
    client = MultiServerMCPClient(

    # ser conf json
    {
        "data_fetch_stdio":{
            "transport": "stdio",
            "command": sys.executable, # os.path.join(ven_path, "Scripts", "python.exe"),
            "args": [str(mcp_server_script)]
        }
    }
    )

    # list the tools 
    tools = await client.get_tools()
    print("___Available tools___",tools)


if __name__ == "__main__":
    asyncio.run(main())
        