## Mini Book Store

A backend RESTful API for a book store system built with FastAPI and Postgre SQL.

This project demonstates authentication, CRUD operations, Dockerized development and CI/CD integration using GitHub Actions.

## 📌 Description

This project is designed as a learning-oriented backend system that simulates a simple book store.

It provides APIs for managing books and users, along with authentication using JWT.

The goal of this project is to practice:

    - Backend architecture desgin
    - API development with FastAPI
    - Database interaction using SQLAlchemy
    - Containerization with Docker
    - CI/CD pipeline setup

## 🚀 Features

- JWT Authentication (Access & Refresh Token)
- User management
- Book CRUD environment
- Dockerized environment
- Environment-based configuration
- Automated testing with Pytest
- CI pipeline with GitHub Actions

## 🛠️ Tech Stack

- Backend: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Validation: Pydantic
- AuthenticationL JWT
- Containerization: Docker, Docker Compose
- Testing: Pytest
- CI/CD: GitHub Actions

## 📂 Project Structure
    app/
    |--main.py
    |--core/
    |--models/
    |--routers/
    |--schemas/
    |--services/

## ⚙️ Setup & Installation

1. Clone repository

git@github.com:LeHoangG-Dev/mini-book-store.git
cd mini-book-store

2. Create environment file

Create a .env.dev and .env.test for testing in the root directory (You can see the key in .env.dev.example and .env.test.example)

3. Run with Docker (Docker must be installed in host)

docker compose build
docker compose up -d

4. Access API

Swagger UI:

http://localhost:80/docs

## 🧪 Running Tests

Run tests using Docker:

docker compose -f docker-compose.test.yml run --rm app pytest -v

## 🔐 Environment Variables

# ORM
DB_USER : Database user
DB_NAME : Database name
DB_PASSWORD: Database password

DB_TEST_NAME: Database test name (If testing)

# Database
POSTGRES_USER: Postgre user
POSTGRES_DB: Postgre database name
POSTGRES_PASSWORD: Postgre password

# HOST
DB_HOST: Database host
DB_PORT: Database port

# Security
ALGORITHM: JWT algorithm
SECRET_KEY: JWT secret key

# Tokens
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS

# App
DEBUG: Debug mode

# Admin
ADMIN_EMAIL: admin account
ADMIN_PASSWORD: admin password

## 📡 API Endpoints 

## 🤝 Contributing

1. Fork the repostiry
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

## Demo

## 📄 License

This project is for learning and demonstration purposes.