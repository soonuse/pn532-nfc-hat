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

print('Before:')
p3, p7, i0i1 = pn532.read_gpio()
for i in range(6):
    print('P3%d: %s' % (i, True if (p3 >> i & 1) else False))
for i in [1, 2]:
    print('P7%d: %s' % (i, True if (p7 >> i & 1) else False))
for i in [0, 1]:
    print('I%d: %s' % (i, True if (i0i1 >> i & 1) else False))
# Same as pn532.write_gpio(p3=0b00010101)
pn532.write_gpio('P30', True)
pn532.write_gpio('P31', False)
# pn532.write_gpio('P32', True)    # RESERVED (Must be HIGH)
pn532.write_gpio('P33', False)
# pn532.write_gpio('P34', True)    # RESERVED (Must be HIGH)
pn532.write_gpio('P35', False)
# Same as pn532.write_gpio(p7=0b00000100)
pn532.write_gpio('P71', False)
pn532.write_gpio('P72', True)
print('After:')
p3, p7, i0i1 = pn532.read_gpio()
for i in range(6):
    print('P3%d: %s' % (i, True if (p3 >> i & 1) else False))
for i in [1, 2]:
    print('P7%d: %s' % (i, True if (p7 >> i & 1) else False))
for i in [0, 1]:
    print('I%d: %s' % (i, True if (i0i1 >> i & 1) else False))
print('Note:')
print('1.  All Pins are set to the default state after hardware reset.')
print('2.  P71/P72 are always HIGH in SPI mode.')
print('3.  DO NOT reset the P32 and P34 pins.')
GPIO.cleanup()
