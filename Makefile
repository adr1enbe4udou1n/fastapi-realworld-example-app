run:
	uvicorn app.main:app --reload
migrate:
	alembic upgrade head
rollback:
	alembic downgrade -1
migrations:
	alembic revision --autogenerate -m "$(name)"
format:
	black app tests
	isort app tests
	flake8 app tests
lint:
	black --check app tests --diff
	isort --check-only app tests
	flake8 app tests
	mypy app tests
analyse:
	mypy app tests
