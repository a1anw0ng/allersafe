#!/bin/bash
# Startup script for FastAPI backend deployment

# Get PORT from environment variable, default to 8000 if not set
PORT=${PORT:-8000}

# Start uvicorn server
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
