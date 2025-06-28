# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Docker-based Google Cloud Emulator wrapper that extends the official `google-cloud-cli` Docker image with initialization hooks. It allows automatic execution of setup scripts when emulator containers start, inspired by LocalStack's initialization mechanism.

## Architecture

### Core Components

- **Dockerfile**: Builds on `gcr.io/google.com/cloudsdktool/google-cloud-cli:x.y.z-emulators`, adds uv package manager and Python dependencies
- **entrypoint.sh**: Main orchestration script that starts emulators, waits for readiness, sets environment variables, and executes initialization hooks
- **pyproject.toml**: Defines Python dependencies for Google Cloud client libraries (Pub/Sub, Spanner, Firestore, etc.)

### Initialization Hook System

The container supports a hook-based initialization system:
- Scripts placed in `/docker-entrypoint-init.d/ready.d/` are executed after the emulator is ready
- Supports both shell scripts (`.sh`) and Python scripts (`.py`)
- Python scripts are executed using `uv run` with pre-installed Google Cloud client libraries
- Environment variables are automatically set via `gcloud beta emulators <type> env-init`

### Health Check Mechanism

- Health check monitors `/tmp/init-completed` file
- The `/tmp/init-completed` file is created by the entrypoint script after all initialization hooks have completed successfully
- Only reports healthy after initialization hooks complete
- Ensures proper startup ordering for dependent services
- If initialization hooks fail, the file is not created and the container remains unhealthy

## Development Commands

### Building and Testing Examples

```bash
# Build the Docker image
docker build -t google-cloud-emulator-docker .

# Test Pub/Sub topic creation example
docker compose -f examples/create_pubsub_topic/compose.yaml up -d --wait

# Check created topic
curl http://localhost:8085/v1/projects/test-project/topics

# Clean up after testing
docker compose -f examples/create_pubsub_topic/compose.yaml down
```

### Linting and Code Quality

```bash
# Lint Dockerfile
hadolint Dockerfile

# Lint shell script
shellcheck entrypoint.sh
```

### Local Development

```bash
# Create a compose.yaml and initialization script files in your example directory
# Navigate to your example directory
cd examples/<YOUR_EXAMPLE_DIRECTORY>

# Build the Docker image
docker compose build

# Start the emulator
docker compose up -d --wait

# Verify the expected results
# View logs if needed
docker compose logs -f <SERVICE_NAME>

# Stop and clean up
docker compose down -v
```

## Supported Emulator Types

This project supports the following emulator types, following Google's official base images:

- **Pub/Sub**: `--emulator=pubsub`
- **Firestore**: `--emulator=firestore`
- **Bigtable**: `--emulator=bigtable`
- **Spanner**: `--emulator=spanner`
- **Datastore**: `--emulator=datastore`

Each emulator is built using Google's official Cloud SDK base image (`gcr.io/google.com/cloudsdktool/google-cloud-cli`), ensuring the latest features and security updates are included.

## Example Usage Pattern

```yaml
# compose.yaml
services:
  emulator:
    # for user
    # image: ghcr.io/yumemi-inc/google-cloud-emulator:latest
    # for development
    build: 
      context: ../../ # /path/to/google-cloud-emulator-docker
      dockerfile: Dockerfile # /path/to/google-cloud-emulator-docker/Dockerfile
    command:
      - --emulator=pubsub
      - --port=8085
    volumes:
      - ./init.d/:/docker-entrypoint-init.d/ready.d/
```

## Testing Strategy

- **Integration tests**: Start real emulators and verify initialization hooks work
- **CI pipeline**: Tests Dockerfile linting, shell script validation, and end-to-end functionality
- **Health check validation**: Ensures proper timing between initialization and health reporting
