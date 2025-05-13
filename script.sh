#!/bin/sh
# Give permission with chmod +x script.sh

echo "Starting Youtube Transcript Pod app..."
gunicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload