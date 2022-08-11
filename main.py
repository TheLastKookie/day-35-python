import requests
import os
from twilio.rest import Client

# WEATHER ALERT APP
# Make sure to fill in your own Open Weather api_key and Twilio account_sid and auth_token
api_key = os.environ.get("OWM_API_KEY")
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

parameters = {
    "lat": 40.712776,
    "lon": -74.005974,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get("https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
hourly_forecast = weather_data["hourly"][:12]
weather_codes = [hour["weather"][0]["id"] for hour in hourly_forecast]

will_rain = False
for code in weather_codes:
    if int(code) < 700:
        will_rain = True

# Fill in your own from and to phone numbers
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an ☔️",
        from_="+",
        to="+"
    )
    print(message.status)
