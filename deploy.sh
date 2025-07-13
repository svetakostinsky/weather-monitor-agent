#!/bin/bash

# Weather Monitor Agent - GCP Deployment Script
# This script deploys the weather agent to Google Cloud Functions

set -e

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-your-project-id}"
REGION="${GCP_REGION:-us-central1}"
FUNCTION_NAME="weather-monitor-agent"
RUNTIME="python311"
MEMORY="256MB"
TIMEOUT="60s"

echo "🌤️ Deploying Weather Monitor Agent to GCP..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Error: Not authenticated with gcloud. Please run 'gcloud auth login' first."
    exit 1
fi

# Set the project
echo "📋 Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Deploy the Cloud Function
echo "🚀 Deploying Cloud Function..."
gcloud functions deploy $FUNCTION_NAME \
    --runtime=$RUNTIME \
    --trigger-http \
    --allow-unauthenticated \
    --memory=$MEMORY \
    --timeout=$TIMEOUT \
    --region=$REGION \
    --entry-point=weather_monitor_agent \
    --source=. \
    --set-env-vars="OPENAI_API_KEY=$OPENAI_API_KEY,OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY,EMAIL_SENDER=$EMAIL_SENDER,EMAIL_PASSWORD=$EMAIL_PASSWORD,EMAIL_RECIPIENT=$EMAIL_RECIPIENT,WEATHER_CITY=$WEATHER_CITY"

echo "✅ Cloud Function deployed successfully!"

# Create Cloud Scheduler job for daily execution
echo "⏰ Creating Cloud Scheduler job..."
gcloud scheduler jobs create http weather-daily-report \
    --schedule="0 8 * * *" \
    --uri="$(gcloud functions describe $FUNCTION_NAME --region=$REGION --format='value(httpsTrigger.url)')" \
    --http-method=POST \
    --location=$REGION

echo "✅ Cloud Scheduler job created successfully!"
echo "📅 Weather reports will be sent daily at 8:00 AM"

# Display function URL
FUNCTION_URL=$(gcloud functions describe $FUNCTION_NAME --region=$REGION --format='value(httpsTrigger.url)')
echo "🔗 Function URL: $FUNCTION_URL"

echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Test the function manually: curl -X POST $FUNCTION_URL"
echo "2. Check Cloud Scheduler: gcloud scheduler jobs list"
echo "3. Monitor logs: gcloud functions logs read $FUNCTION_NAME --region=$REGION" 