[![简体中文](https://img.shields.io/badge/简体中文-点击查看-orange)](README-zh.md)
[![English](https://img.shields.io/badge/English-Click-yellow)](README.md)

# mcp_mysql_server
#### 帮忙点个赞啊，朋友们。
## 介绍
mcp_mysql_server_pro 不仅止于mysql的增删改查功能，还包含了数据库异常分析能力，且便于开发者们进行个性化的工具扩展

- 支持 STDIO 方式 与 SSE 方式
- **支持访问所有数据库，无需连接到特定数据库**
- 支持 支持多sql执行，以";"分隔。 
- 支持 根据表注释可以查询出对于的数据库表名，表字段
- 支持 sql执行计划分析
- 支持 中文字段转拼音.
- 支持 锁表分析
- 支持 运行健康状态分析
- 支持权限控制，只读（readonly）、读写（writer）、管理员（admin）
    ```
    "readonly": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "USE"],  # 只读权限
    
    "writer": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "INSERT", "UPDATE", "DELETE", "USE"],  # 读写权限
    
    "admin": [
        # 完整的数据库管理员权限，包括：
        # 查询权限: SELECT, SHOW, DESCRIBE, EXPLAIN
        # 数据库使用: USE
        # 数据操作: INSERT, UPDATE, DELETE, REPLACE, LOAD
        # 表结构管理: CREATE, ALTER, DROP, TRUNCATE, RENAME
        # 数据库管理: CREATE DATABASE, DROP DATABASE, ALTER DATABASE
        # 索引管理: CREATE INDEX, DROP INDEX, ALTER INDEX
        # 视图管理: CREATE VIEW, DROP VIEW, ALTER VIEW
        # 存储过程/函数: CREATE/DROP/ALTER PROCEDURE/FUNCTION
        # 触发器: CREATE TRIGGER, DROP TRIGGER
        # 事件调度器: CREATE/DROP/ALTER EVENT
        # 用户管理: CREATE/DROP/ALTER/RENAME USER, GRANT, REVOKE
        # 系统管理: SHUTDOWN, RELOAD, LOCK, UNLOCK, PROCESS, SUPER
        # 备份恢复: BACKUP, RESTORE, BACKUP_ADMIN, BINLOG_ADMIN
        # 复制管理: REPLICATION SLAVE/CLIENT, REPLICATION_SLAVE_ADMIN
        # 性能调优: OPTIMIZE, ANALYZE, CHECK, CHECKSUM, REPAIR
        # 临时表: CREATE TEMPORARY TABLES
        # 文件操作: FILE, SELECT INTO OUTFILE, LOAD DATA
        # 其他高级权限: REFERENCES, USAGE, EXECUTE 等
    ]  # 完整的数据库管理员权限
    ```
    
    **注意**: 权限系统支持识别带有SQL注释的语句（支持 `--` 和 `/* */` 注释格式），会自动跳过注释行进行权限验证。
- 支持 prompt 模版调用

## 工具列表
| 工具名称                  | 描述                                                                                                                                 |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------| 
| execute_sql           | sql执行工具，可以访问所有数据库，根据权限配置支持完整的MySQL操作：readonly（查询）、writer（增删改查）、admin（完整数据库管理权限，包括数据库创建、用户管理、备份恢复等） |
| get_databases         | 获取MySQL服务器上所有可用的数据库列表（排除系统数据库）                                                                                                     |
| get_chinese_initials  | 将中文字段名转换为拼音首字母字段                                                                                                                   |
| get_db_health_running | 分析mysql的健康状态（连接情况、事务情况、运行情况、锁情况检测）                                                                                                 |
| get_table_desc        | 根据表名搜索所有数据库中对应的表结构,支持多表查询，支持database.table_name格式                                                                                  |
| get_table_index       | 根据表名搜索所有数据库中对应的表索引,支持多表查询，支持database.table_name格式                                                                                  |
| get_table_lock        | 查询当前mysql服务器是否存在行级锁、表级锁情况                                                                                                          |
| get_table_name        | 根据表注释、表描述搜索所有数据库中对应的表名                                                                                                             |
| get_db_health_index_usage | 获取mysql库的索引使用情况,包含冗余索引情况、性能较差的索引情况、未使用索引且查询时间大于30秒top5情况，支持指定数据库分析|

## prompt 列表
| prompt名称                   | 描述                                                                                                                                 |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------------| 
| analyzing-mysql-prompt     | 这是分析mysql相关问题的提示词       |
| query-table-data-prompt    | 这是通过调用工具查询表数据的提示词，描述可以为空，空时则会初始化为mysql数据库数据查询助手  |

## 使用说明

### SSE 方式

- 使用 uv 启动服务

将以下内容添加到你的 mcp client 工具中，例如cursor、cline等

mcp json 如下
````
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
````

修改.env 文件内容,将数据库连接信息修改为你的数据库连接信息
```
# MySQL数据库配置
MYSQL_HOST=192.168.xxx.xxx
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
# MYSQL_DATABASE=a_llm  # 可选：如果不指定则可以访问所有数据库
MYSQL_ROLE=admin
```

启动命令
```
# 下载依赖
uv sync

# 启动
uv run server.py
```

### STDIO 方式 

将以下内容添加到你的 mcp client 工具中，例如cursor、cline等

mcp json 如下
```
{
  "mcpServers": {
      "operateMysql": {
        "isActive": true,
        "name": "operateMysql",
        "command": "uv",
        "args": [
          "--directory",
          "G:\\python\\mysql_mcp\\src",  # 这里需要替换为你的项目路径
          "run",
          "server.py",
          "--stdio"
        ],
        "env": {
          "MYSQL_HOST": "192.168.xxx.xxx",
          "MYSQL_PORT": "3306",
          "MYSQL_USER": "root",
          "MYSQL_PASSWORD": "root",
          // "MYSQL_DATABASE": "a_llm",  // 可选：如果不指定则可以访问所有数据库
          "MYSQL_ROLE": "admin"
       }
    }
  }
}    
```

## 个性扩展工具
1. 在handles包中新增工具类，继承BaseHandler，实现get_tool_description、run_tool方法

2. 在__init__.py中引入新工具即可在server中调用

## 跨数据库操作示例

现在你可以：

1. **查看所有数据库**：
```
使用get_databases工具查看所有可用的数据库
```

2. **跨数据库查询**：
```sql
SELECT * FROM database1.table1 
UNION ALL 
SELECT * FROM database2.table1;
```

3. **指定数据库操作**：
```sql
USE database_name;
SELECT * FROM table_name;
```

4. **跨数据库表结构查询**：
```
使用get_table_desc工具查询：database1.table1,database2.table2
```

## 工具调用示例
1. 创建新表以及插入数据 prompt格式如下
```
# 任务
   在database_name数据库中创建一张组织架构表，表结构如下：部门名称，部门编号，父部门，是否有效。
# 要求
 - 表名：t_admin_rms_zzjg
 - 字段要求：字符串类型使用'varchar(255)'，整数类型使用'int'，浮点类型使用'float'，日期时间类型使用'datetime'，布尔类型使用'boolean'，文本类型使用'text'，大文本类型使用'longtext'，大整数类型使用'bigint'，大浮点类型使用'double'
 - 表头需要包含主键字段，序号XH varchar(255)
 - 表必须包含这些固定字段在最后：创建人-CJR varchar(50)，创建时间-CJSJ datetime，修改人-XGR varchar(50)，修改时间-XGSJ datetime
 - 字段命名使用工具返回内容
 - 常用字段需要索引
 - 每个字段需要注释，表需要注释
 - 创建完成后生成5条真实数据记录
```

2. 根据表注释查询数据，prompt如下
```
查询用户信息表中张三的数据
```

3. 分析慢SQL，prompt如下
```
select * from database_name.t_jcsjzx_hjkq_cd_xsz_sk xsz
left join database_name.t_jcsjzx_hjkq_jcd jcd on jcd.cddm = xsz.cddm 
根据当前索引情况，查看执行计划并以markdown格式提供优化建议，包括表索引状态、执行详情、优化建议
```

4. 分析SQL死锁问题，prompt如下
```
update database_name.t_admin_rms_zzjg set sfyx = '0' where xh = '1' 卡住了，请分析原因
```

5. 分析健康状态 prompt如下
```
检查当前MySQL的健康状态
```

6. 跨数据库查询示例
```
查询database1和database2中所有用户表的数据
```



