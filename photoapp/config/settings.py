from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic import computed_field, validator

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class DBConfig(BaseModel):
    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: str 

    # Generate url base of postgres settings
    # NOTE: Pydantic > 2.0.0 way (not supported in Pydantic V1)
    @computed_field
    @property
    def url(self) -> PostgresDsn:
        return f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'

    # NOTE: Older way (Pydantic V1), also validator is deprecated in pydantic v2
    # url: PostgresDsn = None
    # @validator("url", always=True)
    # def composite_url(cls, v, values, **kwargs):
    #     user = values['postgres_user']
    #     password = values['postgres_password']
    #     host = values['postgres_host']
    #     port = values['postgres_port']
    #     database = values['postgres_db']
    #     return f'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}'

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    # Required by Alembic to automatically generate names for constraints, indexes etc..
    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class Settings(BaseSettings):
    # Nested env variables
    model_config = SettingsConfigDict(
        # second overloads first
        env_file=(".env-template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    app: AppConfig = AppConfig()
    db: DBConfig


settings = Settings()
