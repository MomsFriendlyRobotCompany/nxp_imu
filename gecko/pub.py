#!/usr/bin/env python

# if 1:
#     import sys
#     import fake_rpi
#     from fake_rpi.smbus import SMBus as fakeSMBus
#
#     class SMBus(fakeSMBus):
#         resp = {
#             0x21: 0xD7,
#             0x1F: 0xC7
#         }
#
#         # @printf
#         def read_byte_data(self, i2c_addr, register):
#             return self.resp[i2c_addr]
# #             ret = 0xff
# #             if i2c_addr == 0x21:
# #                     ret = 0xD7
# #             elif i2c_addr == 0x1F:
# #                     ret = 0xC7
# #             return ret
#
#     sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
#     # sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)
#     sys.modules['smbus2'] = SMBus # Fake smbus (I2C)

from pygeckopb import Imu, protobufPack
from pygecko.multiprocessing import geckopy
from pygecko.transport.zmq_sub_pub import Pub
from pygecko.transport.zmq_base import zmqUDS
from nxp_imu import IMU
# import time
from squaternion import euler2quat
# from squaternion import Quaternion
import os

if 1:
    from fake_rpi import toggle_print
    toggle_print(False) 


if __name__ == "__main__":
    if 'TRAVIS' in os.environ:
        print(">> FOUND TRAVIS\n\n")
    geckopy.init_node()
    pub = Pub()
    pub.bind(zmqUDS('/tmp/uds-lidar'))
    rate = geckopy.Rate(20)
    imu = IMU(gs=2, dps=2000, verbose=False)
    imu.setBias((0.1, -0.02, .25), None, None)

    msg = Imu()

    while not geckopy.is_shutdown():
        a, m, g = imu.get()

        msg.linear_acceleration.x = a[0]
        msg.linear_acceleration.y = a[1]
        msg.linear_acceleration.z = a[2]

        msg.angular_velocity.x = g[0]
        msg.angular_velocity.y = g[1]
        msg.angular_velocity.z = g[2]

        msg.magnetic_field.x = m[0]
        msg.magnetic_field.y = m[1]
        msg.magnetic_field.z = m[2]

        r, p, h = imu.getOrientation(a, m)
        q = euler2quat(r, p, h, degrees=True)
        msg.orientation.w = q.w
        msg.orientation.x = q.x
        msg.orientation.y = q.y
        msg.orientation.z = q.z

        print(msg)

        pub.publish(protobufPack(msg))

        rate.sleep()
