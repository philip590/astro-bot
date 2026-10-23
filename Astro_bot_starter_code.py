#Contains partially completed code with sections for you to complete
#IT IS MANDATORY TO USE THE RESOURCE PROVIDED
#The starter code is structured into functions and modules. You are required to complete the missing sections while maintaining this modular design.  Further step by step instructions can be found in the appendix A of this assignment brief. 
#For extended features implement it within the existing modular structure. The new feature must be triggered using a new command (e.g., /stars, /moon, /sky) and follow the same approach 
#Use Git for version control. Maintain a repository on GitHub to track your project’s progress and changes. Ensure regular commits for each step with meaningful messages that document your step by stepdevelopment process. 

# =========================
# REQUIRED LIBRARIES
# =========================

import requests
import json
import time
from datetime import datetime

# =========================
# CONFIGURATION FUNCTIONS
# =========================
def get_webex_token():
    choice = input("Use hard-coded Webex token? (y/n): ").lower()
    if choice == "n":
        token = input("Enter your Webex Access Token: ")
        return f"Bearer {token}"
    else:
        return "Bearer YOUR_WEBEX_TOKEN"

def get_api_key(prompt, hardcoded_key):
    choice = input(f"Use saved {prompt}? (y/n): ").lower()
    if choice == "n":
        return input(f"Enter your {prompt}: ")
    else:
        return hardcoded_key

# =========================
# WEBEX FUNCTIONS
# =========================
def get_rooms(token):
    url = "https://webexapis.com/v1/rooms"  
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error fetching rooms:", response.status_code)
        return []

    return response.json().get("items", [])


def print_rooms(rooms):
    for room in rooms:
        print(f"Room Title: {room['title']}, Room ID: {room['id']}")


def select_room(rooms):
    while True:
        name = input("Enter the room name: ")
        for room in rooms:
            if name.lower() in room["title"].lower():
                print(f"Selected Room: {room['title']}")
                return room["id"]
        print("Room not found. Please try again.")


def get_latest_message(token, room_id):
    url = "https://webexapis.com/v1/messages"
    params = {"roomId": room_id}
    headers = {"Authorization": token}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return None, None

    data = response.json().get("items", [])

    if not data:
        return None, None

    latest = data[0]
    return latest.get("id"), latest.get("text", "")


def send_message(token, room_id, message):
    url = "https://webexapis.com/v1/messages"
    headers = {"Authorization": token, 
    "Content-Type": "application/json"}
    data = {
        "roomId": room_id,
        "text": message
    }
    requests.post(url, headers=headers, json=data)

# =========================
# WEATHER FUNCTIONS
# =========================
def get_city_coordinates(city, api_key):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    return data[0] if data else None


def get_weather(city, api_key):
    location = get_city_coordinates(city, api_key)

    if not location:
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": location["lat"],
        "lon": location["lon"],
        "units": "metric",
        "appid": api_key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    weather = response.json()

    return (
        f"Weather in {weather['name']}, {weather['sys']['country']}:"
        f"{weather['main']['temp']}°C, "
        f"{weather['weather'][0]['description']}, "
        f"Humidity: {weather['main']['humidity']}%, "
        f"Wind Speed: {weather['wind']['speed']} m/s"
    )
# SKY / STARGAZING FUNCTION
def get_sky(city, api_key):
    location = get_city_coordinates(city, api_key)

    if not location:
        return "City not found."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": location["lat"],
        "lon": location["lon"],
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        cloud_cover = data["clouds"]["all"]

        if cloud_cover <=20:
            condition = "Clear skies, great for stargazing"
        elif cloud_cover <= 50:
            condition = "Partly cloudy, some stars may be visible"
        else:
            condition = "Cloudy, stargazing may be difficult"

        return(
            f"Sky conditions in {city}:\n"
            f"Cloud Cover: {cloud_cover}%\n"
            f"{condition}"
        )
    except (requests.RequestException, KeyError, ValueError, TypeError) as e:
        print(f"Sky API Error: {e}")
        return "Unable to retrieve sky conditions right now."

# =========================
# ISS FUNCTIONS
# =========================
def reverse_geocode(lat, lon, api_key):
    url = "https://api.openweathermap.org/geo/1.0/reverse"
    params = {"lat": lat, "lon": lon, "limit": 1, "appid": api_key}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    return data[0] if data else None


def get_iss_location(api_key):
    url = "http://api.open-notify.org/iss-now.json"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    lat = data["iss_position"]["latitude"]
    lon = data["iss_position"]["longitude"]

    location = reverse_geocode(lat, lon, api_key)

    place = "Over Ocean / No Nearby City"

    if location:
        place = f"{location.get('name', 'Unknown City')}, {location.get('country', 'Unknown Country')}"

    return (
        f"ISS Current Location:\n"
        f"Latitude: {lat}, Longitude: {lon}\n"
        f"Place: {place}"
    )

# =========================
# MAIN BOT LOGIC
# =========================
def main():

    token = get_webex_token()

    weather_key = get_api_key(
        "Weather API key",
        "YOUR_OPENWEATHER_API_KEY"
    )

    rooms = get_rooms(token)

    if not rooms:
        print("No Webex rooms found. Check your access token and try again.")
        return

    print_rooms(rooms)
    room_id = select_room(rooms)

    last_message_id, _ = get_latest_message(token, room_id)

    while True:

        message_id, message_text = get_latest_message(token, room_id)

        if message_id and message_id != last_message_id:

            last_message_id = message_id

            print(f"Received message: {message_text}")

            if not message_text.startswith("/"):
                continue

            if message_text.lower() == "/help":
                send_message(
                    token,
                    room_id,
                    "/weather <city>\n/sky <city>\n/iss\n/help\n/quit"
                )

            elif message_text.lower().startswith("/weather"):

                parts = message_text.split(maxsplit=1)

                if len(parts) < 2:
                    send_message(token, room_id, "Usage: /weather <city>")
                else:
                    city = parts[1]
                    send_message(token, room_id, get_weather(city, weather_key))

            elif message_text.lower().startswith("/sky"):
                parts = message_text.split(maxsplit=1)
                if len(parts) < 2:
                    send_message(token, room_id, "Usage: /sky <city>")
                else:
                    city = parts[1]
                    send_message(token, room_id, get_sky(city, weather_key))

            elif message_text.lower() == "/iss":
                send_message(token, room_id, get_iss_location(weather_key))

            elif message_text.lower() == "/quit":
                send_message(token, room_id, "AstroBot shutting down.")
                break

            else:
                send_message(token, room_id, "Unknown command. Use /help")

        time.sleep(5)


if __name__ == '__main__':
    main()
