#!/bin/bash
# Script to package Lambda functions for deployment

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LAMBDA_DIR="$SCRIPT_DIR"
BUILD_DIR="$SCRIPT_DIR/build"
OUTPUT_ZIP="$SCRIPT_DIR/lambda_package.zip"

echo "Building Lambda deployment package..."

# Clean previous build
rm -rf "$BUILD_DIR"
rm -f "$OUTPUT_ZIP"

# Create build directory
mkdir -p "$BUILD_DIR"

# Copy Lambda function files
echo "Copying Lambda functions..."
cp "$LAMBDA_DIR"/*.py "$BUILD_DIR/"

# Install dependencies
echo "Installing dependencies..."
if [ -f "$LAMBDA_DIR/requirements.txt" ]; then
    pip install -r "$LAMBDA_DIR/requirements.txt" -t "$BUILD_DIR" --upgrade
fi

# Create zip package
echo "Creating deployment package..."
cd "$BUILD_DIR"
zip -r "$OUTPUT_ZIP" . -q

# Clean up
cd "$SCRIPT_DIR"
rm -rf "$BUILD_DIR"

echo "Lambda package created: $OUTPUT_ZIP"
echo "Package size: $(du -h $OUTPUT_ZIP | cut -f1)"
