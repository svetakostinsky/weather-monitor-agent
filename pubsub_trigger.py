"""
GCP Cloud Function entry point for Weather Monitor Agent triggered by Pub/Sub messages
This function will be triggered by messages from your runtime environment.
"""

import os
import sys
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.core import WeatherMonitorAgent


def weather_monitor_agent_pubsub(event, context):
    """
    Cloud Function entry point for weather monitoring triggered by Pub/Sub messages.
    
    Args:
        event: Pub/Sub event containing the message
        context: Cloud Function context
    
    Returns:
        dict: Result of the weather check operation
    """
    # Setup logging for Cloud Functions
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Parse the Pub/Sub message
    try:
        if hasattr(event, 'data'):
            # Pub/Sub event
            message_data = event.data.decode('utf-8')
            message_json = json.loads(message_data)
        else:
            # Direct HTTP call
            message_json = event.get_json() if hasattr(event, 'get_json') else {}
        
        trigger_source = message_json.get('triggered_by', 'pubsub')
        custom_message = message_json.get('message', '')
        
        logger.info(f"🌤️ Weather Monitor Agent triggered by {trigger_source}")
        if custom_message:
            logger.info(f"📝 Custom message: {custom_message}")
            
    except Exception as e:
        logger.warning(f"Could not parse message: {e}")
        trigger_source = 'unknown'
        custom_message = ''
    
    try:
        # Initialize the agent
        agent = WeatherMonitorAgent()
        
        # Run the daily weather check
        result = agent.run_daily_weather_check()
        
        # Add trigger information to result
        result['trigger_source'] = trigger_source
        result['custom_message'] = custom_message
        result['triggered_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
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
            'trigger_source': trigger_source,
            'custom_message': custom_message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


# For local testing
if __name__ == "__main__":
    # Simulate a Pub/Sub event
    class MockEvent:
        def __init__(self, data):
            self.data = json.dumps(data).encode('utf-8')
    
    test_event = MockEvent({
        "triggered_by": "runtime_environment",
        "message": "Test message from runtime"
    })
    
    result = weather_monitor_agent_pubsub(test_event, None)
    print(f"Result: {result}") 