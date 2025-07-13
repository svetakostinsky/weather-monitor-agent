"""
GCP Cloud Function entry point for Weather Monitor Agent
This function will be triggered by Cloud Scheduler for daily weather reports.
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


def weather_monitor_agent(request):
    """
    Cloud Function entry point for weather monitoring.
    
    Args:
        request: Flask request object (unused for scheduled functions)
    
    Returns:
        dict: Result of the weather check operation
    """
    # Setup logging for Cloud Functions
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("🌤️ Weather Monitor Agent triggered by Cloud Scheduler")
    
    try:
        # Initialize the agent
        agent = WeatherMonitorAgent()
        
        # Run the daily weather check
        result = agent.run_daily_weather_check()
        
        if result['success']:
            logger.info("✅ Weather check completed successfully!")
            logger.info(f"📧 Email sent to: {result['email_result']['message']}")
            logger.info(f"📍 Location: {result['weather_data']['city']}, {result['weather_data']['country']}")
            logger.info(f"🌡️ Temperature: {result['weather_data']['temperature']}°C")
        else:
            logger.error("❌ Weather check failed!")
            if 'error' in result:
                logger.error(f"Error: {result['error']}")
            if 'email_result' in result and 'error' in result['email_result']:
                logger.error(f"Email Error: {result['email_result']['error']}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Fatal error in Cloud Function: {str(e)}")
        return {
            'success': False, 
            'error': str(e),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


# For local testing
if __name__ == "__main__":
    result = weather_monitor_agent(None)
    print(f"Result: {result}") 