TORTOISE_ORM = {
    "connections": {"default": 'postgres://postgres:123abcDEF@localhost/NewseeDatabase'},
    "apps": {
        "models": {
            "models": ["database_pack.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}