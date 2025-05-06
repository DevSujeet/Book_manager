# Book_manager
intelligent book management system
# Problem Statement:
    You are tasked with creating an intelligent book management system using Python,
    a locally running Llama3 generative AI model, and cloud infrastructure.
    The system should allow users to add, retrieve, update, and delete books from a PostgreSQL database,
    generate summaries for books using the Llama3 model,
    and provide book recommendations based on user preferences. Additionally, the system should manage user reviews and generate rating and review summaries for books. The system should be accessible via a RESTful API and deployed on cloud.

# setting up local postgress in docker
    docker run --name local-postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=ibm_db \
    -p 5432:5432 \
    -d postgres

## Running Ollama + DeepSeek on MacBook M3
    # Install Ollama if not installed
    brew install ollama

    #Option A: Run it once in terminal
    # to start it once
    /opt/homebrew/opt/ollama/bin/ollama serve

    Option B (recommended): Start as background service
    brew services start ollama

    # Pull and Run DeepSeek model
    ollama run deepseek-coder:1.3b

    # Test it (optional)
    curl http://localhost:11434/api/generate -d '{
    "model": "deepseek-coder:1.3b",
    "prompt": "Summarize this book content in 150 words and classify it as horror, romance, action, or thriller:\n\nA dark forest...",
    "stream": false
    }'

# How to STOP or RESTART Ollama
    brew services stop ollama

# Restart Ollama service
    brew services restart ollama

# Check if Ollama is running
    curl http://localhost:11434



## Reruning docker
    docker-compose down --volumes --remove-orphans
    docker-compose build --no-cache
    docker-compose up --force-recreate
    ---or---
    docker-compose down --volumes --remove-orphans
    docker-compose up --build