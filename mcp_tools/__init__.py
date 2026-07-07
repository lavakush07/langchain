"""
MCP Tools for LangChain Integration

This package provides commonly used MCP tools and utilities for integrating
with the Model Context Protocol in LangChain applications.
"""

from .filesystem_tools import (
    read_file,
    write_file,
    list_directory,
    search_files,
)
from .github_tools import (
    get_repository,
    list_pull_requests,
    create_issue,
    search_code,
)
from .database_tools import (
    execute_query,
    list_tables,
    get_schema,
)
from .web_tools import (
    fetch_url,
    search_web,
    scrape_page,
)

__all__ = [
    # Filesystem
    "read_file",
    "write_file",
    "list_directory",
    "search_files",
    # GitHub
    "get_repository",
    "list_pull_requests",
    "create_issue",
    "search_code",
    # Database
    "execute_query",
    "list_tables",
    "get_schema",
    # Web
    "fetch_url",
    "search_web",
    "scrape_page",
]
