#!/bin/bash

export MSYS_NO_PATHCONV=1  # Workaround for Git Bash on Windows

LOG_FILE="setup.log"
exec > >(tee -a "$LOG_FILE") 2>&1  # Log output to setup.log

echo "--------------------"
echo "...Starting Setup..."
echo "--------------------"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Check if Podman is installed
if ! command -v podman &> /dev/null; then
  echo "Error: Podman is not installed. Please install Podman before running this script."
  exit 1
fi

# Check if Podman is running
if ! podman info &> /dev/null; then
  echo "Error: Podman is not running!"
  podman machine init
  podman machine start
  if ! podman info &> /dev/null; then
    echo "Try running: podman system connection list"
    echo "If no connection is active, try: podman machine init && podman machine start"
    exit 1
  fi
fi

ENV=${1:-dev}

# Load environment variables from .env files
if [ -d "$SCRIPT_DIR/envs" ] && ls "$SCRIPT_DIR/envs"/"$ENV".env 1> /dev/null 2>&1; then
  for env_file in "$SCRIPT_DIR/envs"/$ENV.env; do
    # shellcheck disable=SC2046
    export $(grep -v '^#' "$env_file" | xargs)
  done
else
  echo "Error: No .env files found in the envs folder!"
  exit 1
fi

DATABASE_URL="postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"


# Create Podman network if it doesn’t exist
echo "Creating network (if not exists)..."
podman network exists flight_network || podman network create flight_network

# Stop & remove old PostgreSQL container if it exists
if podman ps -a --format "{{.Names}}" | grep -q "flight_db"; then
  echo "Stopping and removing existing PostgreSQL container..."
  podman stop flight_db && podman rm flight_db && podman volume rm flight_pgdata
fi

# Start PostgreSQL container
echo "Starting PostgreSQL container..."
podman run -d --name flight_db --network flight_network \
  -e POSTGRES_USER="$POSTGRES_USER" \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -e POSTGRES_DB="$POSTGRES_DB" \
  -v flight_pgdata:/var/lib/postgresql/data \
  -v "$SCRIPT_DIR/ddl:/ddl:ro" \
  -p "$POSTGRES_PORT":5432 \
  docker.io/postgres:latest

echo "Waiting for PostgreSQL to be ready..."
sleep 10

# Apply database schema
echo "Applying database seeding..."
podman exec -it flight_db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f ddl/init_ddl/MAKE_TABLES.sql
podman exec -it flight_db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f ddl/init_ddl/DDL.sql

# Stop & remove old Flask container if it exists
if podman ps -a --format "{{.Names}}" | grep -q "flight_service"; then
  echo "Stopping and removing existing Flask container..."
  podman stop flight_service && podman rm flight_service
  podman rmi flight_backend
fi

# Build the Flask application container
echo "Building the Flask application container..."
podman build -t flight_backend .

# Start Flask container
echo "Starting Flask container..."
podman run -d --name flight_service --network flight_network -p 5000:5000 \
  -e POSTGRES_USER="$POSTGRES_USER" \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -e POSTGRES_DB="$POSTGRES_DB" \
  -e POSTGRES_HOST="$POSTGRES_HOST" \
  -e POSTGRES_PORT="$POSTGRES_PORT" \
  -e DATABASE_URL="$DATABASE_URL"  \
  flight_backend

# Show running containers
echo "Containers running:"
podman ps

echo "Setup complete! Your application is running at: http://localhost:5000"
