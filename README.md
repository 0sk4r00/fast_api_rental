# Rental office
Application is about booking items which everyone can add to database. App use authorization.
 
## Run app
```
poetry shell
poetry install
docker-compose up -d
uvicorn app.main:app --port 8001 --reload
```

## Stack
- docker
- postgres
- fastapi
- sqlalchemy
- authorization 
