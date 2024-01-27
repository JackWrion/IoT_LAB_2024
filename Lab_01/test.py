# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony Dicola, Justin Cooper, Brent Rubell

# Import Adafruit IO REST client.
from Adafruit_IO import MQTTClient,Client, Feed
import json
import base64

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_USERNAME = "jackwrion12345"

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_KEY = "YWlvX1VoS202M3FVa0FBTmNrT2FMZUZLWkZtR0NGOVM="
ADAFRUIT_IO_KEY = (base64.b64decode(ADAFRUIT_IO_KEY.encode("utf-8"))).decode("utf-8")

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# List all of your feeds
print("Obtaining user's feeds...")
feeds = aio.feeds()
print('Feeds: ', feeds)

# Create a new feed
print("Creating new feed...")
feed = Feed(name="PythonFeed")
response = aio.create_feed(feed)
print("New feed: ", response)

# Delete a feed
aio.delete_feed(response.key)

