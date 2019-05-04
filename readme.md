![](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/nxp_imu/master/docs/pics/imu-iso.jpg)

# NXP IMU

[![image](https://img.shields.io/pypi/l/nxp_imu.svg)](https://github.com/MomsFriendlyRobotCompany/nxp_imu)
[![image](https://img.shields.io/pypi/pyversions/nxp_imu.svg)](https://github.com/MomsFriendlyRobotCompany/nxp_imu)
[![image](https://img.shields.io/pypi/wheel/nxp_imu.svg)](https://github.com/MomsFriendlyRobotCompany/nxp_imu)
[![image](https://img.shields.io/pypi/v/nxp_imu.svg)](https://github.com/MomsFriendlyRobotCompany/nxp_imu)
[![image](https://travis-ci.org/MomsFriendlyRobotCompany/nxp_imu.svg?branch=master)](https://travis-ci.org/MomsFriendlyRobotCompany/nxp_imu)

Python drivers for [Adafruit Precision NXP
9-DOF](https://www.adafruit.com/product/3463). This is basically a
python version of Adafruit\'s
[FXOS8700](https://github.com/adafruit/Adafruit_FXOS8700) and their
[FXAS21002C](https://github.com/adafruit/Adafruit_FXAS21002C) written in
C++ for the Arduino.

## NXP Precision 9DoF

The board consists of two separate ICs, described below:

**FXOS8700 3-Axis Accelerometer/Magnetometer**

-   2-3.6V Supply
-   ±2 g/±4 g/±8 g adjustable acceleration range
-   ±1200 µT magnetic sensor range
-   Output data rates (ODR) from 1.563 Hz to 800 Hz
-   14-bit ADC resolution for acceleration measurements
-   16-bit ADC resolution for magnetic measurements

**FXAS21002 3-Axis Gyroscope**

-   2-3.6V Supply
-   ±250/500/1000/2000°/s configurable range
-   Output Data Rates (ODR) from 12.5 to 800 Hz
-   16-bit digital output resolution
-   192 bytes FIFO buffer (32 X/Y/Z samples)

## Setup

![](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/nxp_imu/master/docs/pics/imu-front.jpg)

![](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/nxp_imu/master/docs/pics/imu-back.jpg)

[Adafruit setup
tutorial](https://learn.adafruit.com/nxp-precision-9dof-breakout?view=all)

## Usage

Verifying it is there:

```
sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 1f 
20: -- 21 -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --    
```

See the `examples` folder, but to have the IMU run at 4G and 2000
degrees per second:

```python
#!/usr/bin/env python3

from __future__ import division, print_function
from nxp_imu import IMU
import time

imu = IMU(gs=4, dps=2000, verbose=True)
header = 67
print('-'*header)
print("| {:17} | {:20} | {:20} |".format("Accels [g's]", " Magnet [uT]", "Gyros [dps]"))
print('-'*header)
for _ in range(10):
    a, m, g = imu.get()
    print('| {:>5.2f} {:>5.2f} {:>5.2f} | {:>6.1f} {:>6.1f} {:>6.1f} | {:>6.1f} {:>6.1f} {:>6.1f} |'.format(
        a[0], a[1], a[2],
        m[0], m[1], m[2],
        g[0], g[1], g[2])
    )
    time.sleep(0.50)
print('-'*header)
print(' uT: micro Tesla')
print('  g: gravity')
print('dps: degrees per second')
print('')
```

## Examples

```
pi@nav examples $ ./test.py 

========================================
FXOS8700
  Accelerometer:
    Addr: 0x1F
    Range: +/- 2 G
  Magnetometer:
    Range: +/- 1200
  Temperature: 0 C
========================================
FXAS21002C Gyro
  Addr: 0x21
  Range: +/- 250dps
  Temperature: 10 C
-----------------------------------------------
| Accels [g's]         | Orient(r,p,h) [deg]  |
-----------------------------------------------
|    0.0   -0.0    1.0 |   -0.0   -0.0    3.0 |
|    0.0   -0.0    1.0 |   -0.0   -0.0    2.9 |
|    0.0   -0.0    1.0 |   -0.0   -0.0    2.9 |
|    0.0   -0.0    1.0 |   -0.0   -0.0    2.9 |
|    0.0   -0.0    1.0 |   -0.0   -0.0    2.9 |
|    0.0   -0.0    1.0 |   -0.0   -0.0    2.9 |
|    0.0   -0.0    1.0 |   -0.0   -0.0    2.9 |
|    0.0   -0.0    1.0 |   -0.0   -0.0    2.9 |
|    0.0   -0.0    1.0 |   -0.0   -0.0    2.9 |
|    0.0   -0.0    1.0 |   -0.0   -0.0    2.9 |
-----------------------------------------------
  r: roll
  p: pitch
  h: heading
  g: gravity
deg: degree

========================================
FXOS8700
  Accelerometer:
    Addr: 0x1F
    Range: +/- 4 G
  Magnetometer:
    Range: +/- 1200
  Temperature: 25 C
========================================
FXAS21002C Gyro
  Addr: 0x21
  Range: +/- 2000dps
  Temperature: 10 C
-------------------------------------------------------------------
| Accels [g's]      |  Magnet [uT]         | Gyros [dps]          |
-------------------------------------------------------------------
|  0.04 -0.04  1.02 |  -21.5   -4.7    8.3 |    0.8   -1.4   -0.2 |
|  0.04 -0.04  1.03 |  -21.6   -5.3    8.3 |    1.2   -1.1   -0.4 |
|  0.04 -0.04  1.02 |  -21.9   -4.4   10.5 |    0.4   -0.9   -0.1 |
|  0.04 -0.04  1.02 |  -21.5   -4.8    9.9 |    1.3   -1.2    0.1 |
|  0.04 -0.04  1.02 |  -22.4   -4.9    8.7 |    1.2   -0.8   -0.2 |
|  0.04 -0.04  1.02 |  -21.7   -5.4    8.5 |    0.2   -1.6    0.0 |
|  0.04 -0.04  1.03 |  -21.9   -4.7    8.1 |    1.2   -1.2   -0.4 |
|  0.04 -0.04  1.02 |  -22.2   -4.4   10.0 |    1.5   -1.5   -0.1 |
|  0.04 -0.04  1.02 |  -22.2   -5.7    9.1 |    0.5   -1.2   -0.4 |
|  0.04 -0.04  1.02 |  -22.3   -5.0    8.0 |    0.7   -1.4   -0.6 |
-------------------------------------------------------------------
 uT: micro Tesla
  g: gravity
dps: degrees per second

Done ...
```

## Documents

The `/docs` folder has the datasheets for both the accel/magnetometer
and the gyros.

# MIT License

**Copyright (c) 2017 Kevin J. Walchko**

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
