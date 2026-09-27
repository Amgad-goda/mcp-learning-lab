import asyncio
import os

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise RuntimeError("TAVILY_API_KEY is missing")

async def main():
    client = MultiServerMCPClient(
        {
            "tavily_mcp_http":{
                    "transport": "streamable_http",
                    "url": "https://mcp.tavily.com/mcp/",
                    "headers":{
                        "Authorization": f"Bearer {api_key}"
                }, 
            }
        }
    )

    # list the tools 
    tools = await client.get_tools()

    print("_____________________Tools_____________________")
    print("Number of tools:",len(tools))

    for tool in tools:
        print(f"- {tool.name}")

    tool_search = [tool for tool in tools if tool.name == "tavily_search"][0]
    result = await tool_search.ainvoke({"query": "what is the date of today"})
    print("Tool Result:", result)

    
if __name__ == "__main__":
    asyncio.run(main())
        