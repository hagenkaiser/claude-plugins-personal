#!/bin/bash
# One-time setup: creates a venv with required dependencies
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SKILL_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install -q PyJWT cryptography
    echo "Done."
else
    echo "Venv already exists at $VENV_DIR"
fi
