# Books Review Service

A FastAPI-based service for managing books and reviews, featuring authentication, recommendations, and automated testing.

## Features

- User registration and JWT-based authentication
- CRUD operations for books and reviews
- Recommendations endpoint based on weighted average ratings
- Dockerized application with Docker Compose
- Environment variables via `.env`
- Linting with Pylint
- Automated tests with `pytest` and coverage

## Requirements

- Docker & Docker Compose
- Python 3.10+

## Setup

1. Clone the repository:   
```
git clone git@github.com:olisvalue/books-review-service.git
cd books-review-service
```
2. Create an .env file (see .env.example):
```
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```   

3. Build and run with Docker Compose:
```
docker-compose up --build
```

The API will be available at http://localhost:8000.

## Testing
Run
```pytest```