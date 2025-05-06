# Book_manager
intelligent book management system
# Problem Statement:
    You are tasked with creating an intelligent book management system using Python,
    a locally running Llama3 generative AI model, and cloud infrastructure.
    The system should allow users to add, retrieve, update, and delete books from a PostgreSQL database,
    generate summaries for books using the Llama3 model,
    and provide book recommendations based on user preferences. Additionally, the system should manage user reviews and generate rating and review summaries for books. The system should be accessible via a RESTful API and deployed on cloud.

## Tech stack
    Tech Stack

    FastAPI – Web framework

    PostgreSQL – Relational database

    Redis – Caching layer

    Ollama – Local LLM model server

    Docker + Docker Compose – Containerization

## Setup Instructions
    git clone https://github.com/DevSujeet/Book_manager.git
    cd Book_manager

## Configure environment variables

    Update the .env file if needed.
    Defaults should work for local Docker development.

    Make sure DEVELOPMENT_DATABASE_HOST=db if running in Docker.
    Use DEVELOPMENT_DATABASE_HOST=localhost only for local non-Docker testing.

##  Build and run services
    docker-compose up --build
    
    This command will:
    Build the FastAPI app image
    Pull PostgreSQL, Redis, and Ollama images
    Start all containers
## Stopping and Cleaning Up
    to stop all services:
    docker-compose down
    ------
    To remove volumes as well:
    docker-compose down --volumes --remove-orphans
## Accessing the Services
    Service	URL
    FastAPI	http://localhost:8000
    PostgreSQL	localhost:5432
    Redis	localhost:6379
    Ollama API	http://localhost:11434

# API Docs
    You can access the FastAPI Swagger UI at:
        http://localhost:8000/docs#

## Ollama Entrypoint Script
    The ollama-entrypoint.sh script is used to start the Ollama model server and load the specified model automatically when the container starts.

## Testing
    update .env
    "DEVELOPMENT_DATABASE_HOST=localhost" only for local non-Docker testing.

    Run to test
    pytest tests/

##  docker commands
    docker-compose down --volumes --remove-orphans
    docker-compose build --no-cache
    docker-compose up --force-recreate
    ---or---
    docker-compose down --volumes --remove-orphans
    docker-compose up --build
