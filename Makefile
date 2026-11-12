.PHONY: up down logs test train
up:
	docker compose up --build
down:
	docker compose down
logs:
	docker compose logs -f
test:
	cd backend && pytest -q
train:
	cd backend && python -m app.solver.train --iterations 100000
