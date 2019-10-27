#!/usr/bin/env python3
# This is AAN4459.pdf on how to calibrate your IMU
# Note the code in the Application note is incomplete

from nxp_imu.FXAS21002 import FXAS21002  # gyros
from nxp_imu.FXOS8700 import FXOS8700    # accels/mags
from math import atan2, pi, sqrt
import struct
import time

# def write8(addr, data):
#     pass

# def read_dev(addr, num):
#     data = self.read_block(addr, num)
#     # > big-endian
#     # h signed short (2 bytes)
#     data = struct.unpack('>{}h'.format(int(num)), data)
#     return data

# def aa_gpio_change(handke, num):
#     pass

# def dev_display_sens_data():
#     data = self.read_block(0x01, 12)

accel = FXOS8700()  # accels/mags    
    

# Initialize debounce counter for reset
autoCalResetCtr = 0

# Issue soft reset
accel.write8(0x2B, 0x40)
time.sleep(0.1)

# Set threshold. 1000 counts = 100.0uT
magThreshold = 1000 # counts
magThresholdHi = (magThreshold & 0xFF00) >> 8
magThresholdLo = magThreshold & 0xFF

accel.write8(0x6A, 0x80 | magThresholdHi)
accel.write8(0x6B, magThresholdLo)

# M_VECM_CNT = 1 * 20ms = 20ms
# ! - steps double in hybrid mode
accel.write8(0x6C, 0x01)

# M_VECM_CFG
# m_vecm_ele = 1 => event latching enabled
# m_vecm_initm = 1 => use M_VECM_INITX/Y/Z as initial reference
# m_vecm_updm = 1 => do not update initial reference
# m_vecm_en = 1 => enable magnetometer vector magnitude detection feature
accel.write8(0x69, 0x7B)

# enable interrupts for DRDY using CTRL_REG4
accel.write8(0x2D, 0x01)

# route interrupts to INT1 pin using CTRL_REG5
accel.write8(0x2E, 0x01)

# Setup device
# via M_CTRL_REG1 (0x5B): Hybrid mode, OS = 32, Auto Cal
# via M_CTRL_REG2 (0x5C): Hybrid auto increment, maxmin disable threshold
# via CTRL_REG1 (0x2A): ODR = 50Hz, ACTIVE mode
accel.write8(0x5B, 0x9F)
accel.write8(0x5C, 0x20)
accel.write8(0x2A, 0x31)

# Wait for INT1 to assert and clear interrupt by reading register INT_SOURCE (0x0C)
# or reading sensor data (0x01...0x06, 0x33...0x38) depending on the function that
# generated the interrupt
# -------------------
# 0x01/2 X accel
# 0x03/4 Y accel
# 0x05/6 Z accel
# -------------------
# 0x33/4 X mag
# 0x35/6 Y mag
# 0x37/8 Z mag
# -------------------

while( True ):
    # Check INT1 pin for interrupts
    # transition = aa_gpio_change( handle, 100 )
#     if (transition & INT1_PIN ) == INT1_PIN:
#         # print "No interrupt..."
#         continue
    time.sleep(1/20)  # don't have access to INT pin
        
    print("\nODR cycle ==============>\n")
    # Check if interrupt is due to Magnetometer Vector Magnitude
    (count, dataIn) = read_dev( 0x5E, 1 )
    if (dataIn[0] & 0x02) == 0x02:
        print("Interrupt due to Magnetometer Vector Magnitude feature")
        print("*** Magnetic Jamming detected ***")
        # Start debounce ctr
        autoCalResetCtr += 1
    else:
        autoCalResetCtr = 0 # reset counter
        
    # Check if interrupt is due to Data Ready (DRDY)
    (count, dataIn) = read_dev( 0x0C, 1 )
    if (dataIn[0] & 0x01) == 0x01:
        print("Interrupt due to data ready")
        (magX, magY, magZ, accX, accY, accZ) = dev_display_sens_data()
        # Apply HAL to match device coordinate system with NED
        # X matches, Z irrelevant
        magY = -magY
        print("Magnetic Vector Magnitude = {4.1f} uT".format(sqrt(magX * magX + magY * magY + magZ * magZ ) / 10))
    
    print("Heading ===> {.2f} degrees from NORTH".format(atan2(-magY, magX ) * (180 / pi))))
    # Reset Auto Cal based on debounce count
    if autoCalResetCtr > 10:
        print("Resetting Hard Iron Estimation...")
        write_dev( 0x5C, [0x24] )
        autoCalResetCtr = 0 # reset counter
