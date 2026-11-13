# Module-5---Fast-API-Development

Task Management API – Module 5 Assessment
Overview

A RESTful Task Management API built with FastAPI, SQLAlchemy, and JWT authentication. Users can register, log in, and manage their own tasks securely.

Features

User registration and login
Password hashing using bcrypt
JWT-based authentication
Create, read, update, and delete (CRUD) tasks
User-specific task ownership
Protected API endpoints
Interactive API documentation with Swagger UI
Technologies Used

Python 3.12
FastAPI
SQLAlchemy
SQLite
Passlib and bcrypt
Python-JOSE (JWT)
Pytest
Installation and Setup

Clone the repository:

bash
git clone YOUR_REPOSITORY_URL
cd 5_14_Module_Assessment
Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate
Install dependencies:

bash
pip install -r requirements.txt
Start the development server:

bash
uvicorn app.main:app --reload
API Documentation

Once the server is running, visit:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
Use Swagger UI to register users, log in, authorize requests, and test API endpoints.

Running Tests

Run the automated test suite with:


bash
pytest tests/ -v
Authentication

The API uses JSON Web Tokens (JWT) to protect endpoints. Users must log in to receive an access token and authenticate before managing their tasks.

Each task is associated with its owner through a foreign key relationship, ensuring users can only access their own tasks.

Design Choices

JWT Authentication: Provides stateless authentication for protected API endpoints.
One-to-Many Relationship: Allows each user to own multiple tasks while keeping task ownership organized.
Password Hashing: Uses bcrypt to securely store passwords rather than storing plain-text credentials.
Project Purpose

This project demonstrates practical skills in building REST APIs, implementing authentication, managing relational databases, creating CRUD functionality, and testing API endpoints using FastAPI.