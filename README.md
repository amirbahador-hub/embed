# embed
![Tests](https://github.com/amirbahador-hub/embed/actions/workflows/tests.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/amirbahador-hub/embed/badge.svg?branch=main)](https://coveralls.io/github/amirbahador-hub/embed?branch=main)

https://www.embed.xyz/ assignment

## RUN IN DEVELOPMENT MODE
install dev requirements
```
pip install requirements.txt
```
Add ENV_NAME KEY to .env
```
DATABASE_URL=psql://postgres:postgres@127.0.0.1:5432/embed_db
ES_HOST=localhost
ES_PORT=9200
ES_AUTH=""
REDIS_LOCATION=redis://localhost:6379
```
run databases
```
docker-compose -f docker-compse.dev.yml up
```

run migrations
```
python manage.py migrate
```
runserver
```bash
python manage.py runserver
```

