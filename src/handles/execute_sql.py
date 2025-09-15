from typing import Dict, Any, Sequence

from mcp import Tool
from mcp.types import TextContent
from mysql.connector import connect, Error

from config import get_db_config_without_database, get_role_permissions
from .base import BaseHandler


class ExecuteSQL(BaseHandler):
    name = "execute_sql"
    description = (
        "在MySQL数据库上执行SQL，可以访问所有数据库 (multiple SQL execution, separated by ';')"
    )

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要执行的SQL语句，可以包含数据库名称如：USE database_name; 或 SELECT * FROM database_name.table_name;"
                    }
                },
                "required": ["query"]
            }
        )

    def check_sql_permission(self, sql: str, allowed_operations: list) -> bool:
        """检查SQL语句是否有执行权限
        
        参数:
            sql (str): SQL语句
            allowed_operations (list): 允许的操作列表
            
        返回:
            bool: 是否有权限执行
        """
        # 清理和标准化SQL语句
        sql_lines = sql.strip().split('\n')
        
        # 找到第一行非注释的SQL语句
        actual_sql = ""
        for line in sql_lines:
            line = line.strip()
            # 跳过空行和注释行
            if not line or line.startswith('--') or line.startswith('/*'):
                continue
            # 如果行中有 -- 注释，只取注释前的部分
            if '--' in line:
                line = line.split('--')[0].strip()
            if line:
                actual_sql = line
                break
        
        if not actual_sql:
            return False
            
        # 标准化SQL语句
        sql_upper = actual_sql.upper()
        words = sql_upper.split()
        
        if not words:
            return False
        
        # 定义多单词操作的映射
        multi_word_operations = {
            # 数据库操作
            ('CREATE', 'DATABASE'): 'CREATE DATABASE',
            ('DROP', 'DATABASE'): 'DROP DATABASE', 
            ('ALTER', 'DATABASE'): 'ALTER DATABASE',
            # 索引操作
            ('CREATE', 'INDEX'): 'CREATE INDEX',
            ('DROP', 'INDEX'): 'DROP INDEX',
            ('ALTER', 'INDEX'): 'ALTER INDEX',
            # 视图操作
            ('CREATE', 'VIEW'): 'CREATE VIEW',
            ('DROP', 'VIEW'): 'DROP VIEW',
            ('ALTER', 'VIEW'): 'ALTER VIEW',
            # 存储过程操作
            ('CREATE', 'PROCEDURE'): 'CREATE PROCEDURE',
            ('DROP', 'PROCEDURE'): 'DROP PROCEDURE',
            ('ALTER', 'PROCEDURE'): 'ALTER PROCEDURE',
            # 函数操作
            ('CREATE', 'FUNCTION'): 'CREATE FUNCTION',
            ('DROP', 'FUNCTION'): 'DROP FUNCTION',
            ('ALTER', 'FUNCTION'): 'ALTER FUNCTION',
            # 触发器操作
            ('CREATE', 'TRIGGER'): 'CREATE TRIGGER',
            ('DROP', 'TRIGGER'): 'DROP TRIGGER',
            # 事件操作
            ('CREATE', 'EVENT'): 'CREATE EVENT',
            ('DROP', 'EVENT'): 'DROP EVENT',
            ('ALTER', 'EVENT'): 'ALTER EVENT',
            # 用户操作
            ('CREATE', 'USER'): 'CREATE USER',
            ('DROP', 'USER'): 'DROP USER',
            ('ALTER', 'USER'): 'ALTER USER',
            ('RENAME', 'USER'): 'RENAME USER',
            # 临时表
            ('CREATE', 'TEMPORARY'): 'CREATE TEMPORARY TABLES',
            # 复制相关
            ('REPLICATION', 'SLAVE'): 'REPLICATION SLAVE',
            ('REPLICATION', 'CLIENT'): 'REPLICATION CLIENT',
            # 文件操作
            ('SELECT', 'INTO'): 'SELECT INTO OUTFILE',
            ('LOAD', 'DATA'): 'LOAD DATA',
        }
        
        # 检查多单词操作
        if len(words) >= 2:
            two_word_key = (words[0], words[1])
            if two_word_key in multi_word_operations:
                operation = multi_word_operations[two_word_key]
                return operation in allowed_operations
            
            # 特殊处理一些三单词的操作
            if len(words) >= 3:
                if words[0] == 'CREATE' and words[1] == 'TEMPORARY' and words[2] == 'TABLE':
                    return 'CREATE TEMPORARY TABLES' in allowed_operations
                elif words[1] == 'INTO' and words[2] == 'OUTFILE':
                    return 'SELECT INTO OUTFILE' in allowed_operations
                elif words[0] == 'LOAD' and words[1] == 'DATA' and words[2] == 'INFILE':
                    return 'LOAD DATA' in allowed_operations
        
        # 如果不是多单词操作，检查单个单词操作
        single_operation = words[0]
        return single_operation in allowed_operations

    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
       """执行SQL查询语句

          参数:
              query (str): 要执行的SQL语句，支持多条语句以分号分隔

          返回:
              list[TextContent]: 包含查询结果的TextContent列表
              - 对于SELECT查询：返回CSV格式的结果，包含列名和数据
              - 对于SHOW TABLES：返回数据库中的所有表名
              - 对于其他查询：返回执行状态和影响行数
              - 多条语句的结果以"---"分隔

          异常:
              Error: 当数据库连接或查询执行失败时抛出异常
          """
       try:
           if "query" not in arguments:
               raise ValueError("缺少查询语句")

           query = arguments["query"]
           
           # 获取不指定数据库的连接配置和角色权限
           connection_config, role = get_db_config_without_database()
           allowed_operations = get_role_permissions(role)

           with connect(**connection_config) as conn:
               with conn.cursor() as cursor:
                   statements = [stmt.strip() for stmt in query.split(';') if stmt.strip()]
                   results = []

                   for statement in statements:
                       try:
                           # 检查权限
                           if not self.check_sql_permission(statement, allowed_operations):
                               results.append(f"权限不足: 当前角色 '{role}' 无权执行该SQL操作")
                               continue

                           cursor.execute(statement)

                           # 检查语句是否返回了结果集 (SELECT, SHOW, EXPLAIN, etc.)
                           if cursor.description:
                               columns = [desc[0] for desc in cursor.description]
                               rows = cursor.fetchall()

                               # 将每一行的数据转换为字符串，特殊处理None值
                               formatted_rows = []
                               for row in rows:
                                   formatted_row = ["NULL" if value is None else str(value) for value in row]
                                   formatted_rows.append(",".join(formatted_row))

                               # 将列名和数据合并为CSV格式
                               results.append("\n".join([",".join(columns)] + formatted_rows))

                           # 如果语句没有返回结果集 (INSERT, UPDATE, DELETE, etc.)
                           else:
                               conn.commit()  # 只有在非查询语句时才提交
                               results.append(f"查询执行成功。影响行数: {cursor.rowcount}")

                       except Error as stmt_error:
                           # 单条语句执行出错时，记录错误并继续执行
                           results.append(f"执行语句 '{statement}' 出错: {str(stmt_error)}")
                           # 可以在这里选择是否继续执行后续语句，目前是继续

                   return [TextContent(type="text", text="\n---\n".join(results))]

       except Error as e:
           return [TextContent(type="text", text=f"执行查询时出错: {str(e)}")]

