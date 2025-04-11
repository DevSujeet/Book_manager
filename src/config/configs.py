from contextvars import ContextVar

from typing import Dict, Any
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.constant.constant import DB_ENV_PREFIX, CACHE_ENV_PREFIX

# Context variable for storing dynamic state
_ctx_var: ContextVar[Dict[Any, Any]] = ContextVar("ctx_var", default={})


class _db_settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=DB_ENV_PREFIX,  # Match prefix with your .env file #development_
        env_file='.env',
        populate_by_name=True,  # Use field aliases
        extra='ignore',  # Ignore extra inputs from the .env file
        env_file_encoding='utf-8',
    )

    # Match these aliases to .env field keys
    db_host:str = Field(alias='database_host')
    db_username: str = Field(alias='database_username')
    db_password: str = Field(alias='database_password')
    db_name:str = Field(alias='database_name')
    db_port:str = Field(alias='database_port')
    # db_schema: str = Field(alias='DATABASE_SCHEMA')

    def __init__(self, **kwargs):
        print("📦 Raw incoming values to _db_settings:", kwargs)
        super().__init__(**kwargs)

class CacheSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix=CACHE_ENV_PREFIX,  # Match prefix with your .env file #development_
        env_file='.env',
        populate_by_name=True,  # Use field aliases
        extra='ignore',  # Ignore extra inputs from the .env file
        env_file_encoding='utf-8',
    )

    # Match these aliases to .env field keys
    cache_host:str = Field(alias='cache_host')
    cache_port: str = Field(alias='cache_port')
    cache_password: str = Field(alias='cache_password')
    cache_username: str = Field(alias='cache_username')

    default_ttl: int = 300 #seconds
    # redis_url: str = "redis://user:password@localhost:6379"
    # redis_url: str = "redis://localhost:6379"  # Default Redis URL

    @property
    def cache_url(self) -> str:
        return f"redis://{self.cache_username}:{self.cache_password}@{self.cache_host}:{self.cache_port}"
    