# MicroPython Firmware

This folder contains the MicroPython builds for the boards used in this
project.

`LOLIN_C3_MINI-20231005-v1.21.0.bin`: MicroPython v1.21 for the Wemos C3 mini


## Installation Instructions for Wemos C3 Mini

### Dependencies

To install the firmware on the ESP32-C3 we need to use the `esptool` Python
tool. You can install it (ideally in a virtual environment) with:
```
pip install esptool
```

Or you can use this requirements.txt created with Python 3.7 on macOS:
```
pip install -r requirements.txt
```

### Install MicroPython

Use `esptool` to flash the MicroPython build, replacing `ttyUSB0` with
the right port in your system.

You can run `python -m serial.tools.list_ports` to list all your serial ports.

⚠️ Important! Place the board on DFU mode by holding down button D9 and pressing
reset.

```
esptool.py --chip esp32c3 --port /dev/ttyUSB0 erase_flash
```
```
esptool.py --chip esp32c3 --port /dev/ttyUSB0 --baud 1000000 write_flash -z 0x0 LOLIN_C3_MINI-20231005-v1.21.0.bin
```


## MicroPython libraries

Once MicroPython is installed in the Wemos C3 Mini, we need to add the
libraries included here:

- urequests: MicroPython version of the requests library.
    - v0.9.1 https://pypi.org/project/micropython-urequests/0.9.1/#files


### Installing packages

To do that we use the `mpremote` tool.

#### `mpremote`` installation

From a virtual environment:

```
pip install mpremote
```

Or using the requirements.txt located here, which also includes esptool:
```
pip install -r requirements.txt
```

#### Running `mpremote` to install packages

```
mpremote connect <serial_port> fs mkdir urequests
```
```
mpremote connect <serial_port> fs cp urequests/__init__.py :urequests/__init__.py
```
