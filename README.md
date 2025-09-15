[![简体中文](https://img.shields.io/badge/简体中文-点击查看-orange)](README-zh.md)
[![English](https://img.shields.io/badge/English-Click-yellow)](README.md)

# mcp_mysql_server

## Introduction
mcp_mysql_server_pro is not just about MySQL CRUD operations, but also includes database anomaly analysis capabilities and makes it easy for developers to extend with custom tools.

- Supports both STDIO and SSE modes
- **Supports access to all databases without connecting to a specific database**
- Supports multiple SQL execution, separated by ";"
- Supports querying database table names and fields based on table comments
- Supports SQL execution plan analysis
- Supports Chinese field to pinyin conversion
- Supports table lock analysis
- Supports database health status analysis
- Supports permission control with three roles: readonly, writer, and admin
    ```
    "readonly": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "USE"],  # Read-only permissions
    
    "writer": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "INSERT", "UPDATE", "DELETE", "USE"],  # Read-write permissions
    
    "admin": [
        # Complete database administrator permissions, including:
        # Query permissions: SELECT, SHOW, DESCRIBE, EXPLAIN
        # Database usage: USE
        # Data operations: INSERT, UPDATE, DELETE, REPLACE, LOAD
        # Table structure management: CREATE, ALTER, DROP, TRUNCATE, RENAME
        # Database management: CREATE DATABASE, DROP DATABASE, ALTER DATABASE
        # Index management: CREATE INDEX, DROP INDEX, ALTER INDEX
        # View management: CREATE VIEW, DROP VIEW, ALTER VIEW
        # Stored procedures/functions: CREATE/DROP/ALTER PROCEDURE/FUNCTION
        # Triggers: CREATE TRIGGER, DROP TRIGGER
        # Event scheduler: CREATE/DROP/ALTER EVENT
        # User management: CREATE/DROP/ALTER/RENAME USER, GRANT, REVOKE
        # System administration: SHUTDOWN, RELOAD, LOCK, UNLOCK, PROCESS, SUPER
        # Backup and recovery: BACKUP, RESTORE, BACKUP_ADMIN, BINLOG_ADMIN
        # Replication management: REPLICATION SLAVE/CLIENT, REPLICATION_SLAVE_ADMIN
        # Performance tuning: OPTIMIZE, ANALYZE, CHECK, CHECKSUM, REPAIR
        # Temporary tables: CREATE TEMPORARY TABLES
        # File operations: FILE, SELECT INTO OUTFILE, LOAD DATA
        # Other advanced permissions: REFERENCES, USAGE, EXECUTE, etc.
    ]  # Complete database administrator permissions
    ```
    
    **Note**: The permission system supports recognizing SQL statements with comments (supports `--` and `/* */` comment formats), automatically skipping comment lines for permission verification.
- Supports prompt template invocation

## Tool List
| Tool Name                  | Description                                                                                                                                                                                                              |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| execute_sql                | SQL execution tool that can access all databases and supports complete MySQL operations based on permission configuration: readonly (queries), writer (CRUD operations), admin (complete database administration including database creation, user management, backup/recovery, etc.) |
| get_databases              | Get a list of all available databases on the MySQL server (excluding system databases)                                                                                                                                   |
| get_chinese_initials       | Convert Chinese field names to pinyin initials                                                                                                                                                                           |
| get_db_health_running      | Analyze MySQL health status (connection status, transaction status, running status, lock detection)                                                                                                                      |
| get_table_desc             | Search for table structures in all databases based on table names, supports multi-table queries and database.table_name format                                                                                          |
| get_table_index            | Search for table indexes in all databases based on table names, supports multi-table queries and database.table_name format                                                                                             |
| get_table_lock             | Query whether there are row-level locks and table-level locks on the current MySQL server                                                                                                                               |
| get_table_name             | Search for table names in all databases based on table comments and descriptions                                                                                                                                         |
| get_db_health_index_usage  | Get index usage of MySQL databases, including redundant indexes, poorly performing indexes, and top 5 unused indexes with query times greater than 30 seconds, supports specifying database for analysis            |

## Prompt List
| Prompt Name               | Description                                                                                    |
|---------------------------|------------------------------------------------------------------------------------------------| 
| analyzing-mysql-prompt    | This is a prompt for analyzing MySQL-related issues                                           |
| query-table-data-prompt   | This is a prompt for querying table data using tools. If description is empty, it will be initialized as a MySQL database query assistant |

## Usage Instructions

### SSE Mode

- Use uv to start the service

Add the following content to your mcp client tools, such as cursor, cline, etc.

mcp json as follows:
```
{
  "mcpServers": {
    "operateMysql": {
      "name": "operateMysql",
      "description": "",
      "isActive": true,
      "baseUrl": "http://localhost:9000/sse"
    }
  }
}
```

Modify the .env file content to update the database connection information with your database details:
```
# MySQL Database Configuration
MYSQL_HOST=192.168.xxx.xxx
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
# MYSQL_DATABASE=a_llm  # Optional: if not specified, can access all databases
MYSQL_ROLE=admin  # Optional, default is 'readonly'. Available values: readonly, writer, admin
```

Start commands:
```
# Download dependencies
uv sync

# Start
uv run server.py
```

### STDIO Mode

Add the following content to your mcp client tools, such as cursor, cline, etc.

mcp json as follows:
```
{
  "mcpServers": {
      "operateMysql": {
        "isActive": true,
        "name": "operateMysql",
        "command": "uv",
        "args": [
          "--directory",
          "G:\\python\\mysql_mcp\\src",  # Replace this with your project path
          "run",
          "server.py",
          "--stdio"
        ],
        "env": {
          "MYSQL_HOST": "192.168.xxx.xxx",
          "MYSQL_PORT": "3306",
          "MYSQL_USER": "root",
          "MYSQL_PASSWORD": "root",
          // "MYSQL_DATABASE": "a_llm",  // Optional: if not specified, can access all databases
          "MYSQL_ROLE": "admin"  # Optional, default is 'readonly'. Available values: readonly, writer, admin
       }
    }
  }
}    
```

## Custom Tool Extensions
1. Add a new tool class in the handles package, inherit from BaseHandler, and implement get_tool_description and run_tool methods

2. Import the new tool in __init__.py to make it available in the server

## Cross-Database Operation Examples

Now you can:

1. **View all databases**:
```
Use the get_databases tool to view all available databases
```

2. **Cross-database queries**:
```sql
SELECT * FROM database1.table1 
UNION ALL 
SELECT * FROM database2.table1;
```

3. **Specify database operations**:
```sql
USE database_name;
SELECT * FROM table_name;
```

4. **Cross-database table structure queries**:
```
Use get_table_desc tool to query: database1.table1,database2.table2
```

## Examples
1. Create a new table and insert data, prompt format as follows:
```
# Task
   Create an organizational structure table in database_name with the following structure: department name, department number, parent department, is valid.
# Requirements
 - Table name: t_admin_rms_zzjg
 - Field requirements: string type uses 'varchar(255)', integer type uses 'int', float type uses 'float', date and time type uses 'datetime', boolean type uses 'boolean', text type uses 'text', large text type uses 'longtext', large integer type uses 'bigint', large float type uses 'double'
 - Table header needs to include primary key field, serial number XH varchar(255)
 - Table must include these fixed fields at the end: creator-CJR varchar(50), creation time-CJSJ datetime, modifier-XGR varchar(50), modification time-XGSJ datetime
 - Field naming should use tool return content
 - Common fields need indexes
 - Each field needs comments, table needs comment
 - Generate 5 real data records after creation
```

2. Query data based on table comments, prompt as follows:
```
Query Zhang San's data from the user information table
```

3. Analyze slow SQL, prompt as follows:
```
select * from database_name.t_jcsjzx_hjkq_cd_xsz_sk xsz
left join database_name.t_jcsjzx_hjkq_jcd jcd on jcd.cddm = xsz.cddm 
Based on current index situation, review execution plan and provide optimization suggestions in markdown format, including table index status, execution details, and optimization recommendations
```

4. Analyze SQL deadlock issues, prompt as follows:
```
update database_name.t_admin_rms_zzjg set sfyx = '0' where xh = '1' is stuck, please analyze the cause
```

5. Analyze the health status prompt as follows
```
Check the current health status of MySQL
```

6. Cross-database query example
```
Query all user table data from database1 and database2
```