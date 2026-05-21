#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Path to the uv-managed venv
VENV_PATH="$DIR/.venv/bin/activate"

if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
else
    echo "Error: Virtual environment not found at $VENV_PATH"
    echo "Please run 'uv sync' first."
    exit 1
fi

# Configuration
export WHISPER_MODEL="large-v3-turbo"
export WHISPER_DEVICE="cpu"
export WHISPER_COMPUTE_TYPE="int8"
export WHISPER_PORT=9000

echo "Starting Local Whisper API server..."
exec python server.py
