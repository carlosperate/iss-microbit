
"""
This MicroPython script retrieves the current location of the
International Space Station (ISS) using a public free API and determines the
distance to a specific location set up in this script as a global variable.

As a MicroPython script for an ESP32 device, connecting to the internet,
it needs to connects to a Wi-Fi network, which details can be saved on the
gitignore WIFI_SECRETS_DONT_COMMIT.py file.
"""

import math
import network
import ujson as json
import urequests as requests

try:
    # You can add your WiFi SSID and password to this file, but make sure
    # WIFI_SECRETS_DONT_COMMIT.py is not committed to the repository!
    from WIFI_SECRETS_DONT_COMMIT import *
except ImportError:
    # Otherwise, the WiFi settings go here, just make sure you never commit it
    WIFI_SSID = "ssid_goes_here_do_not_commit"
    WIFI_KEY = "key_goes_here_do_no_commit"


# These should be YOUR local co-ordinates to calculate the distance to the ISS
# In this example these are the London co-ordinates
LOCAL_LATITUDE = 51.5072
LOCAL_LONGITUDE = -0.1276


def connect_wifi():
    """
    Connects to a WiFi network using the SSID and key provided in the
    WIFI_SECRETS_DONT_COMMIT.py file, or added to this file.
    """
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_KEY)
        while not sta_if.isconnected():
            pass
        print('network config:', sta_if.ifconfig())


def get_iss_location():
    """
    Retrieves the current latitude and longitude of the International Space
    Station (ISS) using the open-notify free API.

    :returns: A tuple containing the latitude and longitude of the ISS.
    """
    latitude = None
    longitude = None

    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    # print(data)

    if data["message"] == "success":
        latitude = data["iss_position"]["latitude"]
        longitude = data["iss_position"]["longitude"]
    return latitude, longitude


def distance_between_coordinates(lat1: float, lon1:float, lat2:float, lon2:float):
    """
    Calculate the distance between two sets of coordinates using the
    Haversine formula.

    Parameters:
    :param lat1: Latitude of the first coordinate in degrees.
    :param lon1: Longitude of the first coordinate in degrees.
    :param lat2: Latitude of the second coordinate in degrees.
    :param lon2: Longitude of the second coordinate in degrees.

    :returns: The distance between the two coordinates in kilometers.
    """

    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Radius of the Earth in kilometers
    radius = 6371

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c

    return distance


def main():
    connect_wifi()
    latitude, longitude = get_iss_location()
    print(f"Current ISS location:\n\tLatitude {latitude}\n\tLongitude {longitude}")
    distance = distance_between_coordinates(
        LOCAL_LATITUDE, LOCAL_LONGITUDE, float(latitude), float(longitude)
    )
    print(f"Distance from Lat[{LOCAL_LATITUDE}] Lon{LOCAL_LONGITUDE}]: {distance} Km")


if __name__ == "__main__":
    main()
