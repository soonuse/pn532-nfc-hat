"""
Simplest example for UART test.
"""
import binascii
import threading
import time
import serial


def uart_read(uart):
    """UART read"""
    while True:
        result = uart.read(uart.in_waiting)
        if result:
            print('r:', ' '.join([('%02X' % i) for i in result]))
        time.sleep(0.05)


def uart_write(uart):
    """UART write"""
    while True:
        content = input()
        content = content.replace(' ', '').replace('0x', '').replace(',', '')
        content = binascii.unhexlify(content)
        if content:
            print('w:', ' '.join([('%02X' % i) for i in content]))
        uart.write(content)
        time.sleep(0.05)


if __name__ == '__main__':
    print('''
Usage:
Send hex values on UART, e.g. input
    55 55 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF 03 FD D4 14 01 17 00
followed by Enter
''')
    print('Press Ctrl+C to quit')
    uart = serial.Serial('/dev/ttyS0', 115200)
    if not uart.is_open:
        print('serial0 is not enabled')
        exit(-1)
    ts = []
    ts.append(threading.Thread(target=uart_write, args=(uart,)))
    ts.append(threading.Thread(target=uart_read, args=(uart,)))
    for t in ts:
        t.start()
