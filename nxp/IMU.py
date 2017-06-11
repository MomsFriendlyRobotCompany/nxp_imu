#!/usr/bin/env python

from __future__ import division
# from math import atan2, sin, cos, pi
from .FXAS21002 import FXAS21002
from .FXOS8700 import FXOS8700


class IMU(object):
	def __init__(self, dps=250):
		"""
		"""
		self.accel = FXOS8700()
		self.gyro = FXAS21002(dps)

	def __del__(self):
		"""
		"""
		pass

	def get(self):
		"""
		"""
		accel, mag = self.accel.get()
		gyro = self.accel.get()
		return (accel, mag, gyro)
