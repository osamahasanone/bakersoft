# Project Time Management

A Django Rest Framwork simple API for managing multiple projects and users. A project can be splitted into tasks which can be assigned to teams.

## Built With

The below languages, libraries and tools have been used:
* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.mysql.com/)
* [Redis](https://redis.io/)
* [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
* [Django-FSM](https://pypi.org/project/django-fsm/1.6.0/)
* [Pytest](https://docs.pytest.org/en/6.2.x/)
* [Docker](https://www.docker.com/)
* [Swagger](https://swagger.io/)

## Prerequisites

Please make sure that you have Git and Docker installed on you machine.

## Installation

1.  Clone the repo
   
```sh
git clone https://github.com/osamahasanone/bakersoft
```
   
2. Build Docker images and start containers in one command:
   
```sh
docker-compose up -d
```

3. Run tests:

```sh
docker-compose exec web pytest
```

