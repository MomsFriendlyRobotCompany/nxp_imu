.. figure:: https://raw.githubusercontent.com/MomsFriendlyRobotCompany/adafruit-precision-nxp-9-dof/master/docs/pics/imu-iso.jpg
    :align: center


NXP IMU
==============================

Python drivers for `Adafruit Precision NXP 9-DOF <https://www.adafruit.com/product/3463>`_.
This is basically a python version of Adafruit's `FXOS8700 <https://github.com/adafruit/Adafruit_FXOS8700>`_
and their `FXAS21002C <https://github.com/adafruit/Adafruit_FXAS21002C>`_ written
in C++ for the Arduino.

NXP Precision 9DoF
---------------------

The board consists of two separate ICs, described below:

**FXOS8700 3-Axis Accelerometer/Magnetometer**

- 2-3.6V Supply
- ±2 g/±4 g/±8 g adjustable acceleration range
- ±1200 µT magnetic sensor range
- Output data rates (ODR) from 1.563 Hz to 800 Hz
- 14-bit ADC resolution for acceleration measurements
- 16-bit ADC resolution for magnetic measurements

**FXAS21002 3-Axis Gyroscope**

- 2-3.6V Supply
- ±250/500/1000/2000°/s configurable range
- Output Data Rates (ODR) from 12.5 to 800 Hz
- 16-bit digital output resolution
- 192 bytes FIFO buffer (32 X/Y/Z samples)

Setup
--------

.. figure:: https://raw.githubusercontent.com/MomsFriendlyRobotCompany/adafruit-precision-nxp-9-dof/master/docs/pics/imu-front.jpg

.. figure:: https://raw.githubusercontent.com/MomsFriendlyRobotCompany/adafruit-precision-nxp-9-dof/master/docs/pics/imu-back.jpg

`Adafruit setup tutorial <https://learn.adafruit.com/nxp-precision-9dof-breakout?view=all>`_

Documents
------------

The ``/docs`` folder has the datasheets for both the accel/magnetometer and the
gyros.

MIT License
===============

**Copyright (c) 2017 Kevin J. Walchko**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Misc
-----

git config --global core.ignorecase false
