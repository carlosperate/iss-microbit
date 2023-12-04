# Prototype code

This folder contains prototype code used to do proof-of-concepts for the
project.

Each Python file contains a header comment explaining what the code is doing
and the goal of the prototype.

- `iss_location.py`: A CPython (the Python running on your computer) script to
  get the current ISS location, print it, and show it on a map.
- `iss_location_micropython.py`: A simple MicroPython script to get the current
  ISS location and print its latitude/longitude to serial.
- `remote_execution.py`: A CPython script to send Python code via serial to a
  MicroPython device, execute, and parse the result.


## Flashing MicroPython scripts

Follow the instructions in [firmware/README.md](../firmware/README.md) document
to first flash MicroPython into the WiFi device.

Then, using `mpremote` to transfer the script as `main.py`, run:
```
mpremote connect <micropython_serial_port> fs cp iss_location_micropython.py :main.py
```
