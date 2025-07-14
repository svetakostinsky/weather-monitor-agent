# Weather Monitor Agent

A Python-based AI agent that monitors daily weather and sends status emails. Built for deployment on Google Cloud Platform.

## 🌤️ Features

- **Daily Weather Monitoring**: Checks weather data for your specified location
- **AI-Powered Insights**: Uses OpenAI to generate weather analysis and recommendations
- **Email Notifications**: Sends formatted weather reports via email
- **GCP Integration**: Deployed as a Cloud Function with Cloud Scheduler
- **Modular Architecture**: Easy to extend and customize

## 🚀 Quick Start

### 1. **Clone or navigate to the project directory:**
   ```bash
   cd ~/Documents/projects/ai-agent
   ```

### 2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

### 3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys and configuration
   ```

### 5. **Test locally:**
   ```bash
   # Test weather data retrieval
   python app.py --test
   
   # Test email sending
   python app.py --email-test
   
   # Run full weather check and email
   python app.py
   ```

## 📋 Required API Keys & Configuration

Create a `.env` file with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4
TEMPERATURE=0.7
MAX_TOKENS=1000

# Weather API Configuration
OPENWEATHER_API_KEY=your_openweather_api_key_here
WEATHER_CITY=your_city_name
WEATHER_COUNTRY_CODE=US

# Email Configuration
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_RECIPIENT=your_email@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# GCP Configuration
GCP_PROJECT_ID=your_gcp_project_id
GCP_REGION=us-central1

# Agent Configuration
AGENT_NAME=Weather Monitor Agent
SYSTEM_PROMPT=You are a weather monitoring agent that checks daily weather and sends status emails.

# Application Configuration
DEBUG=false
LOG_LEVEL=INFO
```

## 🏗️ Project Structure

```
ai-agent/
├── app.py                 # Local development entry point
├── main.py               # GCP Cloud Function entry point
├── deploy.sh             # GCP deployment script
├── agent/
│   ├── __init__.py
│   ├── core.py           # Main agent functionality
│   └── tools.py          # Weather and email tools
├── config/
│   ├── __init__.py
│   └── settings.py       # Configuration management
├── utils/
│   └── __init__.py
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md            # This file
```

## ☁️ GCP Deployment

### Prerequisites
1. Install Google Cloud CLI: `gcloud`
2. Authenticate: `gcloud auth login`
3. Set your project: `gcloud config set project YOUR_PROJECT_ID`

### Deploy to GCP
```bash
# Make deploy script executable
chmod +x deploy.sh

# Set environment variables
export GCP_PROJECT_ID="your-project-id"
export OPENAI_API_KEY="your-openai-key"
export OPENWEATHER_API_KEY="your-weather-key"
export EMAIL_SENDER="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export EMAIL_RECIPIENT="your-email@gmail.com"
export WEATHER_CITY="your-city"

# Deploy
./deploy.sh
```

### What Gets Deployed
- **Cloud Function**: `weather-monitor-agent` - Runs the weather check
- **Cloud Scheduler**: `weather-daily-report` - Triggers daily at 8:00 AM
- **Environment Variables**: All API keys and configuration

## 📧 Email Format

The agent sends emails with:
- Current weather conditions
- Temperature, humidity, wind speed
- Sunrise/sunset times
- AI-generated insights and recommendations
- Daily activity suggestions

## 🔧 Customization

### Change Weather Location
Update `WEATHER_CITY` and `WEATHER_COUNTRY_CODE` in your `.env` file.

### Modify Email Schedule
Edit the cron expression in `deploy.sh`:
```bash
--schedule="0 8 * * *"  # Daily at 8:00 AM
```

### Add More Weather Data
Extend `agent/tools.py` to include additional weather metrics.

## 🧪 Testing

### Local Testing
```bash
# Test weather data retrieval
python app.py --test

# Test email functionality
python app.py --email-test

# Run full workflow
python app.py
```

### GCP Testing
```bash
# Get function URL
gcloud functions describe weather-monitor-agent --region=us-central1 --format='value(httpsTrigger.url)'

# Test manually
curl -X POST YOUR_FUNCTION_URL
```

## 📊 Monitoring

### View Logs
```bash
# Cloud Function logs
gcloud functions logs read weather-monitor-agent --region=us-central1

# Cloud Scheduler logs
gcloud scheduler jobs list
```

### Check Status
```bash
# Function status
gcloud functions describe weather-monitor-agent --region=us-central1

# Scheduler status
gcloud scheduler jobs describe weather-daily-report --location=us-central1
```

## 🔐 Security Notes

- Use Gmail App Passwords for email authentication
- Store API keys securely in GCP Secret Manager for production
- Enable Cloud Audit Logs for monitoring
- Use IAM roles with minimal required permissions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details 