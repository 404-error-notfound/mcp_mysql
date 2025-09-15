import os
from dotenv import load_dotenv

def get_db_config():
    """从环境变量获取数据库配置信息

    返回:
        dict: 包含数据库连接所需的配置信息
        - host: 数据库主机地址
        - port: 数据库端口
        - user: 数据库用户名
        - password: 数据库密码
        - database: 数据库名称（可选）
        - role: 数据库角色权限

    异常:
        ValueError: 当必需的配置信息缺失时抛出
    """
    # 加载.env文件
    load_dotenv()

    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE"),  # 现在可以为空
        "role": os.getenv("MYSQL_ROLE", "readonly")  # 默认为只读角色
    }
    
    if not all([config["user"], config["password"]]):
        raise ValueError("缺少必需的数据库配置：用户名和密码")

    return config

def get_db_config_without_database():
    """获取不指定数据库的连接配置
    
    返回:
        dict: 不包含database字段的数据库连接配置
    """
    config = get_db_config()
    # 移除database字段，这样就可以连接到MySQL服务器而不指定特定数据库
    connection_config = {k: v for k, v in config.items() if k not in ["database", "role"]}
    return connection_config, config["role"]

# 定义角色权限
ROLE_PERMISSIONS = {
    "readonly": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "USE"],  # 只读权限
    "writer": ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN", "INSERT", "UPDATE", "DELETE", "USE"],  # 读写权限
    "admin": [
        # 查询权限
        "SELECT", "SHOW", "DESCRIBE", "EXPLAIN", 
        # 数据操作权限
        "INSERT", "UPDATE", "DELETE", "REPLACE", "LOAD",
        # 表结构管理权限
        "CREATE", "ALTER", "DROP", "TRUNCATE", "RENAME",
        # 数据库管理权限
        "CREATE DATABASE", "DROP DATABASE", "ALTER DATABASE",
        # 数据库使用权限
        "USE",
        # 索引管理权限
        "CREATE INDEX", "DROP INDEX", "ALTER INDEX",
        # 视图管理权限
        "CREATE VIEW", "DROP VIEW", "ALTER VIEW",
        # 存储过程和函数权限
        "CREATE PROCEDURE", "DROP PROCEDURE", "ALTER PROCEDURE",
        "CREATE FUNCTION", "DROP FUNCTION", "ALTER FUNCTION",
        # 触发器权限
        "CREATE TRIGGER", "DROP TRIGGER",
        # 事件调度器权限
        "CREATE EVENT", "DROP EVENT", "ALTER EVENT",
        # 用户和权限管理
        "CREATE USER", "DROP USER", "ALTER USER", "RENAME USER",
        "GRANT", "REVOKE", "FLUSH", "RESET",
        # 系统管理权限
        "SHUTDOWN", "RELOAD", "LOCK", "UNLOCK", "PROCESS", "SUPER",
        # 备份和恢复相关
        "BACKUP", "RESTORE", "BACKUP_ADMIN", "BINLOG_ADMIN",
        # 复制相关权限
        "REPLICATION SLAVE", "REPLICATION CLIENT", "REPLICATION_SLAVE_ADMIN",
        # 性能调优权限
        "OPTIMIZE", "ANALYZE", "CHECK", "CHECKSUM", "REPAIR",
        # 临时表权限
        "CREATE TEMPORARY TABLES",
        # 文件操作权限
        "FILE", "SELECT INTO OUTFILE", "LOAD DATA",
        # 其他管理权限
        "REFERENCES", "USAGE", "EXECUTE", "BINLOG_ENCRYPTION_ADMIN",
        "CONNECTION_ADMIN", "PERSIST_RO_VARIABLES_ADMIN", "ROLE_ADMIN",
        "SESSION_VARIABLES_ADMIN", "SET_USER_ID", "SYSTEM_USER",
        "SYSTEM_VARIABLES_ADMIN", "XA_RECOVER_ADMIN"
    ]  # 完整的管理员权限
}

def get_role_permissions(role: str) -> list:
    """获取指定角色的权限列表
    
    参数:
        role (str): 角色名称
        
    返回:
        list: 该角色允许执行的SQL操作列表
    """
    return ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS["readonly"])  # 默认返回只读权限