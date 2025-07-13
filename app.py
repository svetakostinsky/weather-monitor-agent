#!/usr/bin/env python3
"""
Weather Monitor Agent - Main Application
A daily weather monitoring agent that sends weather reports via email.
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.core import WeatherMonitorAgent
from config.settings import settings


def main():
    """Main function to run the weather monitor agent."""
    print("🌤️ Weather Monitor Agent Starting...")
    
    try:
        # Initialize the agent
        agent = WeatherMonitorAgent()
        
        # Run the daily weather check
        result = agent.run_daily_weather_check()
        
        if result['success']:
            print("✅ Weather check completed successfully!")
            print(f"📧 Email sent to: {settings.email_recipient}")
            print(f"📍 Location: {result['weather_data']['city']}, {result['weather_data']['country']}")
            print(f"🌡️ Temperature: {result['weather_data']['temperature']}°C")
            print(f"🤖 AI Insights: {result['ai_insights'][:100]}...")
        else:
            print("❌ Weather check failed!")
            if 'error' in result:
                print(f"Error: {result['error']}")
            if 'email_result' in result and 'error' in result['email_result']:
                print(f"Email Error: {result['email_result']['error']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        logging.error(f"Fatal error in main: {str(e)}")
        return {'success': False, 'error': str(e)}


def test_mode():
    """Test mode - get weather without sending email."""
    print("🧪 Weather Monitor Agent - Test Mode")
    
    try:
        agent = WeatherMonitorAgent()
        weather_data = agent.get_weather_only()
        
        if 'error' not in weather_data:
            print("✅ Weather data retrieved successfully!")
            print(f"📍 Location: {weather_data['city']}, {weather_data['country']}")
            print(f"🌡️ Temperature: {weather_data['temperature']}°C")
            print(f"☁️ Conditions: {weather_data['description']}")
            print(f"💧 Humidity: {weather_data['humidity']}%")
            print(f"🌬️ Wind: {weather_data['wind_speed']} m/s")
        else:
            print(f"❌ Failed to get weather data: {weather_data['error']}")
        
        return weather_data
        
    except Exception as e:
        print(f"❌ Test mode error: {str(e)}")
        return {'error': str(e)}


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Weather Monitor Agent")
    parser.add_argument("--test", action="store_true", help="Run in test mode (no email)")
    parser.add_argument("--email-test", action="store_true", help="Send a test email")
    
    args = parser.parse_args()
    
    if args.test:
        test_mode()
    elif args.email_test:
        print("📧 Weather Monitor Agent - Email Test Mode")
        agent = WeatherMonitorAgent()
        result = agent.send_test_email()
        if result['success']:
            print("✅ Test email sent successfully!")
        else:
            print(f"❌ Failed to send test email: {result['error']}")
    else:
        main() 