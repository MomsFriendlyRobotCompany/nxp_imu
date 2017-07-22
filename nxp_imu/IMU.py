#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# from math import atan2, sin, cos, pi
from .FXAS21002 import FXAS21002
from .FXOS8700 import FXOS8700
from math import sin, cos, atan2, pi, sqrt, asin
# from math import radians as deg2rad
# from math import degrees as rad2deg


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

	def getOrientation(self, accel, mag, deg=True):
		ax, ay, az = self.normalize(*accel)
		mx, my, mz = self.normalize(*mag)

		roll = atan2(ay, az)
		pitch = atan2(-ax, ay*sin(roll)+az*cos(roll))

		heading = atan2(
			mz*sin(roll) - my*cos(roll),
			mx*cos(pitch) + my*sin(pitch)*sin(roll) + mz*sin(pitch)*cos(roll)
		)

		if deg:
			roll *= 180/pi
			pitch *= 180/pi
			heading *= 180/pi

			heading = heading if heading >= 0.0 else 360 + heading
			heading = heading if heading <= 360 else heading - 360
		else:
			heading = heading if heading >= 0.0 else 2*pi + heading
			heading = heading if heading <= 2*pi else heading - 2*pi

		return (roll, pitch, heading)

	def normalize(self, x, y, z):
		"""Return a unit vector"""
		norm = sqrt(x * x + y * y + z * z)
		if norm > 0.0:
			inorm = 1/norm
			x *= inorm
			y *= inorm
			z *= inorm
		else:
			raise Exception('division by zero: {} {} {}'.format(x, y, z))
		return (x, y, z)
