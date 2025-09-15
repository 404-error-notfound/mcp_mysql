[![简体中文](https://img.shields.io/badge/简体中文-点击查看-orange)](README-zh.md)
[![English](https://img.shields.io/badge/English-Click-yellow)](README.md)

# MySQL MCP 服务器

一个功能全面的 MySQL 模型上下文协议（MCP）服务器，具有数据库分析、健康监控和 AI 辅助数据库管理的高级功能。

## 🚀 主要特性

**MySQL MCP 服务器**不仅提供基础的 CRUD 操作，更包含强大的数据库分析能力和可扩展的自定义工具框架。

### 🔌 传输模式
- **STDIO 模式**：与 Cursor、Cline 等 MCP 客户端直接集成
- **SSE 模式**：基于 HTTP 的服务器推送事件，适用于 Web 应用

### 🗄️ 数据库操作
- **跨数据库访问**：一次连接，访问所有数据库，无需切换连接
- **多语句执行**：支持用 ";" 分隔的多条 SQL 语句执行
- **智能表发现**：根据注释和描述查找表
- **SQL 执行计划分析**：性能优化建议

### 🛡️ 安全与权限
- **基于角色的访问控制**：三种权限级别（只读、读写、管理员）
- **SQL 注释支持**：处理包含 `--` 和 `/* */` 注释的 SQL 语句

### 🔍 高级分析
- **健康监控**：连接、事务和锁状态分析
- **性能洞察**：索引使用分析和优化建议
- **锁检测**：行级锁和表级锁监控
- **中文文本处理**：中文字段名转拼音功能

### 🤖 AI 集成
- **提示模板**：预置的数据库分析和查询 AI 提示
- **上下文感知辅助**：智能数据库操作指导

## 📋 权限级别

| 角色 | 权限 | 使用场景 |
|------|------|----------|
| **readonly** | `SELECT`、`SHOW`、`DESCRIBE`、`EXPLAIN`、`USE` | 报表和分析的只读访问 |
| **writer** | readonly + `INSERT`、`UPDATE`、`DELETE` | 应用开发和数据操作 |
| **admin** | 完整数据库管理权限 | 包括 DDL、用户管理、备份/恢复在内的完整数据库管理 |

## 🛠️ 可用工具

### 数据库操作
| 工具 | 描述 |
|------|------|
| `execute_sql` | 基于角色权限控制执行 SQL 语句 |
| `get_databases` | 列出所有可用数据库（排除系统数据库） |

### 模式发现
| 工具 | 描述 |
|------|------|
| `get_table_desc` | 跨数据库获取表结构（支持 `database.table` 格式） |
| `get_table_index` | 获取表索引，支持跨数据库 |
| `get_table_name` | 根据注释和描述查找表 |

### 性能和健康
| 工具 | 描述 |
|------|------|
| `get_db_health_running` | 分析 MySQL 健康状况（连接、事务、锁） |
| `get_db_health_index_usage` | 索引使用分析和性能建议 |
| `get_table_lock` | 检测行级锁和表级锁 |

### 实用工具
| 工具 | 描述 |
|------|------|
| `get_chinese_initials` | 将中文字段名转换为拼音首字母 |

## 🤖 AI 提示模板

| 提示模板 | 用途 |
|----------|------|
| `analyzing-mysql-prompt` | 全面的 MySQL 问题分析和故障排除 |
| `query-table-data-prompt` | 智能表数据查询 AI 辅助 |

## 🚀 快速开始

### 前置要求
- Python 3.10+
- UV 包管理器
- MySQL 服务器

### 安装

1. **克隆并安装依赖：**
   ```bash
   git clone <repository-url>
   cd mcp_mysql
   uv sync
   ```

2. **配置数据库连接：**
   
   创建 `.env` 文件：
   ```env
   # MySQL 数据库配置
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   # MYSQL_DATABASE=specific_db  # 可选：留空则可跨数据库访问
   MYSQL_ROLE=admin  # 选项：readonly, writer, admin
   ```

### 运行服务器

#### SSE 模式（基于 Web）
```bash
# 启动 SSE 服务器，监听 http://localhost:9000
uv run server.py
```

**MCP 客户端配置（SSE）：**
```json
{
  "mcpServers": {
    "mysql": {
      "name": "mysql",
      "description": "MySQL 数据库操作",
      "isActive": true,
      "baseUrl": "http://localhost:9000/sse"
    }
  }
}
```

#### STDIO 模式（直接集成）
```bash
# 启动 STDIO 服务器
uv run server.py --stdio
```

**MCP 客户端配置（STDIO）：**
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

## 🔧 扩展自定义工具

1. **创建新工具类：**
   ```python
   # src/handles/my_custom_tool.py
   from .base import BaseHandler
   from mcp.types import Tool, TextContent
   
   class MyCustomTool(BaseHandler):
       name = "my_custom_tool"
       description = "工具功能描述"
       
       def get_tool_description(self) -> Tool:
           # 定义工具模式
           pass
           
       async def run_tool(self, arguments: dict) -> list[TextContent]:
           # 实现工具逻辑
           pass
   ```

2. **注册工具：**
   ```python
   # src/handles/__init__.py
   from .my_custom_tool import MyCustomTool
   
   __all__ = [..., "MyCustomTool"]
   ```

## 💡 使用示例

### 跨数据库操作

**列出所有数据库：**
```
使用 get_databases 工具
```

**跨数据库查询：**
```sql
SELECT u.name, o.total 
FROM users_db.users u
JOIN orders_db.orders o ON u.id = o.user_id;
```

**表结构分析：**
```
get_table_desc: "users_db.users,orders_db.orders"
```

### AI 辅助操作

**性能分析：**
```
分析这个慢查询并提供优化建议：
SELECT * FROM large_table lt 
LEFT JOIN another_table at ON lt.id = at.foreign_id 
WHERE lt.created_date > '2024-01-01'
```

**健康监控：**
```
检查 MySQL 健康状态并识别任何性能问题
```

**智能表发现：**
```
查找所有与用户管理相关的表，搜索所有数据库
```

**死锁分析：**
```
分析为什么这个 UPDATE 语句卡住了：
UPDATE users SET status = 'active' WHERE id = 123
```

## 📖 文档

- [开发指南](CLAUDE.md) - 适用于使用此代码库的开发者
- [API 参考](src/) - 详细的工具和提示文档

## 🤝 贡献

1. Fork 仓库
2. 创建功能分支
3. 添加自定义工具或改进
4. 提交拉取请求

## 📄 许可证

此项目为开源项目。请查看许可证文件了解详情。

---

**如果觉得有帮助，请给个星星！⭐**

#### 帮忙点个赞啊，朋友们。🙏