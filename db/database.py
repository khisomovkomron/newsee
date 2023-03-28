from config.settings import DatabaseConfig

database_config = DatabaseConfig()

SQLALCHEMY_DATABASE_URL = database_config.databse_url
