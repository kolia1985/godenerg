import hidraw
import os

from connector import (Connector)
from time import sleep


class USBConnector(Connector):

    def write(self, data):
        self.dev.write(data)

    def read(self, size):
        retry=0
        return self._read(size)

    def _read(self, size):
        data = ''
        while True:
            data += ''.join(map(chr, self.dev.read(size)))
            if not data or '\r' in data or len(data) >= size:
                break
        return data

    def open(self):
        #device = self.devices[0]
        try:
           device = list(filter(lambda i: i['product_id'] == 20833, hidraw.enumerate()))[0]['path']
        except:
           import os
           from time import sleep
           os.system("./usbreset /dev/bus/usb/001/002")
           sleep(1)
           device = list(filter(lambda i: i['product_id'] == 20833, hidraw.enumerate()))[0]['path']
        self.log.info("Open device: %s" % device)
        try:
            self.dev = hidraw.device()
            self.dev.open_path(device)
        except Exception as e:
            self.log.error(e)
            import os
            self.log.info("Reset USB")
            os.system("./usbreset /dev/bus/usb/001/002")

    def close(self):
        self.dev.close()
