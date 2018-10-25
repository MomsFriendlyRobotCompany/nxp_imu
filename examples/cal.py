#!/usr/bin/env python3
# This is AAN4459.pdf on how to calibrate your IMU

from nxp_imu.FXAS21002 import FXAS21002
from nxp_imu.FXOS8700 import FXOS8700
from math import sin, cos, atan2, pi, sqrt, asin

def write_byte(b):
    pass

# Initialize debounce counter for reset
autoCalResetCtr = 0
# Issue soft reset
write_byte( [0x2B, 0x40] )
time.sleep(0.1)
# Set threshold. 1000 counts = 100.0uT
magThreshold = 1000 # counts
magThresholdHi = (magThreshold & 0xFF00) >> 8
magThresholdLo = magThreshold & 0xFF
write_byte( [0x6A, 0x80 | magThresholdHi] )
write_byte( [0x6B, magThresholdLo] )
# M_VECM_CNT = 1 * 20ms = 20ms
# ! - steps double in hybrid mode
write_byte( [0x6C, 0x01] )
# M_VECM_CFG
# m_vecm_ele = 1 => event latching enabled
# m_vecm_initm = 1 => use M_VECM_INITX/Y/Z as initial reference
# m_vecm_updm = 1 => do not update initial reference
# m_vecm_en = 1 => enable magnetometer vector magnitude detection feature
write_byte( [0x69, 0x7B] )
# enable interrupts for DRDY using CTRL_REG4
write_byte( [0x2D, 0x01] )
# route interrupts to INT1 pin using CTRL_REG5
write_byte( [0x2E, 0x01] )
# Setup device
# via M_CTRL_REG1 (0x5B): Hybrid mode, OS = 32, Auto Cal
# via M_CTRL_REG2 (0x5C): Hybrid auto increment, maxmin disable
# threshold
# via CTRL_REG1 (0x2A): ODR = 50Hz, ACTIVE mode
write_byte( [0x5B, 0x9F] )
write_byte( [0x5C, 0x20] )
write_byte( [0x2A, 0x31] )
# Wait for INT1 to assert and clear interrupt by reading register INT_SOURCE (0x0C)
# or reading sensor data (0x01...0x06, 0x33...0x38) depending on the function that
# generated the interrupt
while( True ):
# Check INT1 pin for interrupts
transition = aa_gpio_change( handle, 100 )
if (transition & INT1_PIN ) == INT1_PIN:
# print "No interrupt..."
continue
print "\nODR cycle ==============>\n"
# Check if interrupt is due to Magnetometer Vector Magnitude
(count, dataIn) = read_dev( 0x5E, 1 )
if dataIn[0] & 0x02 == 0x02:
print "Interrupt due to Magnetometer Vector Magnitude feature"
print "Magnetic Jamming detected"
# Start debounce ctr
autoCalResetCtr = autoCalResetCtr + 1
else:
autoCalResetCtr = 0 # reset counter
# Check if interrupt is due to Data Ready (DRDY)
(count, dataIn) = read_dev( 0x0C, 1 )
if dataIn[0] & 0x01 == 0x01:
print "Interrupt due to data ready"
(magX, magY, magZ, accX, accY, accZ) = dev_display_sens_data()
# Apply HAL to match device coordinate system with NED
# X matches, Z irrelevant
magY = -magY
print "Magnetic Vector Magnitude = %4.1f uT" % (math.sqrt(magX * magX + magY * magY + magZ * magZ ) / 10)
print "Heading ===> %.2f degrees from NORTH" % (math.atan2(
-magY, magX ) * (180 / math.pi))
# Reset Auto Cal based on debounce count
if autoCalResetCtr > 10:
print "Resetting Hard Iron Estimation..."
write_dev( 0x5C, [0x24] )
autoCalResetCtr = 0 # reset counter
