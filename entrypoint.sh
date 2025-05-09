#!/bin/bash
set -euo pipefail

INIT_DIR="/docker-entrypoint-init.d"

EMULATOR_TYPE=""
PORT=""
ADDITIONAL_ARGS=()

# show_usage displays the usage information
function show_usage() {
  echo "Usage: $0 --emulator=<emulator_type> --port=<port> [additional args...]"
  echo "Example: $0 --emulator=pubsub --port=8085 --project=my-project"
  exit 1
}

# check arguments
if [ "$#" -eq 0 ]; then
  show_usage
fi

# parse command-line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --emulator=*)
      EMULATOR_TYPE="${1#*=}"
      shift
      ;;
    --port=*)
      PORT="${1#*=}"
      shift
      ;;
    -h|--help)
      show_usage
      ;;
    *)
      # 残りの引数はすべて追加引数として扱う
      ADDITIONAL_ARGS+=("$1")
      shift
      ;;
  esac
done

# check if required arguments are provided
if [ -z "$EMULATOR_TYPE" ] || [ -z "$PORT" ]; then
  echo "Error: Both --emulator and --port are required"
  show_usage
fi

echo "Emulator type: $EMULATOR_TYPE"
echo "Port: $PORT"

# Construct the gcloud command
COMMAND=("gcloud" "beta" "emulators" "$EMULATOR_TYPE" "start" "--host-port=0.0.0.0:$PORT")

# Add any additional arguments
if [ "$#" -gt 0 ]; then
  COMMAND+=("$@")
fi

echo "Executing command: ${COMMAND[*]}"

# Start emulator in background and redirect output
echo "Starting emulator..."
"${COMMAND[@]}" > /proc/1/fd/1 2>&1 &
EMULATOR_PID=$!

# Wait a bit for the emulator to start properly
sleep 5
echo "Emulator started with PID: $EMULATOR_PID"

# Wait for emulator to be ready
until curl -s "http://localhost:${PORT}" > /dev/null; do
  echo "Waiting for emulator to be ready..."
  sleep 5
done
echo "Emulator is ready."

# Set environment variables for connecting to the emulator
echo "Setting up environment variables..."
eval "$(gcloud beta emulators "${EMULATOR_TYPE}" env-init)"
echo "Environment variables set."

# Run ready.d scripts
READY_DIR="${INIT_DIR}/ready.d"
if [ -d "$READY_DIR" ] && [ -n "$(ls -A $READY_DIR 2>/dev/null)" ]; then
  echo "Running ready scripts..."

  for f in "$READY_DIR"/*.sh; do
    if [ -f "$f" ] && [ -x "$f" ]; then
      echo "Running hook: $f"
      "$f"
    elif [ -f "$f" ]; then
      echo "Running hook: $f (with bash)"
      bash "$f"
    fi
  done

  for f in "$READY_DIR"/*.py; do
    if [ -f "$f" ]; then
      echo "Running hook: $f (with python)"
      uv run "$f"
    fi
  done

  echo "Ready scripts completed."
fi

# Create a file to indicate initialization is complete
touch /tmp/init-completed
echo "Initialization completed marker created at /tmp/init-completed"

# Keep the container running by waiting for the emulator process
wait $EMULATOR_PID
