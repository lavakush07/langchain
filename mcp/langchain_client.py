"""LangChain MCP client — uses langchain-mcp-adapters to drive an agent with MCP tools."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SERVER_PATH = Path(__file__).resolve().parent / "server.py"


async def main() -> None:
    client = MultiServerMCPClient(
        {
            "langchain-ai-server": {
                "transport": "stdio",
                "command": sys.executable,
                "args": [str(SERVER_PATH)],
                "cwd": str(PROJECT_ROOT),
            }
        }
    )

    tools = await client.get_tools()
    print("Loaded MCP tools:", [tool.name for tool in tools])

    agent = create_agent("openai:gpt-4o-mini", tools)
    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Use the run_chain tool to list five players from team CSK, "
                        "then summarize the result in one sentence."
                    ),
                }
            ]
        }
    )
    print("\nAgent response:")
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
