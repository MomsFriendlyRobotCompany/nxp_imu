#!/usr/bin/env python

from math import atan2, sin, cos, pi
from .FXAS21002 import FXAS21002
from .FXOS8700 import FXOS8700


class IMU(object):
	def __init__(self):
		self.accel = FXOS8700()
		self.gyro = FXAS21002()
		# self.mag = Mag()

	def __del__(self):
		pass

	def getRaw(self):
		accel, mag = self.accel.get()
		gyro = self.accel.get()
		return (accel, mag, gyro)


class AHRS(object):
	def __init__(self, deg=False):
		self.deg = deg

	def getOrientation(self, accel, mag):
		# roll: Rotation around the X-axis. -180 <= roll <= 180
		# a positive roll angle is defined to be a clockwise rotation about the positive X-axis
		#
		#                    y
		#      roll = atan2(---)
		#                    z
		#
		# where:  y, z are returned value from accelerometer sensor
		# roll = atan2(accel_event.acceleration.y, accel_event.acceleration.z);
		roll = atan2(accel[1], accel[2])

		# pitch: Rotation around the Y-axis. -180 <= roll <= 180
		# a positive pitch angle is defined to be a clockwise rotation about the positive Y-axis
		#
		#                                 -x
		#      pitch = atan(-------------------------------)
		#                    y * sin(roll) + z * cos(roll)
		#
		# where:  x, y, z are returned value from accelerometer sensor
		# if (accel_event.acceleration.y * sin(orientation->roll) + accel_event.acceleration.z * cos(orientation->roll) == 0)
		# orientation->pitch = accel_event.acceleration.x > 0 ? (PI_F / 2) : (-PI_F / 2);
		# else
		# orientation->pitch = (float)atan(-accel_event.acceleration.x / (accel_event.acceleration.y * sin(orientation->roll) + \
																		#  accel_event.acceleration.z * cos(orientation->roll)));
		# if accel[1]*sin(roll)+accel[2]*cos(roll) == 0:
			# pitch = pi/2 if accel[0] > 0 else -pi/2
		# else:

		# atan2 checks bounds
		pitch = atan2(-accel[0], accel[1]*sin(roll)+accel[2]*cos(roll))
		# heading: Rotation around the Z-axis. -180 <= roll <= 180
		# a positive heading angle is defined to be a clockwise rotation about the positive Z-axis
		#
		#                                       z * sin(roll) - y * cos(roll)
		#   heading = atan2(--------------------------------------------------------------------------)
		#                    x * cos(pitch) + y * sin(pitch) * sin(roll) + z * sin(pitch) * cos(roll))
		#
		# where:  x, y, z are returned value from magnetometer sensor
		# orientation->heading = (float)atan2(mag_event.magnetic.z * sin(orientation->roll) - mag_event.magnetic.y * cos(orientation->roll), \
		#									  mag_event.magnetic.x * cos(orientation->pitch) + \
		#									  mag_event.magnetic.y * sin(orientation->pitch) * sin(orientation->roll) + \
		#									  mag_event.magnetic.z * sin(orientation->pitch) * cos(orientation->roll));

		heading = atan2(
			mag[2]*sin(roll) - mag[1]*cos(roll),
			mag[0]*cos(pitch) + mag[1]*sin(pitch)*sin(roll) + mag[2]*sin(pitch)*cos(roll)
		)
		# Convert angular data to degree
		# orientation->roll = orientation->roll * 180 / PI_F;
		# orientation->pitch = orientation->pitch * 180 / PI_F;
		# orientation->heading = orientation->heading * 180 / PI_F;
		if self.deg:
			roll *= 180/pi
			pitch *= 180/pi
			heading *= 180/pi

		return (roll, pitch, heading)


if __name__ == "__main__":
	import time
	imu = IMU()
	ahrs = AHRS()

	for _ in range(10):
		a, m, _ = imu.get()
		r, p, h = ahrs.getOrientation(a, m)
		print('>> ', r, p, h)
		time.sleep(1.0)
