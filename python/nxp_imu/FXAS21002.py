# Gyro
# MIT License
# Kevin Walchko

from __future__ import print_function
from __future__ import division
from math import pi
import time
import struct
from .I2C import I2C

EARTH_ROTATION_RATE = 2*pi/86400

FXAS21002C_ADDRESS       = 0x21       # 0100001
FXAS21002C_ID            = 0xD7       # 1101 0111

GYRO_SENSITIVITY_250DPS  = 0.0078125  # Table 35 of datasheet
GYRO_SENSITIVITY_500DPS  = 0.015625   # ..
GYRO_SENSITIVITY_1000DPS = 0.03125    # ..
GYRO_SENSITIVITY_2000DPS = 0.0625     # ..

GYRO_REGISTER_STATUS     = 0x00
GYRO_REGISTER_OUT_X_MSB  = 0x01
GYRO_REGISTER_OUT_X_LSB  = 0x02
GYRO_REGISTER_OUT_Y_MSB  = 0x03
GYRO_REGISTER_OUT_Y_LSB  = 0x04
GYRO_REGISTER_OUT_Z_MSB  = 0x05
GYRO_REGISTER_OUT_Z_LSB  = 0x06
GYRO_REGISTER_WHO_AM_I   = 0x0C   # 11010111   r
GYRO_REGISTER_CTRL_REG0  = 0x0D   # 00000000   r/w
GYRO_REGISTER_CTRL_REG1  = 0x13   # 00000000   r/w
GYRO_REGISTER_CTRL_REG2  = 0x14   # 00000000   r/w
GYRO_REGISTER_TEMP       = 0x12

# GYRO_RANGE_250DPS  = 250
# GYRO_RANGE_500DPS  = 500
# GYRO_RANGE_1000DPS = 1000
# GYRO_RANGE_2000DPS = 2000

GYRO_STANDBY = 0
GYRO_READY   = 1
GYRO_ACTIVE  = 2

# ODR bandwidth
# GYRO_BW_800  = 0
# GYRO_BW_400  = (1 << 2)
# GYRO_BW_200  = (2 << 2)
# GYRO_BW_100  = (3 << 2)
# GYRO_BW_50   = (4 << 2)
# GYRO_BW_25   = (5 << 2)

# Low Pass Filter settings
GYRO_LPF_HIGH = 0
GYRO_LPF_MED  = (1 << 6)
GYRO_LPF_LOW  = (2 << 6)

SENSORS_DPS_TO_RADS = pi/180

bandwidths = [25, 50, 100, 200, 400, 800]
# bwd = {
#     25: GYRO_BW_25,
#     50: GYRO_BW_50,
#     100: GYRO_BW_100,
#     200: GYRO_BW_200,
#     400: GYRO_BW_400,
#     800: GYRO_BW_800
# }

# ODR bandwidth
bwd = {
    25: 0,
    50: (1 << 2),
    100: (2 << 2),
    200: (3 << 2),
    400: (4 << 2),
    800: (5 << 2)
}

dps_range = [250, 500, 1000, 2000]


class FXAS21002(I2C):
    def __init__(self, dps=None, bw=100, bus=1, verbose=False):
        """
        Args:
            dps: 250, 500, 1000, or 2000 dps
            bw: 25, 50, 100, 200, 400, 800 Hz
            bus: i2c bus to use, default is 1
            verbose: print out some info at start
        """
        I2C.__init__(self, address=FXAS21002C_ADDRESS, bus=bus)

        if self.read8(GYRO_REGISTER_WHO_AM_I) != FXAS21002C_ID:
            raise Exception('Error talking to FXAS21002C at', hex(FXAS21002C_ID))

        _range = None
        if dps == 250:
            self.scale = GYRO_SENSITIVITY_250DPS
            self.write8(GYRO_REGISTER_CTRL_REG0, 0x03)
            _range = '250dps'
        elif dps == 500:
            self.scale = GYRO_SENSITIVITY_500DPS
            self.write8(GYRO_REGISTER_CTRL_REG0, 0x02)
            _range = '500dps'
        elif dps == 1000:
            self.scale = GYRO_SENSITIVITY_1000DPS
            self.write8(GYRO_REGISTER_CTRL_REG0, 0x01)
            _range = '1000dps'
        elif dps == 2000:
            self.scale = GYRO_SENSITIVITY_2000DPS
            self.write8(GYRO_REGISTER_CTRL_REG0, 0x00)
            _range = '2000dps'
        else:
            raise Exception('FXAS21002C: invalid gyro range: {}'.format(dps))

        """
        Set CTRL_REG1 (0x13)
        ====================================================================
        BIT  Symbol    Description                                   Default
        ---  ------    --------------------------------------------- -------
        6    RESET     Reset device on 1                                   0
        5    ST        Self test enabled on 1                              0
        4:2  DR        Output data rate                                  000
                            000 = 800 Hz
                            001 = 400 Hz
                            010 = 200 Hz
                            011 = 100 Hz
                            100 = 50 Hz
                            101 = 25 Hz
                            110 = 12.5 Hz
                            111 = 12.5 Hz
        1    ACTIVE    Standby(0)/Active(1)                                0
        0    READY     Standby(0)/Ready(1)                                 0
        """
        # Reset then switch to active mode with 100Hz output
        # self.write8(GYRO_REGISTER_CTRL_REG1, 0x00)  # don't need this?
        # self.write8(GYRO_REGISTER_CTRL_REG1, (1 << 6))  # set bit 6, reset bit
        # self.reset()
        # value = GYRO_BW_100 | GYRO_ACTIVE
        if bw in bandwidths:
            value = bwd[bw] | GYRO_ACTIVE
            self.write8(GYRO_REGISTER_CTRL_REG1, value)  # set 100 Hz Active=true
            time.sleep(0.06)  # 60 ms + 1/ODR
        else:
            raise Exception('FXAS21002C: invalid gyro bandwidth: {}'.format(bw))

        if verbose:
            print('='*40)
            print('FXAS21002C Gyro')
            print('  Addr: 0x21')
            print('  Range: +/- {}'.format(_range))
            print('  Temperature: {} C'.format(self.temperature()))

    def setActive(self):
        reg = self.read8(GYRO_REGISTER_CTRL_REG1)
        self.write8(GYRO_REGISTER_CTRL_REG1, reg | 2)

    # FIXME: doesn't work!!
    # def reset(self):
    #     self.write8(GYRO_REGISTER_CTRL_REG1, (1 << 6))
    #     time.sleep(0.1)

    def temperature(self):
        """Return gyro temperature in C, ONLY works in ACTIVE mode"""
        data = [self.read8(GYRO_REGISTER_CTRL_REG1)]
        data = bytearray(data)
        return struct.unpack('b', data)[0]

    def get(self):
        # 6 bytes: axhi, axlo, ayhi, aylo, azhi, azlo
        data = self.read_block(0x1, 6)
        data = bytearray(data)
        data = struct.unpack('>hhh', data)  # '>' big-endian, 'h' short (2 bytes)
        gyro = ([x * self.scale for x in data])

        return tuple(gyro)
