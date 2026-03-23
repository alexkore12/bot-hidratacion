#!/bin/bash
# Deploy script for bot-hidratacion
# Usage: ./deploy.sh [environment]
# Environments: development, staging, production

set -euo pipefail

ENVIRONMENT="${1:-development}"
PROJECT_NAME="bot-hidratacion"
DOCKER_IMAGE="alexkore12/${PROJECT_NAME}:latest"

echo "🚀 Deploying ${PROJECT_NAME} to ${ENVIRONMENT}"

# Load environment variables
if [ -f ".env.${ENVIRONMENT}" ]; then
    export $(cat ".env.${ENVIRONMENT}" | grep -v '^#' | xargs)
    echo "✅ Loaded environment from .env.${ENVIRONMENT}"
fi

# Build Docker image
echo "📦 Building Docker image..."
docker build -t "${DOCKER_IMAGE}" .

# Run health check before deployment
echo "🏥 Running health check..."
python3 health_check.py

# Deploy based on environment
case "${ENVIRONMENT}" in
    production)
        echo "🏭 Deploying to production..."
        docker-compose -f docker-compose.prod.yaml up -d
        ;;
    staging)
        echo "🧪 Deploying to staging..."
        docker-compose up -d
        ;;
    development)
        echo "🧑‍💻 Deploying to development..."
        docker-compose up -d
        ;;
    *)
        echo "❌ Unknown environment: ${ENVIRONMENT}"
        exit 1
        ;;
esac

echo "✅ Deployment complete!"
echo "🌐 Application running at http://localhost:8080"