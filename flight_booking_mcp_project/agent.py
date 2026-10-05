# agent.py
import asyncio
import json
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import ollama

SYSTEM_PROMPT = """You are a helpful flight booking assistant with access to tools.

CRITICAL RULES:
1. When asked to find and save a flight, always call `find_flights` first.
2. When calling `save_flight_to_db`, NEVER invent or hallucinate flight details, airlines, or prices.
3. You MUST ONLY use the EXACT data (airline, price, duration_minutes, stops, date, origin, destination) returned by the `find_flights` tool.
4. If no flight is found, inform the user and do not save anything.
"""


async def main():
    python_executable = sys.executable
    #server_script = os.path.abspath("server.py")
    server_script = os.path.abspath("test_server.py")

    server_params = StdioServerParameters(
        command=python_executable,
        args=[server_script],
        env=os.environ.copy(),
    )

    print("🔌 Connecting to MCP Flight Server...")

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Discover tools from MCP server
            tools_response = await session.list_tools()
            available_tools = []
            for tool in tools_response.tools:
                available_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.input_schema,
                    },
                })

            print(f"✅ Discovered {len(available_tools)} tools from MCP server.")
            print("\n" + "=" * 50)
            print("🛫 Flight Assistant Ready! Type 'exit' or 'quit' to stop.")
            print("=" * 50 + "\n")

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            while True:
                try:
                    user_input = input("👤 You: ").strip()
                except (KeyboardInterrupt, EOFError):
                    print("\nGoodbye!")
                    break

                if not user_input:
                    continue
                if user_input.lower() in ("exit", "quit", "q"):
                    print("Goodbye!")
                    break

                messages.append({"role": "user", "content": user_input})

                # Agent reasoning loop (max 5 tool turns per question)
                max_turns = 5
                for turn in range(max_turns):
                    response = ollama.chat(
                        model="qwen2.5:3b",
                        messages=messages,
                        tools=available_tools,
                    )

                    messages.append(response.message)

                    if not response.message.tool_calls:
                        print(f"\n🤖 Ollama: {response.message.content}\n")
                        break

                    for tool_call in response.message.tool_calls:
                        fn_name = tool_call.function.name
                        fn_args = tool_call.function.arguments

                        print(f"\n⚡ Calling tool: {fn_name}")
                        print(f"📦 Arguments: {json.dumps(fn_args, indent=2)}")

                        result = await session.call_tool(fn_name, arguments=fn_args)
                        tool_output = (
                            result.content[0].text
                            if result.content
                            else "No response"
                        )

                        messages.append({
                            "role": "tool",
                            "name": fn_name,
                            "content": tool_output,
                        })


if __name__ == "__main__":
    asyncio.run(main())