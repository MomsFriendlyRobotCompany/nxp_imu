from __future__ import print_function
from __future__ import division
import os

try:
    # can also be done with: export TRAVIS=1
    if 'TRAVIS' in os.environ:
        raise ImportError()

    from smbus2 import SMBus

except ImportError:
    from fake_rpi.smbus import SMBus as fakeSMBus

    class SMBus(fakeSMBus):
        resp = {
            0x21: 0xD7,
            0x1F: 0xC7
        }

        # @printf
        def read_byte_data(self, i2c_addr, register):
            return self.resp[i2c_addr]
#             ret = 0xff
#             if i2c_addr == 0x21:
#                     ret = 0xD7
#             elif i2c_addr == 0x1F:
#                     ret = 0xC7
#             return ret

"""
accel/mag - 0x1f
gyro - 0x21
other stuff - 0x40, 0x70-0x75
pi@r2d2 nxp $ sudo i2cdetect -y 1
    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 1f
20: -- 21 -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: 70 71 72 73 74 75 -- --
"""


class I2C(object):
    """
    This is just a wrapper around i2c. There are so many implementations.
    """
    def __init__(self, address, bus=1):
        self.i2c = SMBus(bus)
        self.address = address

    def __del__(self):
        self.i2c.close()

    def read8(self, reg):
        b = self.i2c.read_byte_data(self.address, reg)
        return b

    def read_block(self, reg, size):
        block = self.i2c.read_i2c_block_data(self.address, reg, size)
        return block

    def write_block(self, reg, data):
        self.i2c.write_i2c_block_data(self.address, reg, data)

    def write8(self, reg, data):
        # print(hex(self.address), reg, data)
        self.i2c.write_byte_data(self.address, reg, data)
