#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script shows how to execute Python code on a MicroPython device using a
serial connection.

This is a proof of concept using CPython and the PySerial library, but the
idea to be able to easily port it to MicroPython so that one MicroPython
device could execute Python code in another MicroPython device connected
to the serial port.

To use this script, replace '/dev/ttyUSB0' in the `SERIAL_PORT` 
global variable the appropriate serial port of your MicroPython device.
"""
import serial
import time

# Change this to the port for your MicroPython device
SERIAL_PORT = "/dev/cu.usbmodem142301"

# Define the Python code to be executed on the MicroPython device
python_code = '''import time

def foo(a=3):
    return a * 2

time.sleep(1)
print(foo())
time.sleep(1)
print(foo(6))
'''


def run_code_in_micropython(ser, py_code):
    # Send CTRL-B to end raw mode in case we are already there
    ser.write(b"\x02")
    time.sleep(0.01)
    # Send CTRL-C to stop any code running
    ser.write(b"\r\x03")
    ser.read_until(b">>> \r\n>")
    time.sleep(0.01)
    # Send CTRL-A to go into raw REPL mode
    ser.write(b"\r\x01")
    data = ser.read_until(b"raw REPL; CTRL-B to exit\r\n>")
    time.sleep(0.01)

    # Send CTRL-D to soft reset
    # We might not want to reset the device to keep running programme state
    #ser.write(b"\x04")
    #data = ser.read_until(b"soft reboot\r\n")
    #data = ser.read_until(b"raw REPL; CTRL-B to exit\r\n>")

    # Send the Python code to the MicroPython device in blocks of 32 bytes
    code_bytes = py_code.encode("utf-8")
    for i in range(0, len(code_bytes), 32):
        ser.write(code_bytes[i : min(i + 32, len(code_bytes))])
        time.sleep(0.01)

    # Send CTRL-D to indicate we are done, it executes the code & prints the output
    ser.write(b"\x04")
    # Read all output until the prompt
    response = ser.read_until(b"\x04>")
    # Split stdout and stderr, separated by a CTRL-D command
    out, err = response[2:-2].split(b"\x04", 1)

    # Send CTRL-B to exit raw REPL mode
    ser.write(b"\x02")

    return  out, err


def main():
    # Open the serial port
    ser = serial.Serial(SERIAL_PORT, 115200, timeout=5)
    time.sleep(1)

    # Execute code in the MicroPython device
    py_code = python_code
    print(f"Running: {'=' * 26}\n{py_code}\n{'-' * 35}")
    out, err = run_code_in_micropython(ser, py_code)
    print(f"STDOUT: {out}\n{'-' * 35}")
    print(f"STDERR: {err}\n{'=' * 35}\n\n")

    py_code = "print(foo(10))"
    print(f"Running: {'=' * 26}\n{py_code}\n{'-' * 35}")
    out, err = run_code_in_micropython(ser, py_code)
    print(f"STDOUT: {out}\n{'-' * 35}")
    print(f"STDERR: {err}\n{'=' * 35}\n\n")

    # Close the serial port
    ser.close()


if __name__ == "__main__":
    main()
