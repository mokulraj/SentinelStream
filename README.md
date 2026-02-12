🚀 SentinelStream – FinTech Backend Project

SentinelStream is a FinTech transaction monitoring backend built using FastAPI. It implements secure user authentication and transaction management using modern backend practices.

🔑 Key Features

User Registration & Login

JWT-based Authentication

Secure Password Hashing

Create & Fetch Financial Transactions

Protected APIs with Token Authorization

🛠️ Tech Stack

Backend: FastAPI (Python)

Database: PostgreSQL

ORM: SQLAlchemy (Async)

Authentication: JWT

Server: Uvicorn

▶️ How to Run
uvicorn app.main:app --reload

App runs at:

http://127.0.0.1:8000
📑 API Docs

Swagger UI: http://127.0.0.1:8000/docs

🔐 Authentication Flow

Register user

Login to receive JWT token

Use token in request header:

Authorization: Bearer <token>

Access transaction APIs

🎯 Purpose

This project demonstrates:

Secure FinTech backend development

JWT authentication flow

Async database operations

Real-world API design
