run:
	uvicorn app.main:app --reload
migrate:
	alembic upgrade head
rollback:
	alembic downgrade -1
migrations:
	alembic revision --autogenerate -m "$(name)"
format:
	autoflake --remove-all-unused-imports --remove-unused-variables --recursive --in-place app tests alembic
	black app tests alembic
	isort app tests alembic
lint:
	flake8 app tests
	autoflake --remove-all-unused-imports --remove-unused-variables --recursive app tests alembic
	black --check --diff app tests alembic
	isort --check-only app tests alembic
	mypy app tests
