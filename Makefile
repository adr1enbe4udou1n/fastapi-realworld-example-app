run:
	uvicorn app.main:app --reload
migrate:
	alembic upgrade head
rollback:
	alembic downgrade -1
seed:
	python app/seed.py
fresh:
	alembic downgrade -1
	alembic upgrade head
migrations:
	alembic revision --autogenerate -m "$(name)"
format:
	ruff format --check app tests alembic
lint:
	ruff check app tests alembic
	mypy app tests
