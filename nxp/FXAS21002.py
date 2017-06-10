#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from smbus2 import SMBus
import time

FXAS21002C_ADDRESS       = 0x21       # 0100001
FXAS21002C_ID            = 0xD7       # 1101 0111
GYRO_SENSITIVITY_250DPS  = 0.0078125  # Table 35 of datasheet
GYRO_SENSITIVITY_500DPS  = 0.015625   # ..
GYRO_SENSITIVITY_1000DPS = 0.03125    # ..
GYRO_SENSITIVITY_2000DPS = 0.0625     # ..

GYRO_REGISTER_STATUS              = 0x00
GYRO_REGISTER_OUT_X_MSB           = 0x01
GYRO_REGISTER_OUT_X_LSB           = 0x02
GYRO_REGISTER_OUT_Y_MSB           = 0x03
GYRO_REGISTER_OUT_Y_LSB           = 0x04
GYRO_REGISTER_OUT_Z_MSB           = 0x05
GYRO_REGISTER_OUT_Z_LSB           = 0x06
GYRO_REGISTER_WHO_AM_I            = 0x0C   # 11010111   r
GYRO_REGISTER_CTRL_REG0           = 0x0D   # 00000000   r/w
GYRO_REGISTER_CTRL_REG1           = 0x13   # 00000000   r/w
GYRO_REGISTER_CTRL_REG2           = 0x14   # 00000000   r/w

GYRO_RANGE_250DPS  = 250
GYRO_RANGE_500DPS  = 500
GYRO_RANGE_1000DPS = 1000
GYRO_RANGE_2000DPS = 2000

# horrible global
# g_i2c = SMBus(1)


class I2C(object):
	def __init__(self, address, bus=1):
		self.i2c = SMBus(bus)
		# self.i2c = g_i2c
		self.address = address

	def __del__(self):
		self.bus.close()

	def read8(self, reg):
		b = self.bus.read_byte_data(self.address, reg)
		return b

	def read_block(self, reg, size):
		block = self.bus.read_i2c_block_data(self.address, reg, size)
		return block

	def write_block(self, reg, data):
		self.bus.write_i2c_block_data(self.address, reg, data)

	def write8(self, reg, data):
		self.bus.write_byte_data(self.address, reg, data)

	def little_endian(self, data):
		size = len(data)
		form = [0]*size
		for i in range(0, size, 2):
			form[i//2] = data[i] << 8 | data[i+1]
		return form


class FXAS21002(I2C):
	def __init__(self, gyro_range):
		I2C.__init__(self, FXAS21002C_ADDRESS)

		if range == GYRO_RANGE_250DPS:
			self.scale = GYRO_RANGE_250DPS
		elif range == GYRO_RANGE_500DPS:
			self.scale = GYRO_RANGE_500DPS
		elif range == GYRO_RANGE_1000DPS:
			self.scale = GYRO_RANGE_1000DPS
		elif range == GYRO_RANGE_2000DPS:
			self.scale = GYRO_RANGE_2000DPS
		else:
			raise Exception('Invalid gyro range')

		if True:
			self.scale *= SENSORS_DPS_TO_RADS

		if self.read8(GYRO_REGISTER_WHO_AM_I) == FXAS21002C_ID:
			print('Found FXAS21002C gyro')
		else:
			raise Exception('Could not find FXAS21002C gyro')

		"""
		Set CTRL_REG1 (0x13)
		====================================================================
		BIT  Symbol    Description                                   Default
		---  ------    --------------------------------------------- -------
		6  RESET     Reset device on 1                                   0
		5  ST        Self test enabled on 1                              0
		4:2  DR        Output data rate                                  000
					  000 = 800 Hz
					  001 = 400 Hz
					  010 = 200 Hz
					  011 = 100 Hz
					  100 = 50 Hz
					  101 = 25 Hz
					  110 = 12.5 Hz
					  111 = 12.5 Hz
		1  ACTIVE    Standby(0)/Active(1)                                0
		0  READY     Standby(0)/Ready(1)                                 0
		"""
		# Reset then switch to active mode with 100Hz output
		self.write8(GYRO_REGISTER_CTRL_REG1, 0x00)
		self.write8(GYRO_REGISTER_CTRL_REG1, (1 << 6))
		self.write8(GYRO_REGISTER_CTRL_REG1, 0x0E)
		time.sleep(100)  # 60 ms + 1/ODR

	def get(self):
		# 6 bytes: axhi, axlo, ayhi, aylo, azhi, azlo
		data = self.read_block(0x1, 6)
		data = self.little_endian(data)

		scale = self.scale

		data[0] *= scale
		data[1] *= scale
		data[2] *= scale


if __name__ == "__main__":
	import time
	f = FXAS21002()

	for _ in range(10):
		f.get()
		time.sleep(0.5)
