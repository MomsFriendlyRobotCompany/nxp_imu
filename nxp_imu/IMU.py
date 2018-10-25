from __future__ import print_function
from __future__ import division
# from math import atan2, sin, cos, pi
from nxp_imu.FXAS21002 import FXAS21002
from nxp_imu.FXOS8700 import FXOS8700
from math import sin, cos, atan2, pi, sqrt, asin
# from math import radians as deg2rad
# from math import degrees as rad2deg
from thread import Thread, Event
import time


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


class Rate(object):
    """
    Uses sleep to keep a desired message/sample rate.
    """
    def __init__(self, hertz):
        self.last_time = time.time()
        self.dt = 1/hertz

    def sleep(self):
        """
        This uses sleep to delay the function. If your loop is faster than your
        desired Hertz, then this will calculate the time difference so sleep
        keeps you close to you desired hertz. If your loop takes longer than
        your desired hertz, then it doesn't sleep.
        """
        diff = time.time() - self.last_time
        if self.dt > diff:
            time.sleep(self.dt - diff)

        # now that we hav slept a while, set the current time
        # as the last time
        self.last_time = time.time()


class ThreadedIMU(IMU):
    def __init__(self, dps=250, gs=2, gyro_bw=100, verbose=False):
        """
        """
        IMU.__init__(self, dps=250, gs=2, gyro_bw=100, verbose=False)
        self.shutting_down = False
        self.accel = (0,0,0,)
        self.mag = (0,0,0,)
        self.gyro = (0,0,0,)

    def __del__(self):
        self.stop()

    def get(self):
        return (self.accel, self.mag, self.gyro,)

    def run(self, hertz):
        rate = Rate(hertz)
        while not self.shutting_down:
            self.accel, self.mag = self.accel.get()
            self.gyro = self.gyro.get()

            rate.sleep()

    def start(self, hertz):
        self.thread = Thread(
            name='imu_thread',
            target=self.run,
            args=(hertz,))

    def stop(self, timeout=0.1):
        self.shutting_down = True
        self.thread.join(timeout)
        if self.thread.is_alive():
            self.thread.terminate()
