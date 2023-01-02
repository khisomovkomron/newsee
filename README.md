# MIGRATIONS

- make aerich init -t tortoise_conf.TORTOISE_ORM
- make aerich init-db
- add new changes to models


- from setting in pycharm select poetry environment 
- make poetry install 
- make poetry shell to get access to installed packages


- configure DB settings in main.py and tortoise_conf.py
- change postgres password if required
- make aerich upgrade
- make aerich migrate
