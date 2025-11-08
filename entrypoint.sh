#!/bin/sh
set -e

CONFIG_DIR=/config
DEFAULT_CONFIG=/app/config/rules.yaml
TARGET_CONFIG=$CONFIG_DIR/rules.yaml

# Ensure the config directory exists
mkdir -p "$CONFIG_DIR"

# Only copy the default if user didn't mount or create their own
if [ ! -f "$TARGET_CONFIG" ]; then
    echo "No user config found, copying default..."
    cp "$DEFAULT_CONFIG" "$TARGET_CONFIG"
    chmod 777 "$TARGET_CONFIG"
fi

# Continue to your main process
exec "$@"
