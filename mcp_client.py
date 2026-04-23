import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import sys

async def call_tool_async(tool_name, args):
    server = StdioServerParameters(
        command = sys.executable,
        args=["mcp_server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(tool_name, args)

            if result.content:
                return result.content[0].text

            return "No result from tool."


def call_tool_sync(tool_name, args):
    try:
        # ✅ Safe execution (handles Streamlit loop)
        return asyncio.run(call_tool_async(tool_name, args))
    except RuntimeError:
        # 🔁 Fallback if loop already running
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(call_tool_async(tool_name, args))
    except Exception as e:
        return f"MCP Error: {str(e)}"
