run:
	uvicorn app.main:app --reload
migrate:
	alembic upgrade head
rollback:
	alembic downgrade -1
migrations:
	alembic revision --autogenerate -m "$(name)"
format:
	autoflake --remove-all-unused-imports --remove-unused-variables --recursive --in-place app tests
	black app tests
	isort app tests
lint:
	flake8 app tests
	autoflake --remove-all-unused-imports --remove-unused-variables --recursive app tests
	black --check --diff app tests
	isort --check-only app tests
	mypy app tests
