FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY alembic alembic/
COPY app app/
COPY alembic.ini ./

EXPOSE 8000

CMD alembic upgrade head && \
    uvicorn --host=0.0.0.0 app.main:app
