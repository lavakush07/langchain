"""
Filesystem MCP Tools

Common filesystem operations using MCP protocol.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any


def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """
    Read contents of a file.

    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)

    Returns:
        File contents as string
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {str(e)}")


def write_file(file_path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """
    Write content to a file.

    Args:
        file_path: Path to the file to write
        content: Content to write
        encoding: File encoding (default: utf-8)

    Returns:
        Dictionary with success status and file info
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return {
            "success": True,
            "file_path": file_path,
            "bytes_written": len(content.encode(encoding))
        }
    except Exception as e:
        raise Exception(f"Error writing file {file_path}: {str(e)}")


def list_directory(directory_path: str, recursive: bool = False,
                   pattern: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List contents of a directory.

    Args:
        directory_path: Path to the directory
        recursive: Whether to list recursively
        pattern: Optional glob pattern to filter results

    Returns:
        List of file/directory info dictionaries
    """
    try:
        path = Path(directory_path)
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")

        results = []
        if recursive:
            if pattern:
                paths = path.rglob(pattern)
            else:
                paths = path.rglob("*")
        else:
            if pattern:
                paths = path.glob(pattern)
            else:
                paths = path.iterdir()

        for p in paths:
            stat = p.stat()
            results.append({
                "path": str(p),
                "name": p.name,
                "is_file": p.is_file(),
                "is_dir": p.is_dir(),
                "size": stat.st_size if p.is_file() else None,
                "modified": stat.st_mtime
            })

        return results
    except Exception as e:
        raise Exception(f"Error listing directory {directory_path}: {str(e)}")


def search_files(directory: str, query: str, file_extensions: Optional[List[str]] = None,
                max_results: int = 100) -> List[Dict[str, Any]]:
    """
    Search for files containing a query string.

    Args:
        directory: Root directory to search
        query: Search query string
        file_extensions: Optional list of file extensions to filter (e.g., ['.py', '.txt'])
        max_results: Maximum number of results to return

    Returns:
        List of search results with file paths and matching lines
    """
    results = []
    path = Path(directory)

    try:
        for file_path in path.rglob("*"):
            if not file_path.is_file():
                continue

            if file_extensions and file_path.suffix not in file_extensions:
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if query in line:
                            results.append({
                                "file_path": str(file_path),
                                "line_number": line_num,
                                "line_content": line.strip(),
                                "relative_path": str(file_path.relative_to(path))
                            })

                            if len(results) >= max_results:
                                return results
            except (UnicodeDecodeError, PermissionError):
                # Skip binary files or files without read permission
                continue

        return results
    except Exception as e:
        raise Exception(f"Error searching files in {directory}: {str(e)}")
