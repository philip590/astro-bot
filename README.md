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

Security Considerations

AstroBot uses a Webex token to authenticate requests to the webex messaging API and an OpenWeatherMap API key to access weather and geocoding services.

get_webex_token() and get_api_key() functions allow private information to be entered whe nthe program start.

API rate limiting
AstroBot uses time.sleep(5) in its main loop to wait 5 seconds between checks for new Webex messages. This reduces unecessary API requests and helps avoid reaching API rate limit.

Input validation
AstroBot checks whether a message begins with / before treating it as a command

![alt text](<Screenshot 2026-10-23 174251.png>)

The /Weather command also checks whether the user has provided a city name. If the city is missing, AstroBot sends a usage message 

![](<Screenshot 2026-10-23 174756.png>)

This checks help prevent invalid commands from being processed and reduce unnecessary API requests

RESTful API usuage in AstroBot
AstroBot uses RESTful APIs to communicate with Webex, OpenWeatherMap and Open Notify. These APIs allow the python application to request and exchange information over HTTP.

HTTP GET requests
AstroBot uses request.get() to retrieve information from external APIs.
get_rooms() retrieves available Webex space
get_latest_message() retrieves messages from a selected Webex space
get_weather() retrieves current weather information from OpenWeatherMap
get_iss_location() retrieves the ISS locations from the Open Notify
get_city_coordinates() and reverse_geocode() retrieves geographical info from OpenWeatherMap

HTTP POST requests
send_message() function uses requests.post() to send messages to the webex messaging API

Processing JSON responses
APIs return data in JSON format, which AstroBot converts into python dictionaries and lists using response.json()
Weather API returns temp,humidity,weather description, wind speed and formats them into a readable message
ISS API retuerns latitude and longitude inside the iss_position object. AstroBot extracts these coordinates and uses them to identify the ISS location

Security Considerations
AstroBot checks the HTTP status codes to determine whether the API request is successful 
If the Webex API returns status code 200, this would indicate that the request was successful

If an API fails, the bot can return an error message instead of attempting to process an unsuccessful response 

![alt text](<Screenshot 2026-10-23 180747.png>)
![alt text](<Screenshot 2026-10-23 180756.png>)
![alt text](<Screenshot 2026-10-23 180805.png>)

Handling invalid or unexpected API responses
AstroBot uses conditional checks when processing APIs responses. 
An example, the geocoding functions check whether a location was returned before attempting to access its coordinates.
This helps prevent errors when a user emters a city that cannot be found.

Avoiding excessive API requests
AstroBot uses a 5 second delay between Webex message checks reducing unnecessary requests.
The bot also tracks last_message_id to avoid repeatedly processing the same message.

MVC Design Pattern in AstroBot

Model:
Handles retrieving and processing data
Functions such as
                    get_weather(),
                    get_iss_location(),
                    get_city_coordinates(),
                    reverse_geocoding()

obtain information from external APIs and format the result

View:
Presents the information to the user through webex messages.
The send_message() function delivers formatted weather, ISS coordinates and help messages to the selected webex space

Controller:
Handles user commands and decides which functions to execute. 
Main() function checks messages for commands such as /Weather, 
                                                    /iss, 
                                                    /help,
                                                    /quit

Example: When a user enters /waether London:
-The main() function identifies the /weather command and extracts the city name
-The get_weather() function retrieves and process London's weather information from OpenWeatherMap
-Send_message() function sends the formatted weather response to the user through webex 

Effectiness of AstroBot
AstroBot was designed to help users have access to weather information and allow them to track the International Space Station through webex. The bot contains 4 commands: /weather, /iss, /help and /quit

The /weather command allows users to retrieve current weather conditions for a specific city, these include temperature,humidity, weather description and wind speed. 
The /iss command provides the ISS's current latitude and longitude and the ability to identify a nearby geographical location

Testing has proven that these commands have worked and returned information through webex. Overall Astrobot meets it main functionaily, altohugh it depeends on external APIs being available

Successful Design
One successful design was using a separate python functions for using different tasks. Such as get_weather() retrieves weather information, whilst send_messages() handles commmunication with webex. This makes the code easier to understand and fix issues quickly.

Another effective decision was using RESTful APIs because they allow AstroBot to retrieve live information without maintaining its own weather or ISS database

The 5 second delay between message checks also helps reduce unnecessary API requests

Challenge Encountered
One challenge was integrated multiple APIs because each service uses different endpoints, parameters and JSON response structures.

The webex API requires a bearer token for authentication, whike OpenWeatherMap uses an API key supplied through the appid parameter

Testing and debugging were important because errors in API requests or response processing could prevent commands from working correctly

Security Risks
A significant secuirty risk is exposing Webex tokens or OpenWeatherMap API keys. To reduce this risk, AstoBot allows the keys to be entered when the program starts instead of requiring real credentials to be stored in the source code.

Another risk is excessive API requests. AstroBot uses time.sleep(5) to limit how frequently it checks for new messages

Future Improvements
AstroBot could be improved by adding automatic retries when there are API failures.

Another improvement would be to seperate the program into modules for webex communication, weather information, ISS tracking and command processing. This would improve organisation and allow individual components to be tested independently.

Limitations
Although AstroBot successfully performs its main functions, its reliability depends on the availability of external API services.

Another limitation is that AstroBot uses polling to retrieve messages from webex everu 5 seconds. While this is straight forward to implement, it creates repeated API requests even when no messages are available. A future improvement would be to use webex webhooks, which would notify the application when a new message arrives.