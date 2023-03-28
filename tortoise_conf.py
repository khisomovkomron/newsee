from config.settings import DatabaseConfig

database_config = DatabaseConfig()

TORTOISE_ORM = {
    "connections": {"default": database_config.database_url},
    "apps": {
        "models": {
            "models": ['db.models', 'aerich.models'],
            "default_connection": "default",
        }
    },
}