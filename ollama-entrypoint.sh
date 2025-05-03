#!/bin/bash

set -e

# Start Ollama server in background
echo "🟢 Starting Ollama server..."
ollama serve &

# Wait a few seconds to allow the server to boot
sleep 3

# Check if OLLAMA_MODEL is set
if [ -z "$OLLAMA_MODEL" ]; then
  echo "❌ OLLAMA_MODEL not defined in environment. Please set it in .env or docker-compose.yml"
  exit 1
fi

# Pull the model (will also load it)
echo "⬇️  Pulling and loading model: $OLLAMA_MODEL"
ollama run "$OLLAMA_MODEL"

# Wait forever so the container doesn't exit
echo "✅ Ollama is running and model is ready: $OLLAMA_MODEL"
wait
