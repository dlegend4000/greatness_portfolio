#!/bin/bash

# Navigate to project directory
cd /Users/emmanuelkaribiye/greatness_portfolio

# Fetch latest changes and reset to origin/main
git fetch && git reset origin/main --hard

# Stop containers to prevent out of memory issues during build
docker compose -f docker-compose.prod.yml down

# Build and start containers in detached mode
docker compose -f docker-compose.prod.yml up -d --build

echo "Deployment completed successfully!"