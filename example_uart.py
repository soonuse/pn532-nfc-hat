import serial
import binascii
import threading
import time


def uart_read(uart):
    while True:
        result = uart.read(uart.in_waiting)
        if result:
            print('r:', result)
        time.sleep(0.5)

def uart_write(uart):
    while True:
        content = input()
        content = content.replace(' ', '').replace('0x', '').replace(',', '')
        try:
            content = binascii.unhexlify(content)
        except Exception as e:
            print(e)
        uart.write(content)
        if content:
            print('w:', content)
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
    ts.append(threading.Thread(target=uart_write, args=(uart,), daemon=True))
    ts.append(threading.Thread(target=uart_read, args=(uart,), daemon=True))
    for t in ts:
        t.start()
    error = False
    while not error:
        for t in ts:
            if t.is_alive():
                continue
            else:
                break_flag = True
