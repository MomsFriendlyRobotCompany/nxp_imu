from __future__ import print_function
from __future__ import division
from nxp_imu.FXAS21002 import FXAS21002
from nxp_imu.FXOS8700 import FXOS8700
from math import sin, cos, atan2, pi, sqrt
from threading import Thread, Event
import time


def rad2deg(x): return x*180/pi
def deg2rad(x): return x*pi/180


class IMU(object):
    def __init__(self, dps=250, gs=2, gyro_bw=100, verbose=False):
        """
        """
        self.accel = FXOS8700(gs=gs, verbose=verbose)
        self.gyro = FXAS21002(dps=dps, bw=gyro_bw, verbose=verbose)
        self.bias_a = None
        self.bias_g = None
        self.bias_m = None

    def __del__(self):
        """
        """
        pass

    def setBias(self, a, m, g):
        """
        Set the bias for accel, mag, and/or gyro. If you do
        not want to set a bias correction for a sensor, just
        pass None.
        """
        if a and len(a) == 3:
            self.bias_a = a

        if m and len(m) == 3:
            self.bias_m = m

        if g and len(g) == 3:
            self.bias_g = g
           
    def get(self):
        """
        Returns a reading from all 3 sensors. If a bias correction
        was set, then the sensor gets corrected.

        sensor = sensor_raw - bias
        """
        accel, mag = self.accel.get()
        gyro = self.gyro.get()

        if self.bias_a:
            a = self.bias_a
            accel = (accel[0]-a[0],accel[1]-a[1],accel[2]-a[2],)

        if self.bias_g:
            g = self.bias_g
            gyro = (gyro[0]-g[0],gyro[1]-g[1],gyro[2]-g[2],)

        if self.bias_m:
            m = self.bias_m
            mag = (mag[0]-m[0], mag[1]-m[1], mag[2]-m[2],)

        return (accel, mag, gyro)

    def getOrientation(self, accel, mag, deg=False):
        """
        From AN4248.pdf
        roll: eqn 13
        pitch: eqn 15
        heading: eqn 22

        Args with biases removed:
            accel: g's
            mag: uT

        Return:
            roll, pitch, heading
        """
        ax, ay, az = self.normalize(*accel)
        mx, my, mz = self.normalize(*mag)

        roll = atan2(ay, az)
        pitch = atan2(-ax, ay*sin(roll)+az*cos(roll))
        heading = atan2(
            mz*sin(roll) - my*cos(roll),
            mx*cos(pitch) + my*sin(pitch)*sin(roll) + mz*sin(pitch)*cos(roll)
        )

#         heading = heading if heading >= 0.0 else 2*pi + heading
#         heading = heading if heading <= 2*pi else heading - 2*pi
        heading %= (2*pi)

        if deg:
            r2d = 180/pi
            roll *= r2d
            pitch *= r2d
            heading *= r2d

        return (roll, pitch, heading,)

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
        This is a threaded IMU driver.

        value?
        add filter to thread?
        """
        IMU.__init__(self, dps=250, gs=2, gyro_bw=100, verbose=False)
        self.shutting_down = False
        self.accel = (0,0,0,)
        self.mag = (0,0,0,)
        self.gyro = (0,0,0,)
        self.filter = None

    def __del__(self):
        self.stop()

    def get(self):
        return (self.accel, self.mag, self.gyro,)

    def run(self, hertz):
        """Data capture thread"""
        rate = Rate(hertz)
        while not self.shutting_down:
            self.accel, self.mag = self.accel.get()
            self.gyro = self.gyro.get()

            rate.sleep()

    def start(self, hertz):
        """Start thread"""
        self.thread = Thread(
            name='imu_thread',
            target=self.run,
            args=(hertz,))

    def stop(self, timeout=0.1):
        """Stop thread"""
        self.shutting_down = True
        self.thread.join(timeout)
        if self.thread.is_alive():
            self.thread.terminate()
