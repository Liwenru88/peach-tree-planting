import asyncio
from typing import List, Dict, Optional, Any
from pydantic import BaseSettings, AnyHttpUrl, SecretStr


class Settings(BaseSettings):
    __doc__ = "开发环境配置"

    # 跨域设置 验证 list包含任意http url
    BACKEND_CORS_ORIGINS: List = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:8080"
    ]

    MOTOR_URI: str = "mongodb://10.10.100.100:27017"  # mongodb://user:password@localhost:27017
    MONGODB_USER_DB_NAME: str = "ptp_prod"  # 用户数据库

    # REDIS 配置
    APP_REDIS_URI: str = "redis://10.10.100.100:6379/0"  # redis://:password@localhost:6379/0

    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"

    DEV_ENV: bool = True


settings = Settings(_env_file=".env")
