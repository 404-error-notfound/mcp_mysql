from typing import Dict, Any, Sequence

from mcp import Tool
from mcp.types import TextContent

from .base import BaseHandler
from handles import (
    ExecuteSQL
)


class GetTableName(BaseHandler):

    name = "get_table_name"
    description = (
        "根据表注释、表描述搜索所有数据库中对应的表名"
    )

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "要搜索的表中文注释关键词"
                    },
                    "database": {
                        "type": "string",
                        "description": "可选：指定要搜索的数据库名称，如果不指定则搜索所有数据库"
                    }
                },
                "required": ["text"]
            }
        )

    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
            """根据表的注释搜索数据库中的表名

            参数:
                text (str): 要搜索的表中文注释关键词
                database (str, 可选): 指定要搜索的数据库名称

            返回:
                list[TextContent]: 包含查询结果的TextContent列表
                - 返回匹配的表名、数据库名和表注释信息
                - 结果以CSV格式返回，包含列名和数据
            """
            try:
                if "text" not in arguments:
                    raise ValueError("缺少查询语句")

                text = arguments["text"]
                database = arguments.get("database")

                execute_sql = ExecuteSQL()

                sql = "SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_COMMENT "
                sql += "FROM information_schema.TABLES WHERE TABLE_COMMENT LIKE '%{}%'".format(text)
                
                # 如果指定了数据库，则只搜索该数据库
                if database:
                    sql += f" AND TABLE_SCHEMA = '{database}'"
                
                # 排除系统数据库
                sql += " AND TABLE_SCHEMA NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')"
                sql += ";"
                
                return await execute_sql.run_tool({"query": sql})

            except Exception as e:
                return [TextContent(type="text", text=f"执行查询时出错: {str(e)}")]