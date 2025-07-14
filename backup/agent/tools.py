import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, Optional
from config.settings import settings


class WeatherTools:
    """Tools for weather monitoring and email functionality."""
    
    def __init__(self):
        self.weather_api_key = settings.openweather_api_key
        self.city = settings.weather_city
        self.country_code = settings.weather_country_code
        
    def get_current_weather(self) -> Dict[str, Any]:
        """Get current weather data for the configured city."""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': f"{self.city},{self.country_code}",
                'appid': self.weather_api_key,
                'units': 'metric'  # Use metric units
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant weather information
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 'N/A'),
                'visibility': data.get('visibility', 'N/A'),
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return weather_info
            
        except requests.RequestException as e:
            return {'error': f"Failed to fetch weather data: {str(e)}"}
        except KeyError as e:
            return {'error': f"Unexpected weather data format: {str(e)}"}
    
    def format_weather_email(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data into a readable email."""
        if 'error' in weather_data:
            return f"❌ Weather Report Error\n\n{weather_data['error']}"
        
        subject = f"🌤️ Daily Weather Report - {weather_data['city']}, {weather_data['country']}"
        
        body = f"""
🌤️ Daily Weather Report
📅 {weather_data['timestamp']}
📍 {weather_data['city']}, {weather_data['country']}

🌡️ Temperature: {weather_data['temperature']}°C (feels like {weather_data['feels_like']}°C)
☁️ Conditions: {weather_data['description'].title()}
💧 Humidity: {weather_data['humidity']}%
🌬️ Wind: {weather_data['wind_speed']} m/s
📊 Pressure: {weather_data['pressure']} hPa

🌅 Sunrise: {weather_data['sunrise']}
🌇 Sunset: {weather_data['sunset']}

---
Sent by your Weather Monitor Agent 🤖
        """
        
        return body.strip()
    
    def send_weather_email(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send weather report via email."""
        try:
            # Format the email
            email_body = self.format_weather_email(weather_data)
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = settings.email_sender
            msg['To'] = settings.email_recipient
            msg['Subject'] = f"🌤️ Daily Weather Report - {weather_data.get('city', 'Unknown')}"
            
            # Add body to email
            msg.attach(MIMEText(email_body, 'plain'))
            
            # Create SMTP session
            server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
            server.starttls()
            server.login(settings.email_sender, settings.email_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(settings.email_sender, settings.email_recipient, text)
            server.quit()
            
            return {
                'success': True,
                'message': f"Weather email sent successfully to {settings.email_recipient}",
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to send email: {str(e)}",
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def get_weather_and_send_email(self) -> Dict[str, Any]:
        """Main function to get weather and send email report."""
        weather_data = self.get_current_weather()
        email_result = self.send_weather_email(weather_data)
        
        return {
            'weather_data': weather_data,
            'email_result': email_result,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        } 