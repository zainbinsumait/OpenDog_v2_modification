
from __future__ import print_function

import odrive
from odrive.utils import dump_errors
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
odrv0 = odrive.find_any() 

#clear the errors in the system 
odrv0.clear_errors() 

# To read a value, simply read the property
print("Bus voltage is " + str(odrv0.vbus_voltage) + "V")

##calibration motors 
odrv0.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
odrv0.axis1.requested_state = AXIS_STATE_MOTOR_CALIBRATION
time.sleep(4)
if odrv0.axis0.motor.is_calibrated == 1: #if the motor is calibrated successfully
	print("Motor 0 successfully calibrated! Proceeding...")
else:
	print("Could not calibrate motor 0. Something is wrong.")
	print("Have you ran the first script to set all parameters?")
	print("If yes and the wiring looks good, reset the ODrive and try again.\nExiting.")
	quit()

if odrv0.axis1.motor.is_calibrated == 1:
	print("Motor 1 successfully calibrated! Proceeding...")
else:
	print("Could not calibrate motor 1. Something is wrong.")
	print("Have you ran the first script to set all parameters?")
	print("If yes and the wiring looks good, reset the ODrive and try again.\nExiting.")
	quit()
	
##calibration encoders
print("starting encoder calibration of the upper leg...")
odrv0.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
while odrv0.axis1.current_state != AXIS_STATE_IDLE:
	time.sleep(0.1)
	print("waiting ..")

print("starting encoder calibration of the lower leg...")
odrv0.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
while odrv0.axis1.current_state != AXIS_STATE_IDLE:
	time.sleep(0.1)
	print("waiting ..")

if odrv0.axis0.encoder.is_ready == 1 and odrv0.axis1.encoder.is_ready == 1:
	print("encoder 0 and 1 are ready ..")

print(dump_errors(odrv0)) #print the state of the system and affiche the errors if there is any
