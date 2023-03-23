# MIGRATIONS

- make aerich init -t tortoise_conf.TORTOISE_ORM
- make aerich init-db
- add new changes to models


- from setting in pycharm select poetry environment 
- make poetry install 
- make poetry shell to get access to installed packages


- configure DB settings in main.py and tortoise_conf.py
- change postgres password if required
- aerich upgrade: This command applies any outstanding migrations to your database.
- aerich downgrade: This command rolls back the most recent migration applied to your database.
- aerich migrate -m "create_users_table": This command creates a new migration with the specified name (create_users_table in this example). You can then edit the migration file to define the changes to make to your database schema.
- aerich heads: This command lists the most recent applied migrations.
