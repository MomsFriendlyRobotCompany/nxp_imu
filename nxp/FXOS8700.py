#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from smbus2 import SMBus
# import struct

"""
accel/mag - 0x1f
gyro - 0x21
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


FXOS8700_ADDRESS                  = 0x1F     # 0011111
FXOS8700_ID                       = 0xC7     # 1100 0111

FXOS8700_REGISTER_STATUS          = 0x00
FXOS8700_REGISTER_OUT_X_MSB       = 0x01
FXOS8700_REGISTER_OUT_X_LSB       = 0x02
FXOS8700_REGISTER_OUT_Y_MSB       = 0x03
FXOS8700_REGISTER_OUT_Y_LSB       = 0x04
FXOS8700_REGISTER_OUT_Z_MSB       = 0x05
FXOS8700_REGISTER_OUT_Z_LSB       = 0x06
FXOS8700_REGISTER_WHO_AM_I        = 0x0D   # 11000111   r
FXOS8700_REGISTER_XYZ_DATA_CFG    = 0x0E
FXOS8700_REGISTER_CTRL_REG1       = 0x2A   # 00000000   r/w
FXOS8700_REGISTER_CTRL_REG2       = 0x2B   # 00000000   r/w
FXOS8700_REGISTER_CTRL_REG3       = 0x2C   # 00000000   r/w
FXOS8700_REGISTER_CTRL_REG4       = 0x2D   # 00000000   r/w
FXOS8700_REGISTER_CTRL_REG5       = 0x2E   # 00000000   r/w
FXOS8700_REGISTER_MSTATUS         = 0x32
FXOS8700_REGISTER_MOUT_X_MSB      = 0x33
FXOS8700_REGISTER_MOUT_X_LSB      = 0x34
FXOS8700_REGISTER_MOUT_Y_MSB      = 0x35
FXOS8700_REGISTER_MOUT_Y_LSB      = 0x36
FXOS8700_REGISTER_MOUT_Z_MSB      = 0x37
FXOS8700_REGISTER_MOUT_Z_LSB      = 0x38
FXOS8700_REGISTER_MCTRL_REG1      = 0x5B   # 00000000   r/w
FXOS8700_REGISTER_MCTRL_REG2      = 0x5C   # 00000000   r/w
FXOS8700_REGISTER_MCTRL_REG3      = 0x5D   # 00000000   r/w

ACCEL_RANGE_2G                    = 0x00
ACCEL_RANGE_4G                    = 0x01
ACCEL_RANGE_8G                    = 0x02

ACCEL_MG_LSB_2G = 0.000244
ACCEL_MG_LSB_4G = 0.000488
ACCEL_MG_LSB_8G = 0.000976
MAG_UT_LSB      = 0.1


def twos_comp(val, bits):
	"""compute the 2's complement of int value val"""
	if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
		val = val - (1 << bits)        # compute negative value
	return val                         # return positive value as is


class FXOS8700(object):
	def __init__(self, accelSensorID=None, magSensorID=None):
		if accelSensorID is None:
			accelSensorID = FXOS8700_ADDRESS
		if magSensorID is None:
			magSensorID = 1
		self.accelAddr = accelSensorID
		self.magAddr = magSensorID
		self.bus = SMBus(1)

		if self.read8(FXOS8700_REGISTER_WHO_AM_I) == FXOS8700_ID:
			print('Found accel')
		else:
			raise Exception('wrong accel address')

		self._range = ACCEL_RANGE_2G

		# Set to standby mode (required to make changes to this register)
		self.write8(FXOS8700_REGISTER_CTRL_REG1, 0)

		# Configure the accelerometer
		if self._range == ACCEL_RANGE_2G:
			self.write8(FXOS8700_REGISTER_XYZ_DATA_CFG, 0x00)
		elif self._range == ACCEL_RANGE_4G:
			self.write8(FXOS8700_REGISTER_XYZ_DATA_CFG, 0x01)
		elif self._range == ACCEL_RANGE_8G:
			self.write8(FXOS8700_REGISTER_XYZ_DATA_CFG, 0x02)

		# High resolution
		self.write8(FXOS8700_REGISTER_CTRL_REG2, 0x02)
		# Active, Normal Mode, Low Noise, 100Hz in Hybrid Mode
		self.write8(FXOS8700_REGISTER_CTRL_REG1, 0x15)

		# Configure the magnetometer
		# Hybrid Mode, Over Sampling Rate = 16
		self.write8(FXOS8700_REGISTER_MCTRL_REG1, 0x1F)
		# Jump to reg 0x33 after reading 0x06
		self.write8(FXOS8700_REGISTER_MCTRL_REG2, 0x20)

	def __del__(self):
		self.bus.close()

	def read8(self, reg):
		b = self.bus.read_byte_data(self.accelAddr, reg)
		return b

	def read_block(self, reg, size):
		block = self.bus.read_i2c_block_data(self.accelAddr, reg, size)
		return block

	def write_block(self, reg, data):
		self.bus.write_i2c_block_data(self.accelAddr, reg, data)

	def write8(self, reg, data):
		self.bus.write_byte_data(self.accelAddr, reg, data)

	def getAccel(self):
		pass

	def getMag(self):
		pass

	def get(self):
		# 13 bytes: status, ax,ay, az, mx, my, mz
		# status, axhi, axlo, ayhi, aylo ... mxhi, mxlo ...
		data = self.read_block(0x0, 13)
		# data = self.read_block(FXOS8700_REGISTER_STATUS | 0x80, 13)
		# print('status:', data[0])
		# data = data[1:]
		# self.write8(FXOS8700_REGISTER_STATUS | 0x80)
		# data = self.read_block(0x1, 12)
		# print('raw', data)
		# data = struct.unpack('B'*13, data)[0]
		# print('status:', data[0])
		data = data[1:]
		form = [0]*6
		# print('struct', data)
		for i in range(0, 12, 2):
			form[i//2] = data[i] << 8 | data[i+1]

		accel = form[:3]
		a2 = list(accel)
		for i in range(3):
			a2[i] = a2[i] >> 2
			a2[i] = twos_comp(a2[i], 14) * ACCEL_MG_LSB_2G
		# print('a2:', a2)
		# a2 = bytearray(a2)
		# struct.unpack()
		# accel = [(x >> 2) * ACCEL_MG_LSB_2G for x in accel]  # FIXME: do for other accels

		mag = form[3:]
		mag = [x * MAG_UT_LSB for x in mag]
		print('-'*20)
		print('accel:', a2)
		print('mag:', mag)


if __name__ == "__main__":
	import time
	f = FXOS8700()

	for _ in range(10):
		f.get()
		time.sleep(0.5)
