# Weather Monitor Agent - Deployment Guide

## 🚀 Deployment Status: ACTIVE

Your weather monitor agent is successfully deployed to Google Cloud Platform with multiple trigger options.

## 📋 Project Information

- **Project ID**: `advance-river-238200`
- **Region**: `us-west2`
- **Deployment Date**: July 14, 2025

## 🔗 Cloud Functions

### 1. HTTP-Triggered Function (Original)
- **Function Name**: `weather-monitor-agent`
- **URL**: `https://us-west2-advance-river-238200.cloudfunctions.net/weather-monitor-agent`
- **Trigger**: HTTP POST
- **Entry Point**: `weather_monitor_agent`
- **Status**: ✅ ACTIVE

### 2. Pub/Sub-Triggered Function (New)
- **Function Name**: `weather-monitor-agent-pubsub`
- **Pub/Sub Topic**: `weather-agent-trigger`
- **Trigger**: Pub/Sub messages
- **Entry Point**: `weather_monitor_agent_pubsub`
- **Status**: ✅ ACTIVE

## ⏰ Scheduled Execution

- **Cloud Scheduler Job**: `weather-daily-report`
- **Schedule**: Daily at 8:00 AM UTC
- **Target**: HTTP function
- **Status**: ✅ ENABLED

## 🔧 Environment Variables

All environment variables are securely configured:

- `OPENAI_API_KEY`: ✅ Configured
- `OPENWEATHER_API_KEY`: ✅ Configured
- `EMAIL_SENDER`: ✅ Configured
- `EMAIL_PASSWORD`: ✅ Configured
- `EMAIL_RECIPIENT`: ✅ Configured
- `WEATHER_CITY`: ✅ Configured (San Francisco)
- `GCP_PROJECT_ID`: ✅ Configured
- `GCP_REGION`: ✅ Configured

## 🛠️ Integration Options

### Option 1: Direct HTTP Integration
```python
import requests

def trigger_weather_agent(custom_message=None):
    url = "https://us-west2-advance-river-238200.cloudfunctions.net/weather-monitor-agent"
    
    payload = {
        "triggered_by": "runtime_environment",
        "message": custom_message or "Weather check requested"
    }
    
    response = requests.post(url, json=payload)
    return response.json()
```

### Option 2: Pub/Sub Integration (Recommended)
```python
from google.cloud import pubsub_v1
import json

def trigger_weather_agent_via_pubsub(custom_message=None):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("advance-river-238200", "weather-agent-trigger")
    
    message_data = {
        "triggered_by": "runtime_environment",
        "message": custom_message or "Weather check requested"
    }
    
    future = publisher.publish(topic_path, json.dumps(message_data).encode("utf-8"))
    message_id = future.result()
    
    return {"message_id": message_id, "status": "published"}
```

## 📊 Response Format

Both functions return the same JSON response:

```json
{
  "success": true,
  "weather_data": {
    "city": "San Francisco",
    "country": "US",
    "temperature": 16.18,
    "description": "few clouds",
    "humidity": 81,
    "wind_speed": 9.77,
    "pressure": 1014,
    "sunrise": "12:58",
    "sunset": "03:32",
    "timestamp": "2025-07-14 00:47:43"
  },
  "email_result": {
    "success": true,
    "message": "Weather email sent successfully to kostinsky.sveta@gmail.com",
    "timestamp": "2025-07-14 00:47:44"
  },
  "ai_insights": "Subject: Daily Weather Update for San Francisco, US\n\nHello!\n\nHere's your daily weather rundown...",
  "trigger_source": "runtime_environment",
  "custom_message": "Test message from runtime",
  "triggered_at": "2025-07-14 00:47:53",
  "timestamp": "2025-07-14 00:47:53"
}
```

## 🔍 Monitoring & Debugging

### Check Function Logs
```bash
# HTTP function logs
gcloud functions logs read weather-monitor-agent --region=us-west2

# Pub/Sub function logs
gcloud functions logs read weather-monitor-agent-pubsub --region=us-west2
```

### Test Functions
```bash
# Test HTTP function
curl -X POST https://us-west2-advance-river-238200.cloudfunctions.net/weather-monitor-agent

# Test Pub/Sub function
gcloud pubsub topics publish weather-agent-trigger --message='{"triggered_by":"test","message":"test"}'
```

### Check Scheduler Status
```bash
gcloud scheduler jobs list --location=us-west2
```

## 📁 Local Files

### Core Files
- `main.py` - Contains both HTTP and Pub/Sub function entry points
- `agent/` - Core agent logic
- `config/` - Configuration settings
- `utils/` - Utility functions

### Deployment Scripts
- `deploy.sh` - Deploy HTTP-triggered function
- `deploy_pubsub.sh` - Deploy Pub/Sub-triggered function

### Configuration
- `.env` - Environment variables (local only)
- `requirements.txt` - Python dependencies
- `gcp-service-account.json` - Service account credentials

## 🔐 Security Notes

- Environment variables are securely stored in Cloud Functions
- Service account credentials are properly configured
- Functions are accessible via HTTP (can be secured if needed)
- Pub/Sub topic has proper IAM permissions

## 📈 Scaling & Performance

- **Memory**: 256MB per function
- **Timeout**: 60 seconds
- **Max Instances**: 3000 (Pub/Sub function)
- **Concurrent Executions**: Supported

## 🆘 Troubleshooting

### Common Issues
1. **Function not found**: Check function name and region
2. **Authentication errors**: Verify service account permissions
3. **Environment variable errors**: Check .env file and deployment
4. **Pub/Sub errors**: Verify topic exists and permissions

### Useful Commands
```bash
# List all functions
gcloud functions list --region=us-west2

# Describe function
gcloud functions describe weather-monitor-agent --region=us-west2

# Update function
gcloud functions deploy weather-monitor-agent --source=. --region=us-west2

# Delete function (if needed)
gcloud functions delete weather-monitor-agent --region=us-west2 --quiet
```

## 📞 Support

For issues or questions:
1. Check the logs first: `gcloud functions logs read`
2. Test manually: `curl -X POST [function-url]`
3. Verify configuration: Check environment variables
4. Review deployment: Check function status

---
**Last Updated**: July 14, 2025
**Deployment Status**: ✅ ACTIVE
**Backup Location**: `./backup/` 