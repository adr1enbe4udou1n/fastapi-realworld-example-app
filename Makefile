run:
	uvicorn app.main:app --reload
migrate:
	alembic upgrade head
rollback:
	alembic downgrade -1
migrations:
	alembic revision --autogenerate -m "$(name)"
