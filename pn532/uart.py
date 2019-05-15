"""
This module will let you communicate with a PN532 RFID/NFC chip
using UART (ttyS0) on the Raspberry Pi.
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/soonuse/pn532-nfc-hat.git"

import time
import serial
import RPi.GPIO as GPIO
from .pn532 import PN532, BusyError


# pylint: disable=bad-whitespace
DEV_SERIAL          = '/dev/ttyS0'
BAUD_RATE           = 115200


class PN532_UART(PN532):
    """Driver for the PN532 connected over UART. Pass in a hardware UART device.
    Optional IRQ pin (not used), reset pin and debugging output. 
    """
    def __init__(self, dev=DEV_SERIAL, baudrate=BAUD_RATE,
                irq=None, reset=None, debug=False):
        """Create an instance of the PN532 class using UART
        before running __init__, you should
        1.  disable serial login shell
        2.  enable serial port hardware
        using 'sudo raspi-config' --> 'Interfacing Options' --> 'Serial'
        """

        self.debug = debug
        self._gpio_init(irq=irq, reset=reset)
        self._uart = serial.Serial(dev, baudrate)
        if not self._uart.is_open:
            raise RuntimeError('cannot open {0}'.format(dev))
        super().__init__(debug=debug, reset=reset)

    def _gpio_init(self, reset=None,irq=None):
        self._irq = irq
        GPIO.setmode(GPIO.BCM)
        if reset:
            GPIO.setup(reset, GPIO.OUT)
        if irq:
            GPIO.setup(irq, GPIO.OUT)

    def _reset(self, pin):
        """Perform a hardware reset toggle"""
        GPIO.output(pin, True)
        time.sleep(0.1)
        GPIO.output(pin, False)
        time.sleep(0.5)
        GPIO.output(pin, True)
        time.sleep(0.1)

    def _wakeup(self):
        """Send any special commands/data to wake up PN532"""
        #self._write_frame([_HOSTTOPN532, _COMMAND_SAMCONFIGURATION, 0x01])
        self.SAM_configuration()

    def _wait_ready(self, timeout=0.001):
        """Wait `timeout` seconds"""
        time.sleep(timeout)
        return True

    def _read_data(self, count):
        """Read a specified count of bytes from the PN532."""
        frame = self._uart.read(min(self._uart.in_waiting, count))
        if not frame:
            raise BusyError("No data read from PN532")
        if self.debug:
            print("Reading: ", [hex(i) for i in frame])
        else:
            time.sleep(0.1)
        return frame

    def _write_data(self, framebytes):
        """Write a specified count of bytes to the PN532"""
        self._uart.read(self._uart.in_waiting)    # clear FIFO queue of UART
        self._uart.write(b'\x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') # wake up!
        self._uart.write(framebytes)
