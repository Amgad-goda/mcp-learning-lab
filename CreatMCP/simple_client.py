import os 
import sys
import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters, client



# path to the mcp server script 
mcp_server_script = os.path.join((os.path.dirname(os.path.abspath(__file__))), "first_mcpserver_stdio.py") 
print("____Path is HERE___:",mcp_server_script)



# creat server parameters
server_params = StdioServerParameters(
    command= sys.executable, # "python",
    args=[str(mcp_server_script)]
    
)



# Create a Client Session 
async def main():
    
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()
            # fetch the tools 
            tools = await session.list_tools() 
            print("___Available tools___:", tools)      

            result = await session.call_tool("process", arguments={"path": "/path/to/data"})
            print("___Result:___", result)

if __name__ == "__main__":
    asyncio.run(main())            