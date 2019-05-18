"""
This module will let you communicate with a PN532 RFID/NFC chip
using SPI on the Raspberry Pi.
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/soonuse/pn532-nfc-hat.git"

import time
import spidev
import RPi.GPIO as GPIO
from .pn532 import PN532

# pylint: disable=bad-whitespace
_SPI_STATREAD                  = 0x02
_SPI_DATAWRITE                 = 0x01
_SPI_DATAREAD                  = 0x03
_SPI_READY                     = 0x01


class SPIDevice:
    """Implements SPI device on spidev"""
    def __init__(self, cs=None):
        self.spi = spidev.SpiDev(0, 0)
        GPIO.setmode(GPIO.BCM)
        self._cs = cs
        if cs:
            GPIO.setup(self._cs, GPIO.OUT)
            GPIO.output(self._cs, GPIO.HIGH)
        self.spi.max_speed_hz = 15200
        self.spi.mode = 0b00

    def writebytes(self, buf):
        if self._cs:
            GPIO.output(self._cs, GPIO.LOW)
        ret = self.spi.writebytes(list(buf))
        if self._cs:
            GPIO.output(self._cs, GPIO.HIGH)
        return ret

    def readbytes(self, count):
        if self._cs:
            GPIO.output(self._cs, GPIO.LOW)
        ret = bytearray(self.spi.readbytes(count))
        if self._cs:
            GPIO.output(self._cs, GPIO.HIGH)
        return ret

    def xfer(self, buf):
        if self._cs:
            GPIO.output(self._cs, GPIO.LOW)
        buf = bytearray(self.spi.xfer(buf))
        if self._cs:
            GPIO.output(self._cs, GPIO.HIGH)
        return buf


def reverse_bit(num):
    """Turn an LSB byte to an MSB byte, and vice versa. Used for SPI as
    it is LSB for the PN532, but 99% of SPI implementations are MSB only!"""
    result = 0
    for _ in range(8):
        result <<= 1
        result += (num & 1)
        num >>= 1
    return result


class PN532_SPI(PN532):
    """Driver for the PN532 connected over SPI. Pass in a hardware SPI device
    & chip select digitalInOut pin. Optional IRQ pin (not used), reset pin and
    debugging output."""
    def __init__(self, cs=None, irq=None, reset=None, debug=False):
        """Create an instance of the PN532 class using SPI"""
        self.debug = debug
        self._gpio_init(cs=cs, irq=irq, reset=reset)
        self._spi = SPIDevice(cs)
        super().__init__(debug=debug, reset=reset)

    def _gpio_init(self, reset=None, cs=None, irq=None):
        self._cs = cs
        self._irq = irq
        GPIO.setmode(GPIO.BCM)
        if reset:
            GPIO.setup(reset, GPIO.OUT)
        if cs:
            GPIO.setup(cs, GPIO.OUT)
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
        time.sleep(1)
        self._spi.writebytes(bytearray([0x00])) #pylint: disable=no-member
        time.sleep(1)

    def _wait_ready(self, timeout=1):
        """Poll PN532 if status byte is ready, up to `timeout` seconds"""
        status = bytearray([reverse_bit(_SPI_STATREAD), 0])
        timestamp = time.monotonic()
        while (time.monotonic() - timestamp) < timeout:
            time.sleep(0.02)   # required
            status = self._spi.xfer(status) #pylint: disable=no-member
            if reverse_bit(status[1]) == _SPI_READY:  # LSB data is read in MSB
                return True      # Not busy anymore!
            else:
                time.sleep(0.01)  # pause a bit till we ask again
        # We timed out!
        return False

    def _read_data(self, count):
        """Read a specified count of bytes from the PN532."""
        # Build a read request frame.
        frame = bytearray(count+1)
        # Add the SPI data read signal byte, but LSB'ify it
        frame[0] = reverse_bit(_SPI_DATAREAD)
        time.sleep(0.02)   # required
        frame = self._spi.xfer(frame) #pylint: disable=no-member
        for i, val in enumerate(frame):
            frame[i] = reverse_bit(val) # turn LSB data to MSB
        if self.debug:
            print("Reading: ", [hex(i) for i in frame[1:]])
        return frame[1:]

    def _write_data(self, framebytes):
        """Write a specified count of bytes to the PN532"""
        # start by making a frame with data write in front,
        # then rest of bytes, and LSBify it
        rev_frame = [reverse_bit(x) for x in bytes([_SPI_DATAWRITE]) + framebytes]
        if self.debug:
            print("Writing: ", [hex(i) for i in rev_frame])
        time.sleep(0.02)   # required
        self._spi.writebytes(bytes(rev_frame))
