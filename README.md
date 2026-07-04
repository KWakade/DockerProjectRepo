# Docker Compose Learning Project

## Overview

This project demonstrates a simple Flask web application integrated with PostgreSQL and pgAdmin using Docker Compose.

The application allows:

- Adding users through a web interface
- Storing user data in PostgreSQL
- Viewing database contents through pgAdmin
- Retrieving user data using a REST API

This project was created as part of a Docker learning journey focused on:

- Docker Images
- Docker Containers
- Docker Networking
- Dockerfiles
- Environment Variables
- Docker Compose

---

## Project Structure

DockerProjectRepo/

├── app.py

├── requirements.txt

├── Dockerfile

├── D_App_Postgres_Pgadmin.yml

└── templates/

      └── index.html

---

## Application Components

### Flask Application

Provides:

- Web UI
- POST operation (/adduser)
- GET operation (/users)

Runs inside a Docker container.

---

### PostgreSQL

Database used to store user records.

Database:

userdb

User:

postgres

---

### pgAdmin

Web-based PostgreSQL administration tool.

Used for:

- Creating database objects
- Running SQL queries
- Verifying inserted records

---

## Solution Architecture

Browser

↓

Flask Container

↓

PostgreSQL Container

↑

↓

pgAdmin Container

All containers communicate over the Docker Compose network.

---

## Flask Application Features

### Add User (POST)

Web Page:

http://<server-ip>:5000

User submits:

- Username
- Email

Flask inserts the record into PostgreSQL.

---

### Get Users (GET)

Endpoint:

http://<server-ip>:5000/users

Returns:

[
  {
    "id": 1,
    "username": "Karan",
    "email": "karan@example.com"
  }
]

---

## Dockerfile

The Flask application image is built using:

- Python 3.12
- Flask
- psycopg2-binary

Key concepts demonstrated:

- Base Images
- WORKDIR
- COPY
- RUN
- EXPOSE
- CMD

Build image:

docker build -t python:v6 .

---

## Docker Compose

The Compose file creates:

1. PostgreSQL Container
2. pgAdmin Container
3. Flask Application Container

Key concepts demonstrated:

- Multi-container deployment
- Service-to-service communication
- Environment Variables
- Automatic Network Creation
- Port Mapping

---

## Environment Variables

### PostgreSQL

POSTGRES_USER=postgres

POSTGRES_PASSWORD=Password123

POSTGRES_DB=userdb

### Flask

DB_NAME=userdb

DB_USER=postgres

DB_PASSWORD=Password123

DB_HOST=postgres

DB_PORT=5432

### pgAdmin

PGADMIN_DEFAULT_EMAIL=admin@demo.com

PGADMIN_DEFAULT_PASSWORD=Password123

---

## Create PostgreSQL Table

Connect to PostgreSQL using pgAdmin and execute:

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100)
);

---

## Running the Project

### Build Flask Image

docker build -t python:v6 .

### Start Containers

docker compose -f D_App_Postgres_Pgadmin.yml up -d

### Verify Containers

docker ps

---

## Access URLs

### Flask Application

http://<server-ip>:5000

### pgAdmin

http://<server-ip>:8080

Email:
admin@demo.com

Password:
Password123

---

## Docker Concepts Practiced

- Docker Installation
- Docker Images
- Docker Containers
- Docker Networks
- Docker Volumes (Future Enhancement)
- Dockerfile Creation
- Environment Variables
- Container Port Mapping
- Multi-Container Applications
- Docker Compose

---

## Future Improvements

- Add Docker Volumes for PostgreSQL persistence
- Use Docker Compose build feature
- Add Health Checks
- Add Nginx Reverse Proxy
- Move secrets to .env file
- Deploy on Kubernetes

---

## Learning Objective

The goal of this project is to understand how a Flask application, PostgreSQL database and pgAdmin can be containerized and managed using Docker Compose while following real-world deployment practices.
