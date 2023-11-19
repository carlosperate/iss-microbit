#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script retrieves the current location of the International Space Station
(ISS) using the Open Notify API and creates a map that is opened with the
default web browser.

The goal of this prototype script is to check we can get the ISS location with
a simple API call, without any kind of authentication.
The map is just a convenience, which can be contrasted with:
https://www.astroviewer.net/iss/en/
"""
import requests
import folium
import webbrowser
import time


def get_iss_location():
    latitude = None
    longitude = None

    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    # print(data)

    if data["message"] == "success":
        latitude = data["iss_position"]["latitude"]
        longitude = data["iss_position"]["longitude"]
    return latitude, longitude


def main():
    latitude, longitude = get_iss_location()
    print(f"Current ISS location:\n\tLatitude {latitude}\n\tLongitude {longitude}")

    # Create a map with a marker in the ISS location and HTML file and open it
    m = folium.Map(
        location=(latitude, longitude),
        control_scale=True,
    )
    folium.Marker(
        location=(latitude, longitude),
        popup="ISS Location",
        icon=folium.Icon(color="red", icon="satellite", prefix="fa"),
    ).add_to(m)
    m.save("index.html")

    print("Opening map on default browser...", end="")
    webbrowser.open("index.html", new=1, autoraise=True)
    time.sleep(1)
    print(" Done.")


if __name__ == "__main__":
    main()
