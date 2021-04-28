# Development

## Setup

- Install python deps with `poetry install`
- Install node deps with `yarn`
- Setup local variables in .env file
- Run local Postgres with Postgres.app https://postgresapp.com/
- Run local Redis with Redis.app https://jpadilla.github.io/redisapp/
- Run migrations `python manage.py migrate`
  - You will need a database `gyana`

There is a bug with `psycopg2` building on MacOS, due to outdated package
`django-heroku`. After the install fails the first time, run:

```
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2
```

And then run the install again. See for details:
https://stackoverflow.com/questions/26288042/error-installing-psycopg2-library-not-found-for-lssl

## Develop

Commands:

- `just dev`
- `just dev-celery`
- `yarn dev-watch`

Create a new CRUDL Django app with `just startapp`.
