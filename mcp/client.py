"""MCP client — connects to langchain-ai-server and invokes tools directly."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = Path(__file__).resolve().parent / "server.py"


async def list_server_capabilities(session: ClientSession) -> None:
    """Print tools, resources, and prompts exposed by the MCP server."""
    tools = await session.list_tools()
    resources = await session.list_resources()
    prompts = await session.list_prompts()

    print("Tools:", [tool.name for tool in tools.tools])
    print("Resources:", [resource.uri for resource in resources.resources])
    print("Prompts:", [prompt.name for prompt in prompts.prompts])


async def call_example_tools(session: ClientSession) -> None:
    """Demonstrate calling a few MCP tools."""
    chain_result = await session.call_tool("run_chain", {"topic": "CSK"})
    print("\nrun_chain result:")
    print(chain_result.content[0].text)

    prompt_result = await session.call_tool(
        "generate_prompt",
        {
            "paper_input": "Attention Is All You Need",
            "style_input": "technical",
            "length_input": "short",
        },
    )
    print("\ngenerate_prompt result:")
    print(prompt_result.content[0].text[:300], "...")


async def main() -> None:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        cwd=str(SERVER_PATH.parent.parent),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to langchain-ai-server\n")
            await list_server_capabilities(session)
            await call_example_tools(session)


if __name__ == "__main__":
    asyncio.run(main())
