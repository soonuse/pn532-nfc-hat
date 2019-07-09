"""
This example emulates the module into a Mifare Classic card.
After initialization, try attaching the module to another PN532,
which is running the command InListPassiveTarget.
"""

import time
import RPi.GPIO as GPIO
#from pn532.i2c import PN532_I2C
#from pn532.spi import PN532_SPI
from pn532.uart import PN532_UART


if __name__ == '__main__':
    #pn532 = PN532_I2C(debug=False, reset=20, req=16)
    #pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    pn532 = PN532_UART(debug=False, reset=20)
    ic, ver, rev, support = pn532.get_firmware_version()
    pn532.SAM_configuration()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
    print('Emulating...')
    while True:
        result = pn532.tg_init_as_target(
            mode=0x05,                  # MODE: PICC only, Passive only
            mifare_params=[
                0x04, 0x00,             # SENS_RES
                0x3B, 0xC7, 0x54,       # NFCID1, SINGLE
                0x08                    # SEL_RES
            ],
            timeout=1
        )
        if result:
            print(result)
        time.sleep(0.1)
    GPIO.cleanup()
