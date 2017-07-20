#!/usr/bin/env python

from __future__ import division
# from math import atan2, sin, cos, pi
from .FXAS21002 import FXAS21002
from .FXOS8700 import FXOS8700


class IMU(object):
	def __init__(self, dps=250, gs=2, gyro_bw=100, verbose=False):
		"""
		"""
		self.accel = FXOS8700(gs=gs, verbose=verbose)
		self.gyro = FXAS21002(dps=dps, bw=gyro_bw, verbose=verbose)

	def __del__(self):
		"""
		"""
		pass

	def get(self):
		"""
		"""
		accel, mag = self.accel.get()
		gyro = self.gyro.get()
		return (accel, mag, gyro)
