import time
from serial.tools import list_ports
import serial
import logging
import argparse

import br_decoder


logger = logging.getLogger('Barcode Scanner')


def populate_comports(kind='usb') -> list:
    ports = []
    for port in list_ports.comports():
        if kind.lower() in port.name:
            ports.append(port)
    return ports


class BarcodeScanner:
    def __init__(self, comport):
        try:
            self.scanner = serial.Serial(comport, baudrate=115200, timeout=0.2, write_timeout=0.2)
            self.scanner.write(b'#REVSOFT\r\n')
            data = self.scanner.readall().decode()
            if not len(data) > 0:
                raise serial.SerialException("Could not get software revision from the Barcode scanner.")
            logger.debug(data)

        except serial.SerialTimeoutException:
            logger.error('Timeout while trying to communicate with the Barcode Scanner')
        except serial.SerialException:
            logger.error('Error communicating with Barcode Scanner')

    def scan(self) -> bytes:
        self.scanner.write(b'#TRGON\r\n')
        time.sleep(5)
        self.scanner.write(b'#TRGOFF\r\n')
        data = self.scanner.read_until(expected=b'20Z00000')
        return data


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Check Barcode Scanner Communication.")
    parser.add_argument('--L', type=str, default='info')

    if parser.parse_args().L == 'info':
        logging.basicConfig(level=logging.INFO)
    elif parser.parse_args().L.startswith('de'):
        logging.basicConfig(level=logging.DEBUG)

    ports = populate_comports()
    for port in ports:
        logger.debug(port)

    scanner = BarcodeScanner(comport='/dev/cu.usbmodemyymmddxxx1')
    sdata = scanner.scan()
    logger.debug(sdata)  # .decode(encoding="utf-8"))
    logger.debug(len(sdata))
    logger.info(br_decoder.Decoder().decode(sdata))

