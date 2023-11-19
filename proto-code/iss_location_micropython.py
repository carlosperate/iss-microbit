import urequests as requests
import ujson as json
import network


# The wifi settings go here, make sure you never add this to your git repo
WIFI_SSID = "ssid_goes_here_do_not_commit"
WIFI_KEY = "key_goes_here_do_no_commit"


def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_KEY)
        while not sta_if.isconnected():
            pass
        print('network config:', sta_if.ifconfig())


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
    connect_wifi()
    latitude, longitude = get_iss_location()
    print(f"Current ISS location:\n\tLatitude {latitude}\n\tLongitude {longitude}")


if __name__ == "__main__":
    main()
