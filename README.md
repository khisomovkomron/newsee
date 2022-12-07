# MIGRATIONS

- make aerich init -t tortoise_conf.TORTOISE_ORM
- make aerich init-db
- add new changes to models
- make aerich migrate
- make aerich upgrade/downgrade