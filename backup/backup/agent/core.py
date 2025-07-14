import logging
from datetime import datetime
from typing import Dict, Any, Optional
from openai import OpenAI
from agent.tools import WeatherTools
from config.settings import settings


class WeatherMonitorAgent:
    """AI-powered weather monitoring agent that sends daily weather reports."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.weather_tools = WeatherTools()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, settings.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def generate_weather_insights(self, weather_data: Dict[str, Any]) -> str:
        """Generate AI-powered insights about the weather data."""
        if 'error' in weather_data:
            return f"Unable to generate insights due to weather data error: {weather_data['error']}"
        
        prompt = f"""
        As a weather expert, analyze this weather data and provide helpful insights:
        
        City: {weather_data['city']}, {weather_data['country']}
        Temperature: {weather_data['temperature']}°C (feels like {weather_data['feels_like']}°C)
        Conditions: {weather_data['description']}
        Humidity: {weather_data['humidity']}%
        Wind: {weather_data['wind_speed']} m/s
        Pressure: {weather_data['pressure']} hPa
        Sunrise: {weather_data['sunrise']}
        Sunset: {weather_data['sunset']}
        
        Provide:
        1. A brief weather summary
        2. Any notable weather patterns
        3. Recommendations for the day (clothing, activities, etc.)
        4. Any weather alerts or warnings if applicable
        
        Keep it concise and friendly.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=[
                    {"role": "system", "content": settings.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Failed to generate AI insights: {str(e)}")
            return "Unable to generate AI insights at this time."
    
    def run_daily_weather_check(self) -> Dict[str, Any]:
        """Main function to run the daily weather check and send email."""
        self.logger.info("Starting daily weather check...")
        
        try:
            # Get weather data and send email
            result = self.weather_tools.get_weather_and_send_email()
            
            # Generate AI insights
            insights = self.generate_weather_insights(result['weather_data'])
            
            # Log results
            if result['email_result']['success']:
                self.logger.info(f"Weather email sent successfully: {result['email_result']['message']}")
            else:
                self.logger.error(f"Failed to send weather email: {result['email_result']['error']}")
            
            return {
                'success': result['email_result']['success'],
                'weather_data': result['weather_data'],
                'email_result': result['email_result'],
                'ai_insights': insights,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            self.logger.error(f"Error in daily weather check: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def get_weather_only(self) -> Dict[str, Any]:
        """Get weather data without sending email (for testing)."""
        return self.weather_tools.get_current_weather()
    
    def send_test_email(self) -> Dict[str, Any]:
        """Send a test email with current weather data."""
        weather_data = self.get_weather_only()
        return self.weather_tools.send_weather_email(weather_data) 