#!/usr/bin/env python

if 1:
    import sys
    import fake_rpi

    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
    sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

from pygeckopb import Imu, protobufPack
from nxp_imu import IMU
import time


if __name__ == "__main__":
    geckopy.init_node()
    pub = Publisher()
    pub.bind()
    rate = geckopy.Rate(20)
    imu = IMU(gs=2, dps=2000, verbose=False)

    msg = Imu()

    while not geckopy.is_shutdown():
        a, m, g = imu.get()

        msg.linear_acceleration.x = a.x
        msg.linear_acceleration.y = a.y
        msg.linear_acceleration.z = a.z

        msg.angular_velocity.x = g.x
        msg.angular_velocity.y = g.y
        msg.angular_velocity.z = g.z

        msg.magnetic_field.x = m.x
        msg.magnetic_field.y = m.y
        msg.magnetic_field.z = m.z

        # r, p, h = imu.getOrientation(a, m)
        # msg.orientation.w =

        pub.publish(protobufPack(msg))

        rate.sleep()
