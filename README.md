# LangChain MCP Integration

This repository provides Model Context Protocol (MCP) tools, servers, and SDK integrations for LangChain applications.

## Overview

The Model Context Protocol (MCP) is a standardized way for AI applications to interact with external tools, data sources, and services. This integration brings commonly used MCP servers and tools into the LangChain ecosystem.

## Structure

```
langchain/
├── mcp_config.json          # MCP server configurations
├── mcp_sdk_integration.py   # LangChain-MCP integration layer
├── mcp_tools/              # Python MCP tool implementations
│   ├── __init__.py
│   ├── filesystem_tools.py  # File system operations
│   ├── github_tools.py      # GitHub API tools
│   ├── database_tools.py    # Database operations
│   └── web_tools.py         # Web fetching and scraping
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configured MCP Servers

### 1. **Filesystem Server**
- File reading and writing
- Directory listing
- File search

### 2. **GitHub Server**
- Repository management
- Pull request operations
- Issue tracking
- Code search

### 3. **Git Server**
- Version control operations
- Branch management
- Commit history

### 4. **PostgreSQL Server**
- Database queries
- Schema inspection
- Data manipulation

### 5. **SQLite Server**
- Local database operations
- Lightweight data storage

### 6. **Slack Server**
- Message posting
- Channel management
- User lookup

### 7. **Brave Search Server**
- Web search
- News search
- Image search

### 8. **Puppeteer Server**
- Browser automation
- Web scraping
- Screenshot capture

### 9. **Memory Server**
- Knowledge graph storage
- Persistent memory
- Context retention

### 10. **Fetch Server**
- HTTP requests
- Web content retrieval
- API calls

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Node.js dependencies (for MCP servers):
```bash
npm install -g @modelcontextprotocol/server-filesystem \
              @modelcontextprotocol/server-github \
              @modelcontextprotocol/server-git \
              @modelcontextprotocol/server-postgres \
              @modelcontextprotocol/server-sqlite \
              @modelcontextprotocol/server-slack \
              @modelcontextprotocol/server-brave-search \
              @modelcontextprotocol/server-puppeteer \
              @modelcontextprotocol/server-memory \
              @modelcontextprotocol/server-fetch
```

3. Set up environment variables:
```bash
export GITHUB_TOKEN="your_github_token"
export DATABASE_URL="postgresql://user:pass@localhost/db"
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_TEAM_ID="your_team_id"
export BRAVE_API_KEY="your_brave_api_key"
```

## Usage

### Using the MCP Client

```python
from mcp_sdk_integration import MCPClient

# Initialize client
client = MCPClient()

# List available servers
servers = client.list_servers()
print(f"Available servers: {servers}")

# Connect to a server
client.connect_server("github")

# Call a tool
result = client.call_tool(
    server_name="github",
    tool_name="get_repository",
    arguments={"owner": "langchain-ai", "repo": "langchain"}
)
```

### Using MCP Tools Directly

```python
from mcp_tools import read_file, list_directory, search_files

# Read a file
content = read_file("/path/to/file.txt")

# List directory contents
files = list_directory("/path/to/directory", recursive=True)

# Search for files
results = search_files(
    directory="/path/to/search",
    query="import langchain",
    file_extensions=[".py"]
)
```

### LangChain Integration

```python
from langchain.agents import initialize_agent, AgentType
from langchain.llms import ChatAnthropic
from mcp_sdk_integration import LangChainMCPIntegration

# Initialize integration
mcp_integration = LangChainMCPIntegration()

# Create LangChain tools from MCP server
tools = mcp_integration.create_langchain_tools_from_server("github")

# Initialize LangChain agent with MCP tools
llm = ChatAnthropic(model="claude-sonnet-4-5")
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use the agent
response = agent.run(
    "List all open pull requests in the langchain-ai/langchain repository"
)
```

### GitHub Tools Example

```python
from mcp_tools import get_repository, list_pull_requests, create_issue

# Get repository info
repo = get_repository(owner="langchain-ai", repo="langchain")
print(f"Repository: {repo['full_name']}")
print(f"Stars: {repo['stars']}")

# List open PRs
prs = list_pull_requests(
    owner="langchain-ai",
    repo="langchain",
    state="open",
    limit=10
)

# Create an issue
issue = create_issue(
    owner="langchain-ai",
    repo="langchain",
    title="Feature request: Add MCP integration",
    body="It would be great to have built-in MCP support...",
    labels=["enhancement"]
)
```

### Database Tools Example

```python
from mcp_tools import execute_query, list_tables, get_schema

# List all tables
tables = list_tables(database="default")

# Get table schema
schema = get_schema(table_name="users", database="default")

# Execute query
results = execute_query(
    query="SELECT * FROM users WHERE active = ?",
    params=[True],
    database="default"
)
```

### Web Tools Example

```python
from mcp_tools import fetch_url, search_web, scrape_page

# Fetch URL content
response = fetch_url("https://example.com")
print(f"Status: {response['status_code']}")
print(f"Content: {response['content']}")

# Search the web
results = search_web(query="langchain mcp integration", count=5)

# Scrape a page with JavaScript
page_data = scrape_page(
    url="https://example.com",
    wait_for_selector="#content",
    javascript_enabled=True,
    extract_links=True
)
```

## Configuration

Edit `mcp_config.json` to customize server configurations:

```json
{
  "mcpServers": {
    "custom-server": {
      "command": "npx",
      "args": ["-y", "@your/custom-server"],
      "env": {
        "API_KEY": "${YOUR_API_KEY}"
      },
      "description": "Your custom MCP server"
    }
  }
}
```

## Common Use Cases

1. **File Operations**: Read, write, search files in your codebase
2. **GitHub Automation**: Manage repos, PRs, issues programmatically
3. **Database Queries**: Execute SQL, inspect schemas, export data
4. **Web Scraping**: Extract data from websites, take screenshots
5. **Search**: Find information across the web
6. **Memory**: Store and retrieve context across conversations

## Environment Variables

Required environment variables for different servers:

- `GITHUB_TOKEN`: GitHub personal access token
- `DATABASE_URL`: PostgreSQL connection string
- `SLACK_BOT_TOKEN`: Slack bot token
- `SLACK_TEAM_ID`: Slack team/workspace ID
- `BRAVE_API_KEY`: Brave Search API key

## Troubleshooting

### Server Connection Issues

If you encounter connection issues:

1. Verify Node.js packages are installed: `npm list -g @modelcontextprotocol/*`
2. Check environment variables are set
3. Ensure servers have proper permissions

### Tool Call Failures

If tool calls fail:

1. Check server logs for errors
2. Verify tool arguments match expected schema
3. Ensure network connectivity for external services

## Contributing

To add new MCP tools or servers:

1. Add server configuration to `mcp_config.json`
2. Create tool implementations in `mcp_tools/`
3. Update `__init__.py` to export new tools
4. Add usage examples to this README

## Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [LangChain Documentation](https://python.langchain.com)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)

## License

MIT License - See LICENSE file for details
