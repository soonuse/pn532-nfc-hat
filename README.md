# PN532 NFC HAT
This is a PN532 NFC library for Raspberry Pi.

![image](http://www.waveshare.net/photo/accBoard/PN532-NFC-HAT/PN532-NFC-HAT-3.jpg)

## Features
-   Support I2C, SPI and HSU of PN532
-   Easy to understand how the PN532 chip works

## How to use
1.  Plug the PN532 NFC Hat to your Pi.
2.  The module supports I2C, SPI and HSU.
-   on I2C:
    Set `I0: H` and `I1: L`, which means
    ```
    MOSI/SDA/TX Pin to Pi's SDA
    NSS/SCL/RX Pin to Pi's SCL
    ```
-   on SPI:
    Set `I0: L` and `I1: H`, which means
    ```
    MOSI/SDA/TX Pin to Pi's MOSI
    NSS/SCL/RX Pin to Pi's CE0
    ```
-   on HSU(UART):
    Set `I0: L` and `I1: L`, which means
    ```
    MOSI/SDA/TX Pin to Pi's RX
    NSS/SCL/RX Pin to Pi's TX
    ```
3.  Modify the init lines and Run the example with `python3 example.py`.
    -   for SPI, uncomment this line: `pn532 = PN532_SPI(debug=False, reset=20, cs=4)`, and comment lines for I2C and UART.
    -   for I2C, uncomment this line: `pn532 = PN532_I2C(debug=False, reset=20, req=16)`, and comment lines for SPI and UART.
    -   for UART, uncomment this line: `pn532 = PN532_UART(debug=False, reset=20)`, and comment lines for SPI, I2C.
   
4.  With waving a 13.56MHz NFC card, the UID of the card will be printed.
