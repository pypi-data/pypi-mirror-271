# api-auth

## Install

~~~shell
cp .env.example .env
# now edit it
vim .env

alembic upgrade head
~~~


## Usage

~~~
# register
http POST http://localhost:8000/auth/users/ username=me@example.com password=secret

# simple auth (session)
http -f POST http://localhost:8000/auth/login username=me@example.com password=secret

# get token
http -f POST http://localhost:8000/auth/token username=me@example.com password=secret
~~~

## Developer cheatsheet
### Alembic cheatsheet
~~~
alembic revision --autogenerate -m "some desc"
alembic upgrade head
alembic current
~~~