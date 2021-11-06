FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

COPY Pipfile.lock Pipfile ./
RUN pip install pipenv && \
    pipenv install

COPY . ./

CMD pipenv run alembic upgrade head && \
    pipenv run uvicorn --host=0.0.0.0 app.main:app
