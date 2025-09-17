# Medical xAI Web App Backend

## Stack
- FastAPI
- PostgreSQL
- Docker Compose

## Structure
- `app/api`: API endpoints (predict, upload, patient, explain, auth)
- `app/schemas`: Pydantic schemas
- `app/models`: ORM models (to be implemented)
- `app/services`: Business logic (to be implemented)
- `app/auth`: Auth logic (to be implemented)

## Dev
```bash
docker-compose up --build
```
