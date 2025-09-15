# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a MySQL MCP (Model Context Protocol) server that provides comprehensive MySQL database operations and analysis capabilities. The server supports both STDIO and SSE (Server-Sent Events) transport modes and offers tools for database management, health monitoring, and performance analysis.

## Development Commands

### Dependencies and Setup
```bash
# Install dependencies
uv sync

# Start in SSE mode (default)
uv run server.py

# Start in STDIO mode
uv run server.py --stdio
```

### Environment Configuration
Create a `.env` file with the following configuration:
```env
MYSQL_HOST=192.168.xxx.xxx
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
# MYSQL_DATABASE=database_name  # Optional: if not specified, can access all databases
MYSQL_ROLE=admin  # Options: readonly, writer, admin
```

## Architecture

### Core Components

1. **Server (`src/server.py`)**: Main MCP server implementation supporting both STDIO and SSE transport modes
2. **Tool Registry System (`src/handles/base.py`)**: Auto-registration system for database operation tools
3. **Prompt Registry System (`src/prompts/BasePrompt.py`)**: Template system for AI-assisted database operations
4. **Database Configuration (`src/config/dbconfig.py`)**: Role-based permission system and connection management

### Tool Architecture

Tools are implemented as classes that inherit from `BaseHandler` and are automatically registered via the `ToolRegistry`:

- Each tool class defines `name` and `description` class attributes
- Tools implement `get_tool_description()` and `run_tool()` methods
- Auto-registration happens through `__init_subclass__()` metaclass functionality

### Available Tools

**Database Operations:**
- `execute_sql`: Execute SQL with role-based permissions (readonly/writer/admin)
- `get_databases`: List all available databases (excluding system databases)

**Schema Analysis:**
- `get_table_desc`: Get table structure across all databases
- `get_table_index`: Get table indexes across all databases  
- `get_table_name`: Search tables by comments/descriptions

**Performance & Health:**
- `get_db_health_running`: Analyze MySQL health status (connections, transactions, locks)
- `get_db_health_index_usage`: Analyze index usage and performance
- `get_table_lock`: Check for row-level and table-level locks

**Utilities:**
- `get_chinese_initials`: Convert Chinese field names to pinyin initials

### Permission System

Three role levels with escalating permissions:
- **readonly**: SELECT, SHOW, DESCRIBE, EXPLAIN, USE
- **writer**: readonly + INSERT, UPDATE, DELETE  
- **admin**: Complete database administration privileges including DDL, user management, backup/recovery

The system automatically validates SQL statements against role permissions, including support for SQL comments.

### Prompt Templates

The system includes AI prompt templates for common database tasks:
- `analyzing-mysql-prompt`: For MySQL issue analysis
- `query-table-data-prompt`: For intelligent table data querying

## Adding New Tools

1. Create a new class in `src/handles/` that inherits from `BaseHandler`
2. Set the `name` and `description` class attributes
3. Implement `get_tool_description()` and `run_tool()` methods
4. Import the class in `src/handles/__init__.py`
5. The tool will be automatically registered and available

## Cross-Database Operations

The server supports operations across multiple databases without requiring connection to a specific database:
- Use `database.table_name` syntax for cross-database queries
- Tools like `get_table_desc` can search across all databases
- The `get_databases` tool lists all available databases

## Transport Modes

**STDIO Mode**: For command-line MCP clients
**SSE Mode**: For web-based clients, runs HTTP server on port 9000 with `/sse` endpoint for connections and `/messages/` for message handling