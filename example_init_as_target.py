"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported.
After initialization, try waving various 13.56MHz RFID cards over it!
"""

import time
import RPi.GPIO as GPIO
#from pn532.i2c import PN532_I2C
from pn532.spi import PN532_SPI
#from pn532.uart import PN532_UART


if __name__ == '__main__':
    #pn532 = PN532_I2C(debug=False, reset=20, req=16)
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    #pn532 = PN532_UART(debug=False, reset=20)
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
    print('Waiting for an initiator')
    result = pn532.tg_init_as_target(
        mode=0x00,                  # MODE: PICC only, Passive only
        mifare_params=[
            0x08, 0x00, 0x12, 0x34, 0x36, 0x40
        ],
        felica_params=[
            0x01, 0xFE, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7,
            0xC0, 0xC1, 0xC2, 0xC3, 0xC4, 0xC5, 0xC6, 0xC7,
            0xFF, 0xFF
        ],
        nfcid3t=[
            0xAA, 0x99, 0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11
        ],
        gt=[ord(i) for i in 'Hello world!']
    )
    if not result:
        GPIO.cleanup()
        exit(-1)
    mode, initiator_command = result
    ## print(pn532.tg_init_as_target(
    ##     mode=0x05,                  # MODE: PICC only, Passive only
    ##     mifare_params=[
    ##         0x04, 0x00,             # SENS_RES
    ##         0x11, 0x22, 0x23,       # NFCID1, SINGLE. Set UID as 0x112233
    ##         0x20                    # SEL_RES
    ##     ]
    ## ))

    print('mode: 0x%02X' % mode)
    for i in initiator_command:
        print('%02X' % i, end=' ')
    GPIO.cleanup()
