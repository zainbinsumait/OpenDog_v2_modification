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

# To read a value, simply read the property
print("Bus voltage is " + str(odrv0.vbus_voltage) + "V")


         
print("motor 0 : starting closed loop control...")
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

print("motor 1 : starting closed loop control...")
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

print("changing to passthrough...")
odrv0.axis1.controller.config.input_mode = INPUT_MODE_POS_FILTER
#odrv0.axis0.controller.config.input_mode = INPUT_MODE_PASSTHROUGH
odrv0.axis0.controller.config.input_mode = INPUT_MODE_POS_FILTER
odrv0.axis0.controller.config.input_filter_bandwidth = 20
odrv0.axis1.controller.config.input_filter_bandwidth = 20

##PID

odrv0.axis1.controller.config.pos_gain = 60
odrv0.axis1.controller.config.vel_gain = 0.3
odrv0.axis1.controller.config.vel_integrator_gain = 0.0005

odrv0.axis0.controller.config.pos_gain = 60
odrv0.axis0.controller.config.vel_gain = 0.3
odrv0.axis0.controller.config.vel_integrator_gain = 0.0005

rotation_0 = [-0.0810185185185185,	0,	0.0810185185185185]
rotation_1 = [-0.307974646373183,	-0.254666112539341,	-0.186446868595405]

rotation_0 = [round(num , 4) for num in rotation_0] 
rotation_1 = [round(num , 4) for num in rotation_1] 

standing_u = - 0.170138888888889 #the default rotation to reach the default position from the ground
standing_L = 0.245930766377029 #the default rotation to reach the default position from the ground
print("moving up")
odrv0.axis0.controller.move_incremental(standing_u,True)    
odrv0.axis1.controller.move_incremental((standing_L),True)

time.sleep(2)
"""print("moving down")
odrv0.axis1.controller.move_incremental(-0.245930766377029,True)
odrv0.axis0.controller.move_incremental(0.170138888888889,True)
time.sleep(3)
print(x)"""

shift_u = standing_u
shift_l = standing_L

front_u = 0
front_l = -0.2431
back_u = 0.3241
back_l = -0.3464
for i in range(10):
    print("moving up")
    odrv0.axis1.controller.move_incremental(- (shift_l + front_l - 0.2),True)
    time.sleep(0.3)
    odrv0.axis0.controller.move_incremental(-(shift_u + front_u),True)
    odrv0.axis1.controller.move_incremental(-0.3 ,True)
    
    time.sleep(0.3)
  
    print("moving down")
    odrv0.axis0.controller.move_incremental((shift_u + front_u),True)
    odrv0.axis1.controller.move_incremental((shift_l + front_l) +0.1,True)
    
    time.sleep(0.3)

odrv0.axis0.controller.move_incremental(-standing_u,True)    
odrv0.axis1.controller.move_incremental(-(standing_L),True)
time.sleep(3)

print("torque" + str(odrv0.axis1.motor.config.torque_lim) + "bandwidth" + str(odrv0.axis1.motor.config.current_control_bandwidth))
print("errors ..")
print(dump_errors(odrv0))
print("releasing ..")
odrv0.axis1.requested_state = AXIS_STATE_IDLE
odrv0.axis0.requested_state = AXIS_STATE_IDLE
