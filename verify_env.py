#!/usr/bin/env python3
"""
Verify environment variables for Weather Monitor Agent
"""

import os
from dotenv import load_dotenv

def verify_env():
    """Verify all required environment variables are set."""
    print("🔍 Verifying Environment Variables...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Required variables to check
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API Key',
        'MODEL_NAME': 'OpenAI Model Name',
        'TEMPERATURE': 'OpenAI Temperature',
        'MAX_TOKENS': 'OpenAI Max Tokens',
        'OPENWEATHER_API_KEY': 'OpenWeather API Key',
        'WEATHER_CITY': 'Weather City',
        'WEATHER_COUNTRY_CODE': 'Weather Country Code',
        'EMAIL_SENDER': 'Email Sender',
        'EMAIL_PASSWORD': 'Email Password',
        'EMAIL_RECIPIENT': 'Email Recipient',
        'SMTP_SERVER': 'SMTP Server',
        'SMTP_PORT': 'SMTP Port',
        'GCP_PROJECT_ID': 'GCP Project ID',
        'GCP_REGION': 'GCP Region',
        'GOOGLE_APPLICATION_CREDENTIALS': 'GCP Credentials Path',
        'AGENT_NAME': 'Agent Name',
        'SYSTEM_PROMPT': 'System Prompt',
        'DEBUG': 'Debug Mode',
        'LOG_LEVEL': 'Log Level'
    }
    
    all_good = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'PASSWORD' in var:
                display_value = value[:8] + "..." if len(value) > 8 else "***"
            else:
                display_value = value
            print(f"✅ {description}: {display_value}")
        else:
            print(f"❌ {description}: MISSING")
            all_good = False
    
    print("=" * 50)
    
    if all_good:
        print("🎉 All environment variables are set correctly!")
    else:
        print("⚠️  Some environment variables are missing.")
    
    return all_good

if __name__ == "__main__":
    verify_env() 