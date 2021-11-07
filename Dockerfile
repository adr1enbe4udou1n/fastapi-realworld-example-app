FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Pipfile.lock Pipfile ./
RUN pip install pipenv && \
    pipenv install --dev --deploy --system

COPY alembic alembic/
COPY app app/
COPY alembic.ini Pipfile Pipfile.lock ./

EXPOSE 8000

CMD pipenv run alembic upgrade head && \
    pipenv run uvicorn --host=0.0.0.0 app.main:app
