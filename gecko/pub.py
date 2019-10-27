#!/usr/bin/env python

if 1:
    import sys
    import fake_rpi

    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
    sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)

from pygeckopb import Imu, protobufPack
from pygecko.multiprocessing import geckopy
from pygecko.transport.zmq_sub_pub import Pub
from nxp_imu import IMU
import time
from squaternion import euler2quat, Quaternion


if __name__ == "__main__":
    geckopy.init_node()
    pub = Pub()
    pub.bind()
    rate = geckopy.Rate(20)
    imu = IMU(gs=2, dps=2000, verbose=False)
    imu.setBias((0.1, -0.02, .25), None, None)

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

        r, p, h = imu.getOrientation(a, m)
        q = euler2quat(r, p, h, degrees=True)
        msg.orientation.w = q.w
        msg.orientation.x = q.x
        msg.orientation.y = q.y
        msg.orientation.z = q.z

        pub.publish(protobufPack(msg))

        rate.sleep()
