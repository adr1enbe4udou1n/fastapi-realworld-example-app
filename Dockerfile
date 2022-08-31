FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY .venv .venv/
COPY alembic alembic/
COPY app app/
COPY alembic.ini ./

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD alembic upgrade head && \
    uvicorn --host=0.0.0.0 app.main:app --no-access-log
