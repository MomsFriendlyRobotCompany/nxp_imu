#!/usr/bin/env python

from __future__ import division, print_function
from nxp_imu import FXAS21002, FXOS8700
# from nxp.FXAS21002 import GYRO_RANGE_250DPS
# from nxp_imu.I2C import I2C
# from nxp.IMU import IMU
# from nxp.AHRS import AHRS


def test_dummy():
	assert True

# def test_2comp():
# 	i2c = I2C(30)
# 	xx = [0, 127, 128, 255]
# 	yy = [0, 127, -128, -1]
#
# 	for x, ans in zip(xx, yy):
# 		y = i2c.twos_comp(x, 8)
# 		assert y == ans


# def test_accel():
# 	try:
# 		a = FXOS8700()
# 		assert True
# 	except Exception:
# 		assert False
#
#
# def test_gyro():
# 	try:
# 		g = FXAS21002(250)
# 		assert True
# 	except Exception:
# 		assert False
