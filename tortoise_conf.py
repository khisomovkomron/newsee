from config.settings import APPS_MODELS

TORTOISE_ORM = {
    "connections": {"default": 'postgres://postgres:1234@localhost/NewseeDatabase'},
    "apps": {
        "models": {
            "models": ['db.models', 'aerich.models'],
            "default_connection": "default",
        }
    },
}