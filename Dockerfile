FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

COPY Pipfile.lock Pipfile ./
RUN pip install pipenv && \
    pipenv install --dev --deploy --system

COPY . ./

CMD pipenv run alembic upgrade head && \
    pipenv run uvicorn --host=0.0.0.0 app.main:app
