import sys
import fake_rpi

# dummy will return the correct response to make it
# look like a real IMU
import dummy as smbus
sys.modules['smbus2'] = smbus #SMBus # Fake smbus (I2C)

from nxp_imu.FXAS21002 import FXAS21002
from nxp_imu.FXOS8700 import FXOS8700
from nxp_imu.FXAS21002 import GYRO_RANGE_250DPS
from nxp_imu.I2C import I2C
from nxp_imu.IMU import IMU


def test_dummy():
    assert True


def test_2comp():
    i2c = I2C(30)
    xx = [0, 127, 128, 255]
    yy = [0, 127, -128, -1]


def test_accel():
    try:
        a = FXOS8700()
        assert True
    except Exception as e:
        assert False, f"FXOS8700:{e}"


def test_gyro():
    try:
        g = FXAS21002(250)
        assert True
    except Exception as e:
        assert False, f"FXAS21002: {e}"
