import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    client = MultiServerMCPClient(
    {
        "data_fetch_stdio":{
            "transport": "stdio",
            "command": "uvx", 
            "args": ["duckduckgo-mcp-server"]
        }
    }
    )

    # list the tools 
    tools = await client.get_tools()
    print("________Tools________")
    
    for tool in tools: 
        print(f"-{tool.name}" )
    
    fetch_tool = tools[0]
    result = await fetch_tool.ainvoke({"query": "what is the date today"})
    
    print("__________Rsult__________", result)

if __name__ == "__main__":
    asyncio.run(main())
        