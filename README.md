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

# ENV file content

    #postgresql+asyncpg://username:password@hostname:port/databasename
    DEVELOPMENT_DATABASE_DRIVERNAME=postgresql
    DEVELOPMENT_DATABASE_USERNAME=postgres  
    DEVELOPMENT_DATABASE_PASSWORD=postgres  
    # Use "db" when running via Docker Compose (container service name)
    # Use "localhost" for local testing without Docker
    DEVELOPMENT_DATABASE_HOST=db 
    DEVELOPMENT_DATABASE_NAME=ibm_db 
    DEVELOPMENT_DATABASE_PORT=5432



    DEVELOPMENT_CACHE_DRIVERNAME=redis
    DEVELOPMENT_CACHE_USERNAME=username@dev_database
    DEVELOPMENT_CACHE_PASSWORD=pass123!
    DEVELOPMENT_CACHE_HOST=redis 
    DEVELOPMENT_CACHE_NAME=vodafone
    DEVELOPMENT_CACHE_PORT=6379

    # azure app registration
    CLIENT_ID=b564554a-xxxx-4583-xxxx-3b70daxxxx82
    CLIENT_SECRET=87w8Q~_xxxxxxxxxxxx-KRjzkSnjUmNdSstqoNdrA
    TENANT_ID=1452a59b-1e9c-xxxxx-xxxxx-fb10b415xxxxx
    REDIRECT_URI=http://localhost:8000/auth/callback

    # OLLAMA_URL=http://localhost:11434
    OLLAMA_URL=http://ollama:11434
    OLLAMA_MODEL=deepseek-coder:1.3b #mistral:7b-instruct

# Authentication
Used Microsoft Entra ID for Authentication.
step to try it out.
    1. Create an app registration and get the above required value
    or 
    will share mine if required.

    2. open fast api docs : http://localhost:8000/docs#
    3. open in a new tab: http://localhost:8000/auth/login
        a. enter MS cred and get the token.
        b. copy id token
        c. tap the authorize button in top right corner and auth using the id token copied earlier.
        d. test the protected route
    4. Note: Authenication dependency is not integrated to all the route as of now, consider protect route for demo.