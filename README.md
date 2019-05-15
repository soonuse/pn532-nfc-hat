# PN532 NFC HAT
This is a PN532 NFC library for Raspberry Pi.

## Features
-   Support I2C, SPI and HSU of PN532
-   Easy to understand how the PN532 chip works

## How to use
1.  Plug the PN532 NFC Hat to your Pi.
2.  The module supports I2C, SPI and HSU.
-   on I2C:
    Set switch SW1 as '010010', i.e.
    ```
    MOSI/SDA/TX Pin to Pi's SDA
    NSS/SCL/RX Pin to Pi's SCL
    ```
    Then set `SEL0: ON` and `SEL1: OFF`
-   on SPI:
    Set switch SW1 as '001001', i.e.
    ```
    MOSI/SDA/TX Pin to Pi's MOSI
    NSS/SCL/RX Pin to Pi's CE0
    ```
    Then set `SEL0: OFF` and `SEL1: ON`
-   on HSU(UART):
    Set switch SW1 as '100100', i.e.
    ```
    MOSI/SDA/TX Pin to Pi's RX
    NSS/SCL/RX Pin to Pi's TX
    ```
    Then set `SEL0: OFF` and `SEL1: OFF`
3.  Run the example with `python3 example.py`
4.  With waving a 13.56MHz NFC card, the UID of the card will be printed.
