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

##PID

odrv0.axis1.controller.config.pos_gain = 60
odrv0.axis1.controller.config.vel_gain = 0.3
odrv0.axis1.controller.config.vel_integrator_gain = 0.0005

odrv0.axis0.controller.config.pos_gain = 60
odrv0.axis0.controller.config.vel_gain = 0.3
odrv0.axis0.controller.config.vel_integrator_gain = 0.0005

rotation_0 = [0.0891203703703704, 0.0972222222222222, 0.105324074074074,	0.113425925925926,	0.121527777777778,	0.129629629629630,	0.137731481481481,	0.145833333333333,	0.153935185185185,	0.162037037037037,	0.170138888888889,	0.178240740740741,	0.186342592592593,	0.194444444444444,	0.202546296296296,	0.210648148148148,	0.218750000000000,	0.226851851851852,	0.234953703703704,	0.243055555555556,	0.251157407407407,	0.259259259259259,	0.267361111111111,	0.275462962962963,	0.283564814814815,	0.291666666666667,	0.299768518518519,	0.307870370370370,	0.315972222222222,	0.324074074074074,	0.332175925925926,	0.340277777777778,	0.348379629629630,	0.356481481481481,	0.364583333333333,	0.372685185185185,	0.380787037037037,	0.388888888888889,	0.396990740740741,	0.405092592592593,	0.413194444444444,	0.421296296296296,	0.429398148148148,	0.437500000000000,	0.445601851851852]
rotation_1 = [-0.128965191536379,	-0.140678335578586,	-0.152388554326095,	-0.164095576290702,	-0.175799122983372,	-0.187498908235774,	-0.199194637487773,	-0.210886007037322,	-0.222572703248938,	-0.234254401716658,	-0.245930766377029,	-0.257601448567340,	-0.269266086023890,	-0.280924301814642,	-0.292575703200145,	-0.304219880416025,	-0.315856405369791,	-0.327484830244002,	-0.339104685997158,	-0.350715480752836,	-0.362316698066730,	-0.373907795060295,	-0.385488200408600,	-0.397057312168850,	-0.408614495434728,	-0.420159079800327,	-0.431690356615863,	-0.443207576015720,	-0.454709943697500,	-0.466196617428786,	-0.477666703256167,	-0.489119251388713,	-0.500553251725637,	-0.511967628995168,	-0.523361237468861,	-0.534732855212599,	-0.546081177832474,	-0.557404811670602,	-0.568702266402812,	-0.579971946987126,	-0.591212144909158,	-0.602421028668184,	-0.613596633445895,	-0.624736849899014,	-0.635839412017505]
rotation_0 = [round(num , 4) for num in rotation_0] 
rotation_1 = [round(num , 4) for num in rotation_1] 
print(rotation_0[0])
print(rotation_1[0])

for x in range(0,len(rotation_0),3):
    print("moving up")
    odrv0.axis0.controller.move_incremental(- rotation_0[x],True)
    odrv0.axis1.controller.move_incremental(- rotation_1[x],True)
    
    time.sleep(3)

    print("moving down")
    odrv0.axis1.controller.move_incremental(rotation_1[x],True)
    odrv0.axis0.controller.move_incremental(rotation_0[x],True)
    time.sleep(3)
    print(x)


print("torque" + str(odrv0.axis1.motor.config.torque_lim) + "bandwidth" + str(odrv0.axis1.motor.config.current_control_bandwidth))
print("errors ..")
print(dump_errors(odrv0))
print("releasing ..")
odrv0.axis1.requested_state = AXIS_STATE_IDLE
odrv0.axis0.requested_state = AXIS_STATE_IDLE
