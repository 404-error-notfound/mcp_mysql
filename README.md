[![简体中文](https://img.shields.io/badge/简体中文-点击查看-orange)](README-zh.md)
[![English](https://img.shields.io/badge/English-Click-yellow)](README.md)

# MySQL MCP Server

A comprehensive Model Context Protocol (MCP) server for MySQL database operations with advanced features for database analysis, health monitoring, and AI-assisted database management.

## 🚀 Features

**MySQL MCP Server** goes beyond basic CRUD operations, providing powerful database analysis capabilities and an extensible framework for custom tools.

### 🔌 Transport Modes
- **STDIO Mode**: Direct integration with MCP clients like Cursor, Cline
- **SSE Mode**: HTTP-based Server-Sent Events for web applications

### 🗄️ Database Operations
- **Cross-Database Access**: Connect once, access all databases without switching connections
- **Multi-Statement Execution**: Execute multiple SQL statements separated by ";"
- **Smart Table Discovery**: Find tables by comments and descriptions
- **SQL Execution Plan Analysis**: Performance optimization insights

### 🛡️ Security & Permissions
- **Role-Based Access Control**: Three permission levels (readonly, writer, admin)
- **SQL Comment Support**: Handles SQL statements with `--` and `/* */` comments

### 🔍 Advanced Analysis
- **Health Monitoring**: Connection, transaction, and lock status analysis
- **Performance Insights**: Index usage analysis and optimization recommendations
- **Lock Detection**: Row-level and table-level lock monitoring
- **Chinese Text Processing**: Pinyin conversion for Chinese field names

### 🤖 AI Integration
- **Prompt Templates**: Pre-built AI prompts for database analysis and querying
- **Context-Aware Assistance**: Intelligent database operation guidance

## 📋 Permission Levels

| Role | Permissions | Use Case |
|------|-------------|----------|
| **readonly** | `SELECT`, `SHOW`, `DESCRIBE`, `EXPLAIN`, `USE` | Read-only access for reporting and analysis |
| **writer** | readonly + `INSERT`, `UPDATE`, `DELETE` | Application development and data manipulation |
| **admin** | Full database administration | Complete database management including DDL, user management, backup/recovery |

## 🛠️ Available Tools

### Database Operations
| Tool | Description |
|------|-------------|
| `execute_sql` | Execute SQL statements with role-based permission control |
| `get_databases` | List all available databases (excluding system databases) |

### Schema Discovery
| Tool | Description |
|------|-------------|
| `get_table_desc` | Get table structures across databases (supports `database.table` format) |
| `get_table_index` | Retrieve table indexes with cross-database support |
| `get_table_name` | Find tables by comments and descriptions |

### Performance & Health
| Tool | Description |
|------|-------------|
| `get_db_health_running` | Analyze MySQL health (connections, transactions, locks) |
| `get_db_health_index_usage` | Index usage analysis with performance recommendations |
| `get_table_lock` | Detect row-level and table-level locks |

### Utilities
| Tool | Description |
|------|-------------|
| `get_chinese_initials` | Convert Chinese field names to pinyin initials |

## 🤖 AI Prompt Templates

| Prompt Template | Purpose |
|----------------|----------|
| `analyzing-mysql-prompt` | Comprehensive MySQL issue analysis and troubleshooting |
| `query-table-data-prompt` | Intelligent table data querying with AI assistance |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- UV package manager
- MySQL server

### Installation

#### 📦 Installing UV Package Manager

**Windows:**
```powershell
# Using PowerShell (Recommended)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv

# Or using Chocolatey
choco install uv

# Or using Scoop
scoop install uv
```

**Linux/macOS:**
```bash
# Using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

#### 🔽 Project Setup

1. **Clone and install dependencies:**

   **Windows (PowerShell):**
   ```powershell
   git clone <repository-url>
   cd mcp_mysql
   uv sync
   ```

   **Linux/macOS:**
   ```bash
   git clone <repository-url>
   cd mcp_mysql
   uv sync
   ```

2. **Configure database connection:**

   Create a `.env` file in the project root directory:

   **Windows (PowerShell):**
   ```powershell
   # Create .env file using PowerShell
   @"
   # MySQL Database Configuration
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   # MYSQL_DATABASE=specific_db  # Optional: leave empty for cross-database access
   MYSQL_ROLE=admin  # Options: readonly, writer, admin
   "@ | Out-File -FilePath ".env" -Encoding utf8
   ```

   **Or manually create `.env` file with content:**
   ```env
   # MySQL Database Configuration
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   # MYSQL_DATABASE=specific_db  # Optional: leave empty for cross-database access
   MYSQL_ROLE=admin  # Options: readonly, writer, admin
   ```

   **For remote MySQL server (example):**
   ```env
   MYSQL_HOST=192.168.1.100
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_secure_password
   MYSQL_ROLE=admin
   ```

### Running the Server

#### SSE Mode (Web-based)

**Windows (PowerShell):**
```powershell
# Start SSE server on http://localhost:9000
uv run server.py
```

**Linux/macOS:**
```bash
# Start SSE server on http://localhost:9000
uv run server.py
```

**MCP Client Configuration (SSE):**
```json
{
  "mcpServers": {
    "mysql": {
      "name": "mysql",
      "description": "MySQL database operations",
      "isActive": true,
      "baseUrl": "http://localhost:9000/sse"
    }
  }
}
```

#### STDIO Mode (Direct integration)

**Windows (PowerShell):**
```powershell
# Start STDIO server
uv run server.py --stdio
```

**Linux/macOS:**
```bash
# Start STDIO server
uv run server.py --stdio
```

**MCP Client Configuration (STDIO):**

**Windows:**
```json
{
  "mcpServers": {
    "mysql": {
      "name": "mysql",
      "command": "uv",
      "args": [
        "--directory", "C:\\path\\to\\mcp_mysql",
        "run", "server.py", "--stdio"
      ],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "your_username",
        "MYSQL_PASSWORD": "your_password",
        "MYSQL_ROLE": "admin"
      }
    }
  }
}
```

**Linux/macOS:**
```json
{
  "mcpServers": {
    "mysql": {
      "name": "mysql",
      "command": "uv",
      "args": [
        "--directory", "/path/to/mcp_mysql",
        "run", "server.py", "--stdio"
      ],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "your_username",
        "MYSQL_PASSWORD": "your_password",
        "MYSQL_ROLE": "admin"
      }
    }
  }
}
```

## 🛠️ Windows-Specific Configuration Notes

### Common Issues and Solutions

**PowerShell Execution Policy:**
If you encounter execution policy errors, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path Separators:**
- Use double backslashes `\\` or forward slashes `/` in JSON configuration
- Example: `"C:\\Users\\YourName\\mcp_mysql"` or `"C:/Users/YourName/mcp_mysql"`

**Environment Variables in Windows:**
```powershell
# Set environment variables temporarily (current session)
$env:MYSQL_HOST = "localhost"
$env:MYSQL_USER = "your_username"
$env:MYSQL_PASSWORD = "your_password"

# Run the server with environment variables
uv run server.py --stdio
```

**Windows Firewall:**
Ensure MySQL port (default 3306) is allowed through Windows Firewall if connecting to remote MySQL server.

## 🔧 Extending with Custom Tools

1. **Create a new tool class:**
   ```python
   # src/handles/my_custom_tool.py
   from .base import BaseHandler
   from mcp.types import Tool, TextContent
   
   class MyCustomTool(BaseHandler):
       name = "my_custom_tool"
       description = "Description of what this tool does"
       
       def get_tool_description(self) -> Tool:
           # Define tool schema
           pass
           
       async def run_tool(self, arguments: dict) -> list[TextContent]:
           # Implement tool logic
           pass
   ```

2. **Register the tool:**
   ```python
   # src/handles/__init__.py
   from .my_custom_tool import MyCustomTool
   
   __all__ = [..., "MyCustomTool"]
   ```

## 💡 Usage Examples

### Cross-Database Operations

**List all databases:**
```
Use get_databases tool
```

**Cross-database queries:**
```sql
SELECT u.name, o.total 
FROM users_db.users u
JOIN orders_db.orders o ON u.id = o.user_id;
```

**Table structure analysis:**
```
get_table_desc: "users_db.users,orders_db.orders"
```

### AI-Assisted Operations

**Performance Analysis:**
```
Analyze this slow query and suggest optimizations:
SELECT * FROM large_table lt 
LEFT JOIN another_table at ON lt.id = at.foreign_id 
WHERE lt.created_date > '2024-01-01'
```

**Health Monitoring:**
```
Check MySQL health status and identify any performance issues
```

**Smart Table Discovery:**
```
Find all tables related to user management across all databases
```

**Deadlock Analysis:**
```
Analyze why this UPDATE statement is stuck:
UPDATE users SET status = 'active' WHERE id = 123
```

## 📖 Documentation

- [Development Guide](CLAUDE.md) - For developers working with this codebase
- [API Reference](src/) - Detailed tool and prompt documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your custom tools or improvements
4. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

---

**Star this repository if you find it helpful! ⭐**