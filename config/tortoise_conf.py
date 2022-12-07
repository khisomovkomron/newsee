from settings import APPS_MODELS

TORTOISE_ORM = {
    "connections": {"default": 'postgres://postgres:123abcDEF@localhost/NewseeDatabase'},
    "apps": {
        "models": {
            "models": APPS_MODELS,
            "default_connection": "default",
        }
    },
}