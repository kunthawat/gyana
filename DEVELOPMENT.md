# Development

## Setup

- Install python deps with `poetry install`
  - You need to manually update the `psycopg2` dependency to `psycopg2-binary`
    for the initial install.
- Install node deps with `yarn`
- Setup local variables in .env file
- Run local Postgres with Postgres.app https://postgresapp.com/
- Run local Redis with Redis.app https://jpadilla.github.io/redisapp/

## Run

- `just dev`
- `just celery`
- `yarn dev-watch`
