
try:
    from importlib_metadata import version # type: ignore
except ImportError:
    from importlib.metadata import version # type: ignore

from nxp_imu.I2C import I2C
from nxp_imu.IMU import IMU


__version__ = version("nxp_imu")
__author__ = 'Kevin J. Walchko'
__license__ = 'MIT'
__copyright__ = '2017 Kevin J. Walchko'
