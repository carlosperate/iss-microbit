# MicroPython Firmware

This folder contains the MicroPython builds for the boards used in this
project.

Currently only builds for the Wemos LOLIN C3 Mini board as stored here.

- `LOLIN_C3_MINI-20231005-v1.21.0.bin`: Official MicroPython v1.21 for the
  Wemos C3 mini
- `LOLIN_C3_MINI-30b0ee3-uartrepl.bin`: Custom build of MicroPython v1.21
  for the Wemos C3 mini with REPL directed to UART 0 pins
- `LOLIN_C3_MINI-30b0ee3-uartrepl-frozen.bin`: Custom build with UART REPL
  and the urequests library frozen inside the build.


## Installation Instructions for Wemos C3 Mini

### Dependencies

To install the firmware on the ESP32-C3 we need to use the `esptool` Python
tool and the MicroPython `mpremote` tool.
You can install it (ideally in a virtual environment) with:

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
esptool.py --chip esp32c3 --port /dev/ttyUSB0 --baud 1000000 write_flash -z 0x0 LOLIN_C3_MINI-30b0ee3-uartrepl-frozen.bin
```

### Installing MicroPython libraries

The MicroPython build with frozen modules doesn't need this step,
but other MicroPython images don't include the `micropython-libraries`:

- urequests: MicroPython version of the requests library.
    - v0.9.1 https://pypi.org/project/micropython-urequests/0.9.1/#files

After flashing MicroPython, the libraries can be installed into the device
with the `mpremote` tool:

```
mpremote connect <serial_port> fs mkdir urequests
```
```
mpremote connect <serial_port> fs cp urequests/__init__.py :urequests/__init__.py
```

### Building the MicroPython image

The MicroPython repo has been included in this directory as a submodule,
at the commit from main at the time of inclusion.

To configure the REPL to be directed to UART0 instead of USB the
`ports/esp32/boards/LOLIN_C3_MINI/sdkconfig.board` file has to be edited
with this patch:

```
cd micropython
git apply ../micropython-reapl-uart.patch
cd ../..    # Moving to the project root directory
docker run -it --rm -v $(pwd):/mp -w /mp espressif/idf:v5.0.2 make -C firmware/micropython/mpy-cross
docker run -it --rm -v $(pwd):/mp -w /mp espressif/idf:v5.0.2 make -C firmware/micropython/ports/esp32 submodules BOARD=LOLIN_C3_MINI
docker run -it --rm -v $(pwd):/mp -w /mp espressif/idf:v5.0.2 make -C firmware/micropython/ports/esp32 all BOARD=LOLIN_C3_MINI
```

Built file will be located in `ports/esp32/build-LOLIN_C3_MINI/firmware.bin`.

#### Building MicroPython with frozen libraries

The required libraries, like urequests, can be embedded into the MicroPython
bin file as frozen modules/packages, which saves the step to send the
Python files via `mpremote`.

The `manifes.py` file can be added to the Makefile invocation and it will
freeze the packages as part of the MicroPython build.

Adding `FROZEN_MANIFEST=manifest.py` to the build command,
from the repository root directory:

```
docker run -it --rm -v $(pwd):/mp -w /mp espressif/idf:v5.0.2 make -C firmware/micropython/ports/esp32 all BOARD=LOLIN_C3_MINI FROZEN_MANIFEST=/mp/firmware/manifest.py
```
