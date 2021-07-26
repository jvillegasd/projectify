# Projectify

Tecnical test for [Leanware](https://www.leanware.io)


# Run project locally

This project is dockerized, so all you have to do is to type this command line: `docker-compose up -d`

## Environment variables

```
FLASK_PORT=5001

REDIS_URL=
REDIS_PORT=

MONGODB_PORT=
MONGODB_ROOT_USERNAME=
MONGODB_PASSWORD=
MONGODB_SERVER=
MONGODB_DATABASE=
MONGODB_URL=

SALT_ROUNDS=

SECRET_KEY=

BUCKETEER_AWS_ACCESS_KEY_ID=
BUCKETEER_AWS_REGION=
BUCKETEER_AWS_SECRET_ACCESS_KEY=
BUCKETEER_AWS_PUBLIC_URL=
BUCKETEER_BUCKET_NAME=
```

## Report table schema
This is the schema to follow when a user wants to upload a report file

```markdown
| project_id                           | report_date | dedication_percentage |
|--------------------------------------|-------------|-----------------------|
| 290ac198-424f-428b-a63f-6bde2e20d583 | 2/06/2021   | 60.1                  |
| ...                                  | ...         | ...                   |
|                                      |             |                       |
```

## Week days
Week days under ISo standard was handled using Python's library datetime. The method used was `isocalendar()`.
Week days is used for make validations around duplicate reports on the same week.