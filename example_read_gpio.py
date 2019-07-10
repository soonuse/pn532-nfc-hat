"""
This example shows connecting to the PN532 and reading the GPIOs.
"""

import RPi.GPIO as GPIO

from pn532 import *

pn532 = PN532_SPI(reset=20, cs=4, debug=False)
#pn532 = PN532_I2C(debug=False, reset=20, req=16)
#pn532 = PN532_UART(reset=20, debug=False)

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

p3, p7, i0i1 = pn532.read_gpio()
print('GPIO state:')
for i in range(6):
    print('P3%d: %s' % (i, True if (p3 >> i & 1) else False))
for i in [1, 2]:
    print('P7%d: %s' % (i, True if (p7 >> i & 1) else False))
for i in [0, 1]:
    print('I%d: %s' % (i, True if (i0i1 >> i & 1) else False))
print('i0:', pn532.read_gpio('I0'))
print('i1:', pn532.read_gpio('I1'))
print('P34:', pn532.read_gpio('P34'))
GPIO.cleanup()
