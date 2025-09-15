from typing import Dict, Any, Sequence

from mcp import Tool
from mcp.types import TextContent

from .base import BaseHandler
from handles import (
    ExecuteSQL
)


class GetTableDesc(BaseHandler):
    name = "get_table_desc"
    description = (
        "根据表名搜索所有数据库中对应的表结构，支持多表查询"
    )

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "table_names": {
                        "type": "string",
                        "description": "要查询的表名，多个表名用逗号分隔，可以使用 database.table_name 格式指定数据库"
                    }
                },
                "required": ["table_names"]
            }
        )

    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """根据表名搜索数据库中对应的表结构

        参数:
            table_names (str): 要查询的表名，多个表名用逗号分隔

        返回:
            list[TextContent]: 包含查询结果的TextContent列表
            - 返回表的字段信息，包括字段名、类型、是否为空、键信息、默认值和注释
            - 结果以CSV格式返回，包含列名和数据
            - 多个表的结果以"---"分隔
        """
        try:
            if "table_names" not in arguments:
                raise ValueError("缺少表名参数")

            table_names = arguments["table_names"]
            execute_sql = ExecuteSQL()

            # 分割表名
            tables = [name.strip() for name in table_names.split(',')]
            results = []

            for table in tables:
                try:
                    # 检查是否包含数据库名
                    if '.' in table:
                        database, table_name = table.split('.', 1)
                        sql = f"SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, COLUMN_COMMENT "
                        sql += f"FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{database}' AND TABLE_NAME = '{table_name}' "
                        sql += "ORDER BY ORDINAL_POSITION;"
                    else:
                        # 如果没有指定数据库，搜索所有数据库（排除系统数据库）
                        sql = f"SELECT TABLE_SCHEMA, COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, COLUMN_COMMENT "
                        sql += f"FROM information_schema.COLUMNS WHERE TABLE_NAME = '{table}' "
                        sql += "AND TABLE_SCHEMA NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys') "
                        sql += "ORDER BY TABLE_SCHEMA, ORDINAL_POSITION;"

                    result = await execute_sql.run_tool({"query": sql})
                    results.extend(result)

                except Exception as e:
                    results.append(TextContent(type="text", text=f"查询表 '{table}' 时出错: {str(e)}"))

            return results

        except Exception as e:
            return [TextContent(type="text", text=f"执行查询时出错: {str(e)}")]