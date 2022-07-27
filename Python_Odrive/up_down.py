
from __future__ import print_function

import odrive
from odrive.utils import dump_errors
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
odrv0 = odrive.find_any()

odrv0.clear_errors()

	 	
print("motor 0 : starting closed loop control...")
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

print("motor 1 : starting closed loop control...")
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

print("changing to passthrough...")
odrv0.axis1.controller.config.input_mode = INPUT_MODE_POS_FILTER
#odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
# PASSTHROUGH mode is without any control so it's very fast
odrv0.axis0.controller.config.input_mode = INPUT_MODE_POS_FILTER
odrv0.axis0.controller.config.input_filter_bandwidth = 3
odrv0.axis1.controller.config.input_filter_bandwidth = 3

##PID
#here we can adjust the parameters for more stability
odrv0.axis1.controller.config.pos_gain = 40
odrv0.axis1.controller.config.vel_gain = 0.2
odrv0.axis1.controller.config.vel_integrator_gain = 0.0005

odrv0.axis0.controller.config.pos_gain = 40
odrv0.axis0.controller.config.vel_gain = 0.2
odrv0.axis0.controller.config.vel_integrator_gain = 0.0005

for i in range(10):
	print("moving up")
	odrv0.axis1.controller.move_incremental(0.7,True)
	odrv0.axis0.controller.move_incremental(-0.45,True)
	time.sleep(2)

	print("moving down")
	odrv0.axis1.controller.move_incremental(-0.7,True)
	odrv0.axis0.controller.move_incremental(0.45,True)
	time.sleep(2)

print("torque" + str(odrv0.axis1.motor.config.torque_lim) + "bandwidth" + str(odrv0.axis1.motor.config.current_control_bandwidth))
print("errors ..")
print(dump_errors(odrv0))
print("releasing ..")
odrv0.axis1.requested_state = AXIS_STATE_IDLE
odrv0.axis0.requested_state = AXIS_STATE_IDLE #release motors
