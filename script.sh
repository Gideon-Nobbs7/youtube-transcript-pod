#!/bin/sh
# Give permission with chmod +x script.sh

echo "Starting Youtube Transcript Pod app..."
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload