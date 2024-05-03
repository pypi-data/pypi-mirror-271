# This file contains the programmer interface for the piccstick programmer.
# It supports the low-voltage ICSP interface for PICs. Design files and firmware
# is available in the github repo: https://github.com/rex--/picstick

from .programmer import *

# PreDefined Characters and Commands
SEP = ASCII(':')
OK = ASCII('OK')
GREETING = ASCII('HELLO')
BYE = ASCII('BYE')
START = ASCII('START')
STOP = ASCII('STOP')
ADDR = ASCII('ADDR')
ROW = ASCII('ROW')
WORD = ASCII('WORD')
READ = ASCII('READ')
ERASE = ASCII('ERASE')

@register_programmer('picstick')
class PicstickProgrammer(SerialProgrammer):

    def __init__(self, args):
        super().__init__(args)
        self.page_size = 128

    def connect(self):
        try:
            self._conn.open()
        except serial.SerialException:
            print(f"Failed to open serial port: { self._port }")
            return False
        wait_print(f"Connecting to picstick: { self._port } @ { self._baud }\nSending greeting...")
        self._conn.flushInput()
        self._conn.write(GREETING + SEP)
        if self.__check_response(expected_resp=GREETING) is not True:
            print('device failed to respond')
            self._conn.close()
            return False
        print("connected to programmer")
        wait_print('Entering programming mode...')
        self._conn.flushInput()
        self._conn.write(START + SEP)
        if self.__check_response() is not True:
            print('failed. Closing connection')
            self.disconnect()
            return False
        print('success')
        return True
    
    def disconnect(self):
        wait_print('Leaving programming mode...')
        # print(self._conn.read_all())
        self._conn.flushInput()
        self._conn.write(STOP + SEP)
        if self.__check_response() is not True:
            print('failed. Closing connection')
            self._conn.close()
            return False
        print ('success')
        wait_print('Disconnecting from programmer...')
        self._conn.write(BYE + SEP)
        resp = self.__check_response(expected_resp=BYE)
        self._conn.close()
        if resp is not True:
            print('GOODBYE')
            return False
        print('goodbye')
        return True

    def write(self, address, data):
        wait_print(f"Writing {len(data)} bytes to {hex(address)}...")
        if len(data) == 2:
            # Write a single word
            cmd = WORD + SEP + INTBYTES(address) + SEP + data
        elif len(data) == self.page_size:
            # Write a whole row
            cmd = ROW + SEP + INTBYTES(address) + SEP + data
        else:
            # We should pad it or chunk to size.
            # Return an error until thats implemented.
            print(f'failed\nIncompatible data size: {len(data)}')
            return False
        self._conn.write(cmd)
        if self.__check_response() is not True:
            print('failed')
            return False
        print('success')
        return True

    def read(self, address, length):
        wait_print("Reading %i words from address: 0x%.4X..." % (length, address))
        read_resp = bytearray()
        for word in range(length):
            self._conn.write(READ + SEP + INTBYTES(address))
            if self.__check_response() is not True:
                print('failed')
                return None
            resp = self._conn.read(size=2)
            read_resp.extend(resp)
            address += 1
        print('success')
        return read_resp
    
    def erase(self, address):
        wait_print("Erasing Row: 0x%.4X..." % (address))
        self._conn.write(ERASE + SEP + INTBYTES(address))
        if self.__check_response() is not True:
            print('failed')
            return False
        print('success')
        return True

    def __check_response(self, expected_resp=OK):
        resp = self._conn.read_until(expected=SEP)
        # print(resp)
        if resp.rstrip(SEP) == expected_resp:
            return True
        else:
            return resp
