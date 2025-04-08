#!/bin/bash

# Script to run Jobberwocky tests

SERVICE_NAME="jobberwocky-api"

echo "Checking if Docker service '$SERVICE_NAME' is running..."

if docker compose ps | grep -q "$SERVICE_NAME"; then
  echo "Container is running. Running tests inside Docker..."
  docker compose exec $SERVICE_NAME pytest tests/
else
  echo "Container not found. Running tests locally..."

  if ! command -v pytest &> /dev/null; then
    echo "pytest is not installed. Please run: pip install pytest"
    exit 1
  fi

  pytest tests/
fi

