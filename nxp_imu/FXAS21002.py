#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from math import pi
import time
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

GYRO_RANGE_250DPS  = 250
GYRO_RANGE_500DPS  = 500
GYRO_RANGE_1000DPS = 1000
GYRO_RANGE_2000DPS = 2000

GYRO_STANDBY = 0
GYRO_READY   = 1
GYRO_ACTIVE  = 2

# ODR bandwidth
GYRO_BW_800  = 0
GYRO_BW_400  = (1 << 2)
GYRO_BW_200  = (2 << 2)
GYRO_BW_100  = (3 << 2)
GYRO_BW_50   = (4 << 2)
GYRO_BW_25   = (5 << 2)

# Low Pass Filter settings
GYRO_LPF_HIGH = 0
GYRO_LPF_MED  = (1 << 6)
GYRO_LPF_LOW  = (2 << 6)

SENSORS_DPS_TO_RADS = pi/180


class FXAS21002(I2C):
	def __init__(self, gyro_range, bus=1):
		I2C.__init__(self, address=FXAS21002C_ADDRESS, bus=bus)

		if gyro_range == GYRO_RANGE_250DPS:
			self.scale = GYRO_SENSITIVITY_250DPS
			self.write8(GYRO_REGISTER_CTRL_REG0, 0x03)
		elif gyro_range == GYRO_RANGE_500DPS:
			self.scale = GYRO_SENSITIVITY_500DPS
			self.write8(GYRO_REGISTER_CTRL_REG0, 0x02)
		elif gyro_range == GYRO_RANGE_1000DPS:
			self.scale = GYRO_SENSITIVITY_1000DPS
			self.write8(GYRO_REGISTER_CTRL_REG0, 0x01)
		elif gyro_range == GYRO_RANGE_2000DPS:
			self.scale = GYRO_SENSITIVITY_2000DPS
			self.write8(GYRO_REGISTER_CTRL_REG0, 0x00)
		else:
			raise Exception('Invalid gyro range')

		# if True:
		# 	self.scale *= SENSORS_DPS_TO_RADS

		if self.read8(GYRO_REGISTER_WHO_AM_I) == FXAS21002C_ID:
			print('Found FXAS21002C gyro')
			print('Temperature:', self.temperature())
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
		# self.write8(GYRO_REGISTER_CTRL_REG1, 0x00)  # don't need this?
		# self.write8(GYRO_REGISTER_CTRL_REG1, (1 << 6))  # set bit 6, reset bit
		# self.reset()
		value = GYRO_BW_100 | GYRO_ACTIVE
		self.write8(GYRO_REGISTER_CTRL_REG1, value)  # set 100 Hz Active=true
		time.sleep(0.06)  # 60 ms + 1/ODR

	def setActive(self):
		reg = self.read8(GYRO_REGISTER_CTRL_REG1)
		self.write8(GYRO_REGISTER_CTRL_REG1, reg | 2)

	# FIXME: doesn't work!!
	# def reset(self):
	# 	self.write8(GYRO_REGISTER_CTRL_REG1, (1 << 6))
	# 	time.sleep(0.1)

	def temperature(self):
		"""Return gyro temperature in C, ONLY works in ACTIVE mode"""
		t = self.read8(GYRO_REGISTER_CTRL_REG1)
		# print('intermediate tmp:', t)
		return self.twos_comp(t, 8)

	def get(self):
		# 6 bytes: axhi, axlo, ayhi, aylo, azhi, azlo
		data = self.read_block(0x1, 6)
		# print('i2c', data)
		# data = self.little_endian(data)
		ret = [0]*3
		print('raw', data)
		for i in range(0, 6, 2):
			# data = self.twos_comp(data, 16)
			d = self.little_endian2(data[i], data[i+1])
			# print('d', d)
			ret[i//2] = self.twos_comp(d, 16) * self.scale

		data = ret

		# return tuple(data)
		return data


# if __name__ == "__main__":
# 	f = FXAS21002(GYRO_RANGE_250DPS)
#
# 	for _ in range(10):
# 		f.get()
# 		time.sleep(0.5)
