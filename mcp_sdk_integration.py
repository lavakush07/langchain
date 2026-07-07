"""
MCP SDK Integration for LangChain

Integrates Model Context Protocol servers with LangChain applications.
"""

import json
import subprocess
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path


class MCPClient:
    """
    Client for interacting with MCP servers.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize MCP client.

        Args:
            config_path: Path to MCP configuration file (default: mcp_config.json)
        """
        if config_path is None:
            config_path = str(Path(__file__).parent / "mcp_config.json")

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.servers = {}
        self.connected_servers = set()

    def list_servers(self) -> List[str]:
        """
        List all configured MCP servers.

        Returns:
            List of server names
        """
        return list(self.config.get("mcpServers", {}).keys())

    def connect_server(self, server_name: str) -> bool:
        """
        Connect to an MCP server.

        Args:
            server_name: Name of the server from config

        Returns:
            True if connection successful
        """
        if server_name not in self.config.get("mcpServers", {}):
            raise ValueError(f"Server {server_name} not found in configuration")

        server_config = self.config["mcpServers"][server_name]

        # Store server configuration
        self.servers[server_name] = {
            "config": server_config,
            "description": server_config.get("description", "")
        }

        self.connected_servers.add(server_name)
        return True

    def disconnect_server(self, server_name: str):
        """
        Disconnect from an MCP server.

        Args:
            server_name: Name of the server to disconnect
        """
        if server_name in self.connected_servers:
            self.connected_servers.remove(server_name)

    def call_tool(self, server_name: str, tool_name: str,
                 arguments: Dict[str, Any]) -> Any:
        """
        Call a tool on an MCP server.

        Args:
            server_name: Name of the server
            tool_name: Name of the tool to call
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        if server_name not in self.connected_servers:
            raise RuntimeError(f"Server {server_name} is not connected")

        # This would integrate with the actual MCP SDK
        # For now, providing the interface structure
        return {
            "result": None,
            "server": server_name,
            "tool": tool_name
        }

    def list_tools(self, server_name: str) -> List[Dict[str, Any]]:
        """
        List available tools on a server.

        Args:
            server_name: Name of the server

        Returns:
            List of tool descriptions
        """
        if server_name not in self.connected_servers:
            raise RuntimeError(f"Server {server_name} is not connected")

        # Interface for MCP SDK integration
        return []

    def get_resources(self, server_name: str) -> List[Dict[str, Any]]:
        """
        Get available resources from a server.

        Args:
            server_name: Name of the server

        Returns:
            List of available resources
        """
        if server_name not in self.connected_servers:
            raise RuntimeError(f"Server {server_name} is not connected")

        # Interface for MCP SDK integration
        return []


class LangChainMCPIntegration:
    """
    Integration layer between LangChain and MCP servers.
    """

    def __init__(self, mcp_client: Optional[MCPClient] = None):
        """
        Initialize LangChain MCP integration.

        Args:
            mcp_client: Optional MCPClient instance
        """
        self.mcp_client = mcp_client or MCPClient()

    def create_langchain_tool(self, server_name: str, tool_name: str,
                             description: Optional[str] = None) -> Callable:
        """
        Create a LangChain-compatible tool from an MCP tool.

        Args:
            server_name: MCP server name
            tool_name: Tool name on the server
            description: Optional tool description

        Returns:
            Callable tool function for LangChain
        """
        def tool_function(**kwargs) -> Any:
            """Execute the MCP tool."""
            return self.mcp_client.call_tool(server_name, tool_name, kwargs)

        tool_function.__name__ = f"{server_name}_{tool_name}"
        tool_function.__doc__ = description or f"{tool_name} from {server_name}"

        return tool_function

    def create_langchain_tools_from_server(self, server_name: str) -> List[Callable]:
        """
        Create LangChain tools for all tools on an MCP server.

        Args:
            server_name: MCP server name

        Returns:
            List of LangChain-compatible tool functions
        """
        if not self.mcp_client.connect_server(server_name):
            raise RuntimeError(f"Failed to connect to server {server_name}")

        tools = self.mcp_client.list_tools(server_name)
        langchain_tools = []

        for tool in tools:
            tool_name = tool.get("name")
            description = tool.get("description")
            langchain_tool = self.create_langchain_tool(
                server_name, tool_name, description
            )
            langchain_tools.append(langchain_tool)

        return langchain_tools

    def get_all_available_tools(self) -> Dict[str, List[str]]:
        """
        Get all available tools across all configured servers.

        Returns:
            Dictionary mapping server names to lists of tool names
        """
        all_tools = {}

        for server_name in self.mcp_client.list_servers():
            try:
                self.mcp_client.connect_server(server_name)
                tools = self.mcp_client.list_tools(server_name)
                all_tools[server_name] = [t.get("name") for t in tools]
            except Exception as e:
                print(f"Error connecting to {server_name}: {e}")
                all_tools[server_name] = []

        return all_tools
