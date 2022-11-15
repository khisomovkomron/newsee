# PART I 
## start app, learn working with fastapi framework
- fastapi 
  - models
  - routers
  - pydantic
  - sqlalchemy
  - orm 
- ROUTERS - AUTH, ADDRESS, TO-DO, USER
- AUTH
  - /auth/create/user
  - /auth/token
- ADDRESS
  - /address/ - CRD
  - /address/{address_id} - CRUD
  - /address/user/ 
- TO-DO
  - /todos/
  - /todos/user
  - /todos/{todo_id}
- USER
  - /users/
  - /users/users/{user_id}
  - /users/user
  - /users/user/password
- ALEMBIC
  - add Table 
  - add columns
  - add constraints
- POSTGRES
  - create table
  - select, update, insert
- DOCKER
  - dockerfile
  - docker-compose

# PART II
## consolidate acquired knowledge, add new endpoints, learn nested bodies - DEADLINE 1.12.2022
- nested bodies
- ROUTER - PROFILE, ARCHIVE
- PROFILE
  - /info - gather all info of a user into one endpoint - USER, TOKEN, ADDRESS, TODOS- all deleted todos passed in ARCHIVE, 
  all done todos are passed to ARCHIEVE router
- ARCHIEVE
  - /archive/deletes - read all deleted todos of a user
  - /archieve/todos - read all completed todos of a user
  - /archieve - read all deleted and completed todos of a user
  - /archieve/clean - clean an archieve of a user
- new columsa and endpoints to to-do
  - /todos/titles
  - column - createdat, createdby, modifiedat, modifiedby
- read asyncio, asynchttp
- read design pattern

# PART III 
## new microservice, broker, interaction of microservice, deployment
- deployment in AWS
- broker
- microservices interaction
- asynchronous requests
- add more apis to new service and new service
- second microservice will be on Tortoise ORM


# LEARNING

In order to avoid vacancies in Github contribuiton, I will take notes in 
this README file. Dates and topics will be included

### 14.11.2022

- learning asynchronous programming with Python
- asyncio, httpx
- asynchronous contextmanager "async with"