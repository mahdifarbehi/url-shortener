run:
	uvicorn main:app --reload --app-dir src

run_tests:
	pytest

run_migrations:
	cd src && alembic upgrade head