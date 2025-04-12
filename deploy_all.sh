#!/bin/bash

set -e

PROJECT_ID="duke-chatbot-project"
REGION="us-central1"
REPO="duke-chatbot-repo"

BACKEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/backend:v1"
FRONTEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO}/frontend:v1"

echo "🔨 Building backend..."
docker buildx build --platform linux/amd64 -t $BACKEND_IMAGE -f Dockerfile.backend --push .

echo "🚀 Deploying backend to Cloud Run..."
gcloud run deploy backend \
  --image $BACKEND_IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --set-secrets=GEMINI_API_KEY=GEMINI_API_KEY:latest,\
GOOGLE_API_KEY=GOOGLE_API_KEY:latest,\
DUKE_API_AUTH_TOKEN=DUKE_API_AUTH_TOKEN:latest,\
DUKE_EVENTS_API_URL=DUKE_EVENTS_API_URL:latest,\
DUKE_FUTURE_EVENTS_API_URL=DUKE_FUTURE_EVENTS_API_URL:latest,\
DUKE_GENERAL_API_URL=DUKE_GENERAL_API_URL:latest

echo "🔨 Building frontend..."
docker buildx build --platform linux/amd64 -t $FRONTEND_IMAGE -f Dockerfile.frontend --push .

echo "🚀 Deploying frontend to Cloud Run..."
gcloud run deploy frontend \
  --image $FRONTEND_IMAGE \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 256Mi

echo "✅ Deployment complete!"