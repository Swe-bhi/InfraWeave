# FastAPI + PostgreSQL Microservice (Dockerized)

A lightweight, containerized microservice built with FastAPI and PostgreSQL, orchestrated using Docker Compose.  
This project demonstrates a clean, production-style setup for building and deploying Python-based APIs with a real database backend.

## Features
- FastAPI backend with modular endpoints
- PostgreSQL database running in a separate container
- Dockerfile + Docker Compose for full environment reproducibility
- CRUD operations:
  - Create user
  - Read all users
  - Read user by ID
- Environment-based configuration for database connectivity
- Lightweight Python 3.11 image

## API Endpoints
- `GET /health` — database connectivity check  
- `GET /users` — fetch all users  
- `GET /user/{id}` — fetch a single user by ID  
- `POST /add-user` — add a new user  

## Running the Service

```bash
docker compose build --no-cache
docker compose up

