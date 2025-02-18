#!/bin/bash
set -eux

# Define the target directory
TARGET_DIR="public"

# Find and replace in all files inside the public folder
find "$TARGET_DIR" -type f -exec sed -i -e 's|href="."|href="core.html"|g' -e 's|href="./"|href="core.html"|g' {} +

echo "Global find and replace completed in all files inside $TARGET_DIR."
