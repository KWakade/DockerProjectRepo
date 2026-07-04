# Docker Flask PostgreSQL Demo

## Overview

This repository is part of a Docker learning project where a simple Flask web application connects to a PostgreSQL database running inside a Docker container.

The current demo architecture is intentionally simple:

- Flask application runs locally on the laptop
- PostgreSQL runs as a Docker container on the Ubuntu lab VM
- pgAdmin runs as a Docker container on the Ubuntu lab VM
- PostgreSQL and pgAdmin communicate using a custom Docker network
- Flask connects to PostgreSQL using database connection details defined by the learner/environment

This project is mainly created to understand:

- Docker basics
- Docker images
- Docker containers
- Docker networking
- PostgreSQL container setup
- pgAdmin container setup
- Flask to PostgreSQL connectivity
- GET and POST flow between frontend, Flask, and database
- Environment variable usage through `.env`
- Keeping sensitive configuration out of Git using `.gitignore`

## Important Note About Configuration

This README is written as a reusable template.

Do not directly reuse fixed usernames, passwords, database names, hostnames, or ports without reviewing them first.

Create your own `.env` file or hardcode values only for lab/demo purposes as per your need.

The `.env` file should not be committed to GitHub because it can contain sensitive details such as database username, password, pgAdmin login, and connection information.

A reference `.env.example` file can be committed to the repository to show which values are required.

## Demo Architecture

```text
Laptop
│
├── Flask Application running locally
│   ├── app.py
│   └── templates/
│       └── index.html
│
└── Connects to PostgreSQL running on Ubuntu lab VM

Ubuntu Lab VM
│
└── Docker Network
    │
    ├── PostgreSQL Container
    │   ├── POSTGRES_DB
    │   ├── POSTGRES_USER
    │   └── POSTGRES_PASSWORD
    │
    └── pgAdmin Container
        ├── PGADMIN_DEFAULT_EMAIL
        └── PGADMIN_DEFAULT_PASSWORD
```

## Technologies Used

- Python
- Flask
- PostgreSQL
- pgAdmin
- Docker
- Docker Network
- Environment variables
- Git / GitHub

## Project Structure

```text
DockerProjectRepo/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env.example
├── templates/
│   └── index.html
└── README.md
```

Example files/folders that may exist during learning:

```text
DockerProjectRepo/
│
├── D_App_Postgres_Pgadmin.yaml
└── dockercomposeproject/
    └── docker-compose.yaml
```

Note:

- `.env` should be created locally and ignored by Git.
- `.env.example` can be used as a reference template.
- Docker Compose work can be kept in a separate folder while learning.
- Later, Docker Compose changes can be pushed to a new branch in the same repository or moved to a separate repository based on project scope.

## Environment Variable Reference

Create a local `.env` file based on the below reference.

```env
# Flask application database connection configuration
# If Flask is running on the laptop and PostgreSQL is running inside Ubuntu lab VM,
# DB_HOST should be the IP address of the Ubuntu lab VM.
# If Flask runs inside the same Docker network later, DB_HOST can be the PostgreSQL container name.
DB_HOST=<postgres_host_or_lab_vm_ip_here>
DB_PORT=<postgres_port_here>
DB_NAME=<database_name_here>
DB_USER=<postgres_username_here>
DB_PASSWORD=<postgres_password_here>

# Flask Configuration
FLASK_APP=<your_application_filename_here_eg_app.py>
FLASK_ENV=<name_appdeployment_name_here>
```

## .gitignore Reference

Make sure `.env` is added to `.gitignore`.

```gitignore
.env
__pycache__/
*.pyc
```

## Docker Network Setup

Create a custom Docker network so that PostgreSQL and pgAdmin containers can communicate with each other.

```bash
docker network create <network_name_here>
```

Example:

```bash
docker network create demo-net
```

## PostgreSQL Container Setup

Run PostgreSQL container using values from your own environment.

Template:

```bash
docker run -d \
  --name <postgres_container_name_here> \
  --network <docker_network_name_here> \
  -e POSTGRES_DB=<database_name_here> \
  -e POSTGRES_USER=<postgres_username_here> \
  -e POSTGRES_PASSWORD=<postgres_password_here> \
  -p <host_port_here>:5432 \
  postgres:latest
```

What happens:

- PostgreSQL image gets downloaded if it is not already available locally
- PostgreSQL container starts
- Database is created based on `POSTGRES_DB`
- PostgreSQL listens on container port `5432`
- Host port mapping allows the Flask app running outside Docker to connect to PostgreSQL

## pgAdmin Container Setup

Run pgAdmin container using your own values.

Template:

```bash
docker run -d \
  --name <pgadmin_container_name_here> \
  --network <docker_network_name_here> \
  -e PGADMIN_DEFAULT_EMAIL=<pgadmin_email_here> \
  -e PGADMIN_DEFAULT_PASSWORD=<pgadmin_password_here> \
  -p <host_port_here>:80 \
  dpage/pgadmin4
```

What happens:

- pgAdmin image gets downloaded if it is not already available locally
- pgAdmin container starts
- pgAdmin can be accessed from browser using the mapped host port
- pgAdmin can connect to PostgreSQL using the PostgreSQL container name when both containers are on the same Docker network

## Configure pgAdmin

Open pgAdmin in browser.

```text
http://<lab_vm_ip_or_localhost>:<pgadmin_host_port>
```

Login using the email and password configured for pgAdmin.

Add a new PostgreSQL server connection:

```text
Name: <any_display_name_here>
Host: <postgres_container_name_here>
Port: 5432
Username: <postgres_username_here>
Password: <postgres_password_here>
```

Note:

- When pgAdmin and PostgreSQL are connected to the same Docker network, use the PostgreSQL container name as the host.
- When Flask is running on the laptop and PostgreSQL is running on the Ubuntu lab VM, use the Ubuntu lab VM IP address as `DB_HOST` in the Flask configuration.

## Create Users Table

Open pgAdmin Query Tool and run:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100)
);
```

## Flask Application Setup

Install Python dependencies on the laptop where Flask is running.

```bash
pip install flask psycopg2-binary
```

Or install using `requirements.txt` if available:

```bash
pip install -r requirements.txt
```

Start the Flask application:

```bash
python app.py
```

Access the Flask application from browser:

```text
http://localhost:<flask_port>
```

## POST Operation Flow

The POST operation is used to insert user details from the web page into PostgreSQL.

```text
Browser
  ↓
Flask Web Application
  ↓
POST /adduser
  ↓
PostgreSQL Container
  ↓
Record Inserted
```

Validation:

```sql
SELECT * FROM users;
```

## GET Operation Flow

The GET operation is used to fetch records from PostgreSQL and show them as JSON output.

```text
Browser
  ↓
GET /users
  ↓
Flask Web Application
  ↓
SELECT * FROM users
  ↓
PostgreSQL Container
  ↓
JSON Response
```

Expected JSON format:

```json
[
  {
    "id": 1,
    "username": "<inserted_username_here>",
    "email": "<inserted_email_here>"
  }
]
```

## End-to-End Demo Flow

```text
Browser Tab 1
    │
    ▼
Flask Web Application
http://localhost:<flask_port>
    │
    │ POST /adduser
    │ GET /users
    ▼
PostgreSQL Container
<database_name_here>
    ▲
    │
    │ Docker Network
    │
pgAdmin Container
http://<lab_vm_ip_or_localhost>:<pgadmin_host_port>
    │
    ▼
SELECT * FROM users;
```

## Learning Status

Current phase:

- Flask app running locally on laptop
- PostgreSQL running as Docker container on Ubuntu lab VM
- pgAdmin running as Docker container on Ubuntu lab VM
- Database validation through pgAdmin
- POST operation tested from Flask web page
- GET operation tested using browser JSON output

Next learning phase:

- Learn Docker Compose
- Move PostgreSQL and pgAdmin container configuration to `docker-compose.yaml`
- Keep Docker Compose practice in a separate folder such as `dockercomposeproject`
- Later decide whether to push Docker Compose work to a new branch in the same repo or create a separate repo

## Repository Status

Work in progress.

This repository is part of my Docker and DevOps learning journey.
