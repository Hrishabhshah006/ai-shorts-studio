up:
	docker compose up -d

down:
	docker compose down

api:
	cd backend && uvicorn app.main:app --reload --port 8000

worker:
	cd backend && python -m app.workers.main

web:
	cd frontend && npm install && npm run dev

test:
	cd backend && python -m pytest
