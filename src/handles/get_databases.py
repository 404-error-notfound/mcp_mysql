from typing import Dict, Any, Sequence

from mcp import Tool
from mcp.types import TextContent

from .base import BaseHandler
from handles import (
    ExecuteSQL
)

class GetDatabases(BaseHandler):
    name = "get_databases"
    description = (
        "获取MySQL服务器上所有可用的数据库列表（排除系统数据库）"
    )

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "include_system": {
                        "type": "boolean",
                        "description": "是否包含系统数据库（information_schema, performance_schema, mysql, sys），默认为false"
                    }
                }
            }
        )

    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """获取所有可用的数据库列表

        参数:
            include_system (bool, 可选): 是否包含系统数据库，默认为false

        返回:
            list[TextContent]: 包含查询结果的TextContent列表
            - 返回数据库名称列表
            - 结果以CSV格式返回
        """
        try:
            include_system = arguments.get("include_system", False)
            execute_sql = ExecuteSQL()

            sql = "SELECT SCHEMA_NAME as database_name FROM information_schema.SCHEMATA"
            
            if not include_system:
                sql += " WHERE SCHEMA_NAME NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')"
            
            sql += " ORDER BY SCHEMA_NAME;"

            return await execute_sql.run_tool({"query": sql})

        except Exception as e:
            return [TextContent(type="text", text=f"执行查询时出错: {str(e)}")] 