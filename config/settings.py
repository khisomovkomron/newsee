from pydantic import BaseSettings, Field


class AppConfig(BaseSettings):

    class Config:
        env_file = '.env'
        env_file_encoding = "utf-8"

    project_name: str = Field(env='PROJECT_NAME', default='newsee')
    environment: str = Field(env='ENVIRONMENT', default='development')
    debug: bool = Field(env='DEBUG', cast=bool, default=True)
    server_host: str = Field(env='SERVER_HOST', default='localhost')
    server_port: int = Field(env="SERVER_PORT", cast=int, default='8000')

class DatabaseConfig(BaseSettings):

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    protocol: str = Field(env="POSTGRES_USER")
    database: str = Field(env="POSTGRES_DB")
    username: str = Field(env="POSTGRES_USER")
    password: str = Field(env="POSTGRES_PASSWORD")
    host: str = Field(env="BACKEND_DATABSE_HOST")

    @property
    def database_url(self) -> str:
        return f"{self.protocol}://{self.username}:{self.password}@{self.host}/{self.database}"


class KeysConfig(BaseSettings):

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    secret_key: str = Field(env="SECRET_KEY")
    algorithm: str = Field(env="ALGORITHM", default="HS256")
    newsapikey: str = Field(env="NEWSAPIKEY")
    newsdata: str = Field(env="NEWSDATA")
    alpha_api_key: str = Field(env="ALPHA_API_KEY")
    coinmarketapikey: str = Field(env='COINMARKETAPIKEY')