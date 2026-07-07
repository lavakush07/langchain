"""
Example Usage of MCP Tools with LangChain

This file demonstrates common patterns for using MCP tools in LangChain applications.
"""

from mcp_sdk_integration import MCPClient, LangChainMCPIntegration
from mcp_tools import (
    read_file, write_file, list_directory, search_files,
    get_repository, list_pull_requests,
    execute_query, list_tables,
    fetch_url, search_web
)


def example_filesystem_operations():
    """Example: File system operations with MCP tools."""
    print("=== Filesystem Operations ===\n")

    # List directory contents
    files = list_directory("/Users/lavakush/langchain", recursive=False)
    print(f"Found {len(files)} files/directories")
    for f in files[:5]:
        print(f"  - {f['name']} ({'file' if f['is_file'] else 'dir'})")

    # Search for Python files
    results = search_files(
        directory="/Users/lavakush/langchain",
        query="import",
        file_extensions=[".py"],
        max_results=5
    )
    print(f"\nSearch results: {len(results)} matches")
    for r in results:
        print(f"  {r['relative_path']}:{r['line_number']}")

    # Read and write files
    content = "# MCP Tools Example\n\nThis is a test file."
    result = write_file("/tmp/mcp_test.txt", content)
    print(f"\nWrote {result['bytes_written']} bytes to {result['file_path']}")

    read_content = read_file("/tmp/mcp_test.txt")
    print(f"Read back: {read_content[:50]}...")


def example_github_operations():
    """Example: GitHub operations with MCP tools."""
    print("\n=== GitHub Operations ===\n")

    # Get repository info
    repo = get_repository(owner="langchain-ai", repo="langchain")
    print(f"Repository: {repo['full_name']}")
    print(f"URL: {repo['url']}")

    # List pull requests
    prs = list_pull_requests(
        owner="langchain-ai",
        repo="langchain",
        state="open",
        limit=5
    )
    print(f"\nOpen PRs: {len(prs)}")


def example_database_operations():
    """Example: Database operations with MCP tools."""
    print("\n=== Database Operations ===\n")

    # List tables
    tables = list_tables(database="default")
    print(f"Tables: {len(tables)}")

    # Execute query
    results = execute_query(
        query="SELECT name FROM sqlite_master WHERE type='table'",
        database="default"
    )
    print(f"Query returned {results['row_count']} rows")


def example_web_operations():
    """Example: Web operations with MCP tools."""
    print("\n=== Web Operations ===\n")

    # Fetch URL
    response = fetch_url("https://www.langchain.com")
    print(f"Fetched {response['url']}")
    print(f"Status: {response['status_code']}")
    print(f"Content type: {response['content_type']}")

    # Search web
    results = search_web(query="langchain python tutorial", count=3)
    print(f"\nSearch results: {len(results)}")


def example_mcp_client():
    """Example: Using MCPClient to interact with servers."""
    print("\n=== MCP Client ===\n")

    # Initialize client
    client = MCPClient()

    # List available servers
    servers = client.list_servers()
    print(f"Available servers: {', '.join(servers)}")

    # Connect to server
    if "filesystem" in servers:
        client.connect_server("filesystem")
        print("\nConnected to filesystem server")

        # List tools
        tools = client.list_tools("filesystem")
        print(f"Available tools: {len(tools)}")


def example_langchain_integration():
    """Example: LangChain integration with MCP."""
    print("\n=== LangChain Integration ===\n")

    # Initialize integration
    integration = LangChainMCPIntegration()

    # Get all available tools
    all_tools = integration.get_all_available_tools()
    print("Available tools by server:")
    for server, tools in all_tools.items():
        print(f"  {server}: {len(tools)} tools")

    # Create LangChain tool from MCP
    try:
        tools = integration.create_langchain_tools_from_server("github")
        print(f"\nCreated {len(tools)} LangChain tools from GitHub server")
    except Exception as e:
        print(f"Note: {e}")


def example_combined_workflow():
    """Example: Combined workflow using multiple MCP tools."""
    print("\n=== Combined Workflow ===\n")

    # 1. Search for files in codebase
    print("Step 1: Searching for files...")
    code_files = search_files(
        directory="/Users/lavakush/langchain",
        query="def",
        file_extensions=[".py"],
        max_results=3
    )
    print(f"Found {len(code_files)} Python files with functions")

    # 2. Read one of the files
    if code_files:
        first_file = code_files[0]['file_path']
        print(f"\nStep 2: Reading {first_file}...")
        try:
            content = read_file(first_file)
            print(f"File has {len(content)} characters")
        except Exception as e:
            print(f"Error reading file: {e}")

    # 3. Search web for related information
    print("\nStep 3: Searching web for LangChain info...")
    web_results = search_web(query="langchain mcp integration", count=2)
    print(f"Found {len(web_results)} web results")

    # 4. Save summary to file
    print("\nStep 4: Saving workflow summary...")
    summary = f"""# MCP Workflow Summary

Files analyzed: {len(code_files)}
Web results: {len(web_results)}

This workflow demonstrated:
- File system search
- File reading
- Web search
- File writing
"""
    result = write_file("/tmp/mcp_workflow_summary.md", summary)
    print(f"Saved summary to {result['file_path']}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("MCP Tools Examples for LangChain")
    print("=" * 60)

    try:
        example_filesystem_operations()
        example_github_operations()
        example_database_operations()
        example_web_operations()
        example_mcp_client()
        example_langchain_integration()
        example_combined_workflow()
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Note: Some examples require proper MCP server setup and credentials")

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
