from functools import cached_property
from pathlib import Path

from pydantic import ConfigDict, Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationSettings(BaseSettings):
    model_config: ConfigDict = SettingsConfigDict(
        arbitrary_types_allowed=True,
        case_sensitive=False,
        env_file=(".env", ".env.dev"),
    )
    app_name: str = "sqlpile"
    database_name: str = "default"
    memory_database_type: str = "sqlite"
    local_database_type: str = "duckdb"
    app_data_dir: Path = Field(
        default_factory=lambda: Path.home() / ".app_data" / "sqlpile" / "databases"
    )

    # Postgres settings
    postgres_db: str = "postgres"
    postgres_user: str = "user"
    postgres_password: SecretStr = Field(default="password", env="POSTGRES_PASSWORD")
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    database_url: str | None = Field(
        None,
        description="The entire database url. Will overwrite other database settings.",
    )
    is_unlink: bool = False
    cache_timeout: int = 60 * 60 * 24

    @computed_field
    @cached_property
    def memory_uri(self) -> str:
        return f"{self.local_database_type}:///:memory:"

    @computed_field
    @cached_property
    def local_db_uri(self) -> str:
        database_file = self.app_data_dir / f"{self.database_name}.db"
        if self.is_unlink and database_file.exists():
            database_file.unlink(missing_ok=True)
        return f"{self.local_database_type}:///{database_file.absolute()}"

    @computed_field
    @cached_property
    def remote_db_uri(self) -> str:
        if self.database_url:
            return self.database_url
        return f"postgresql://{self.postgres_user}:{self.postgres_password.get_secret_value()}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = ApplicationSettings()
