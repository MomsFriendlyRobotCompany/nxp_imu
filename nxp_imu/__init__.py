from .FXAS21002 import FXAS21002, GYRO_RANGE_250DPS, GYRO_RANGE_500DPS, GYRO_RANGE_1000DPS, GYRO_RANGE_2000DPS
from .FXOS8700 import FXOS8700, ACCEL_RANGE_2G, ACCEL_RANGE_4G, ACCEL_RANGE_8G
from .I2C import I2C
from .IMU import IMU
from .AHRS import AHRS
from .version import __version__


class Namespace(object):
	def __init__(self, **kwds):
		self.__dict__.update(kwds)


__author__ = 'Kevin J. Walchko'
__license__ = 'MIT'
__copyright__ = '2017 Kevin J. Walchko'
