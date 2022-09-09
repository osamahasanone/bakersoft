FROM python:3.10-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/service

COPY pyproject.toml poetry.lock ./
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY --chown=django:django ./app ./
COPY --chown=django:django ./tests ./tests
COPY --chown=django:django pytest.ini ./

USER django
