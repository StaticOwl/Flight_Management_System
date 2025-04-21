#!/bin/bash

export MSYS_NO_PATHCONV=1  # Workaround for Git Bash on Windows

LOG_FILE="setup.log"
exec > >(tee -a "$LOG_FILE") 2>&1  # Log output to setup.log

echo "--------------------"
echo "...Starting Setup..."
echo "--------------------"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Function to load environment variables
load_env() {
    ENV=${1:-dev}  # Default to 'dev' if no argument is given
    if [ -d "$SCRIPT_DIR/envs" ] && ls "$SCRIPT_DIR/envs"/"$ENV".env 1> /dev/null 2>&1; then
        for env_file in "$SCRIPT_DIR/envs"/$ENV.env; do
            export $(grep -v '^#' "$env_file" | xargs)
        done
    else
        echo "Error: No .env files found in the envs folder!"
        exit 1
    fi
}

# Function to setup Podman & Network
setup_podman() {
    echo "Checking Podman installation..."
    if ! command -v podman &> /dev/null; then
        echo "Error: Podman is not installed. Please install Podman before running this script."
        exit 1
    fi

    echo "Checking if Podman is running..."
    if ! podman info &> /dev/null; then
        podman machine init
        podman machine start
        if ! podman info &> /dev/null; then
            echo "Try running: podman system connection list"
            exit 1
        fi
    fi

    echo "Creating Podman network if not exists..."
    podman network exists flight_network || podman network create flight_network
}

# Function to setup PostgreSQL Database
setup_database() {
    echo "Setting up PostgreSQL container..."
    if podman ps -a --format "{{.Names}}" | grep -q "flight_db"; then
        podman stop flight_db && podman rm flight_db && podman volume rm flight_pgdata
    fi

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
}

# Function to seed database
seed_database() {
    echo "Applying database schema..."
    podman exec -it flight_db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f ddl/init_ddl/MAKE_TABLES.sql
    podman exec -it flight_db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f ddl/init_ddl/DDL.sql
}

# Function to deploy backend
deploy_backend() {
    echo "Deploying Flask backend..."
    if podman ps -a --format "{{.Names}}" | grep -q "flight_service"; then
        podman stop flight_service && podman rm flight_service
        podman rmi flight_backend
    fi

    podman build -t flight_backend .
    podman run -d --name flight_service --network flight_network -p 5000:5000 \
      -e POSTGRES_USER="$POSTGRES_USER" \
      -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
      -e POSTGRES_DB="$POSTGRES_DB" \
      -e POSTGRES_HOST="$POSTGRES_HOST" \
      -e POSTGRES_PORT="$POSTGRES_PORT" \
      -e DATABASE_URL="postgresql+psycopg2://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB"  \
      flight_backend
}


check_status() {
    echo "Checking running containers..."
    podman ps
}

case "$1" in
    "")
        echo "No argument provided, running full setup..."
        load_env
        setup_podman
        setup_database
        seed_database
        deploy_backend
        check_status
        ;;
    podman)
        load_env
        setup_podman
        ;;
    db)
        load_env
        setup_database
        ;;
    seed)
        load_env
        seed_database
        ;;
    backend)
        load_env
        deploy_backend
        ;;
    status)
        check_status
        ;;
    full)
        load_env
        setup_podman
        setup_database
        seed_database
        deploy_backend
        check_status
        ;;
    *)
        echo "Usage: $0 {podman|db|seed|backend|status|full}"
        exit 1
        ;;
esac

echo "Setup complete! Your application is running at: http://localhost:5000"
