from config.settings import APPS_MODELS

TORTOISE_ORM = {
    "connections": {"default": 'postgres://postgres:1234@localhost/NewseeDatabase'},
    "apps": {
        "models": {
            "models": APPS_MODELS,
            "default_connection": "default",
        }
    },
}