#!/bin/bash

# Weather Monitor Agent - Pub/Sub Triggered Deployment Script
# This script deploys the weather agent as a Pub/Sub triggered Cloud Function

set -e

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-advance-river-238200}"
REGION="${GCP_REGION:-us-west2}"
FUNCTION_NAME="weather-monitor-agent-pubsub"
TOPIC_NAME="weather-agent-trigger"
RUNTIME="python311"
MEMORY="256MB"
TIMEOUT="60s"

echo "🌤️ Deploying Weather Monitor Agent (Pub/Sub) to GCP..."

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

# Create Pub/Sub topic if it doesn't exist
echo "📢 Creating Pub/Sub topic..."
gcloud pubsub topics create $TOPIC_NAME --quiet || echo "Topic already exists"

# Deploy the Cloud Function
echo "🚀 Deploying Cloud Function..."
gcloud functions deploy $FUNCTION_NAME \
    --runtime=$RUNTIME \
    --trigger-topic=$TOPIC_NAME \
    --memory=$MEMORY \
    --timeout=$TIMEOUT \
    --region=$REGION \
    --entry-point=weather_monitor_agent_pubsub \
    --source=. \
    --no-gen2 \
    --set-env-vars="OPENAI_API_KEY=$OPENAI_API_KEY,OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY,EMAIL_SENDER=$EMAIL_SENDER,EMAIL_PASSWORD=$EMAIL_PASSWORD,EMAIL_RECIPIENT=$EMAIL_RECIPIENT,WEATHER_CITY=$WEATHER_CITY,GCP_PROJECT_ID=$PROJECT_ID,GCP_REGION=$REGION"

echo "✅ Cloud Function deployed successfully!"

# Display function info
echo "🔗 Function name: $FUNCTION_NAME"
echo "📢 Pub/Sub topic: $TOPIC_NAME"
echo "📍 Region: $REGION"

echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Test the function by publishing a message:"
echo "   gcloud pubsub topics publish $TOPIC_NAME --message='{\"triggered_by\":\"runtime\",\"message\":\"test\"}'"
echo "2. Monitor logs: gcloud functions logs read $FUNCTION_NAME --region=$REGION"
echo "3. From your runtime, publish messages to: projects/$PROJECT_ID/topics/$TOPIC_NAME" 