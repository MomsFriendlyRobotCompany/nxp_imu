#!/usr/bin/env python

from __future__ import division, print_function
from nxp_imu import FXAS21002, FXOS8700
from nxp_imu.FXAS21002 import GYRO_RANGE_250DPS
from nxp_imu import I2C
from nxp_imu import IMU
from nxp_imu import AHRS
import time


def gyro():
	f = FXAS21002(GYRO_RANGE_250DPS)

	for _ in range(10):
		data = f.get()
		print('x y z:', *data)
		time.sleep(0.5)


def accel():
	f = FXOS8700()

	for _ in range(10):
		f.get()
		time.sleep(0.5)


def t():
	i2c = I2C(30)
	for i in range(256):
		a = i2c.twos_comp(i, 8)
		print(i, '>>', a)


def a():
	imu = IMU()
	ahrs = AHRS(True)

	for _ in range(10):
		a, m, _ = imu.get()
		r, p, h = ahrs.getOrientation(a, m)
		print(' >> ', r, p, h)
		time.sleep(1.0)


if __name__ == "__main__":
	# gyro()
	# accel()
	# t()
	a()
	print('Done ...')
