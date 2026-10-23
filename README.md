# astro-bot

Task 1: Webex Messaging API
The Webex Messaging API allows AstroBot to communicate with users through Webex spaces.My python programme uses HTTP GET requests to retrieve rooms and messages, and POST request to send responses.

API Base URL: https://webexapis.com/v1
Authentication Method: Bearer token found when signing into yor account on Webex
Endpoint to list rooms: GET /rooms
Endpoint to get messages: GET /messages?roomID={room_id}
Endpoint to send messages: POST /messages
Required Headers: Authorisation: Bearer (Your Webex token) and Content-type:application/json
Sample full GET request: GET https://webexapis.com/v1/rooms

![](<Screenshot 2026-10-23 155059.png>)
![alt text](<Screenshot 2026-10-23 155151.png>)

get_rooms() function retrieves the available webex space
get_latest_messages() checks for any new commands
send_message() function sends responses back to the selected space

The access token is used for authentication

ISS Current Location API
The ISS shows the current coordinates of the International Space Station. The Astrobot uses the Open Notify API to retrive this information

API Base URL: https://api.open-notify.org
Endpoint for current ISS location: GET /iss-now.json
Sample response format (JSON):{"message":"success",
                                "timestamp":1471273200
                                "iss_position":{"latitude": "50.0258": "longitude": "-149.9405"}}
                            
![alt text](image.png)

get_iss_location() function sends a GET request using requests.get(url) to retrieve the ISS location
The JSON response is processed using response.json()
The latitude and longitude are taken from the iss_position

The coordinates are passed to a reverse_geocode() function to identify a nearby place. If no nearby locations is found the bot displays "Over Ocean/No Nearby City"

Geocoding API

Provider used: OpenWeatherMap
API Base URL: https//api.openweathermap.org
Endpoint for geocoding: GET /geo/1.0/direct
Endpoint for reverse geocoding GET /geo/1.0/reverse
Authentication method: API key ising appid
Required query parameters: q,lat,lon,limit,appid

get_city_coordinates() function uses forward geocoding to convert a city name into coordinates for the weather API.
reverse_geocode() function uses the ISS coordinates to find a nearby location

Weather API

API Provider:OpenWeatherMap
API Base URL:https://api.open.weathermap.org
Endpoint for current weather: GET /data/2.5/weather
Authentication Method:API key passed through the appid

QUery parameters:
lat-Latittude of location
lon-longitude of the location
appid-OpenWeatherMap API key
units=metric -Returns temperature in celsius

When I type /weather London, the bot first uses get_city_coordinates() to find London's latitude and longitude
get_weather() function then sends a GET request to OpenWeatherMap using requests.get()

The API returns JSON containing the temp,weather description, humidity and wind speed. AstroBot formats this info and sends it to the webex space using send_message.

![alt text](<Screenshot 2026-10-23 162034.png>)

Epoch to Human Time Conversion
Library Used:Python's built-in time module.
Function used to convert epoch:
time.strftime() with time.localtime()

The output is a timestamp that is converted to a date and time in the computers local timezone.

time.localtime() function converts the unix timestamp into a local time structure
time_strftime() function formats this into a readable date and time

Extended Feature API

API Provider:OpenWeatherMap
API Base URL: https://api.openweathermap.org
Endpoint: GET /geo/1.0/reverse
Authentication method: API key supplied 

Required parameters:
lat-latitude of the ISS
lon-longitude of the ISS
limit-Maximum number of locations returned
appid-OpenWeatherMap API key

get_iss_location() function retrieves the ISS coordinates from the Open Notify API. These coordinates are then passed to reverse_geocode(), which sends a GET request to OpenWeatherMap.

Web Architecture- Client- Server Model
AstroBot uses a client-server communication with webex and retrieve information from external APIs

Client: AstroBot uses a python application that acts as an HTTP client when requesting information from APIs. The user interacts with AstroBot through webex.

Servers:
Webex Messaging API: Recieves and delivers messages between users and Astrobot
OpenWeatherMap API: Provides current weather information and geocoding services
Open Notify API: Provides the current location of the internation space station

The user enters a command such as /weather London into webex
Astrobot sends a GET request to the webex messaging API to retrieve the message
Astrobot process the command and sends GET requests to the appropriate external API
The API returns information in JSON format
AstroBot process the JSON and sends a POST request to Webex to deliver the response to the user

![alt text](<Screenshot 2026-10-23 173327.png>)

The get_latest_message() function uses requests.get() to retrieve Webex messages
Send_message() function uses request.get() to request weather information from OpenWeatherMap
Send_message() function uses request.post() to send the response back to webex
