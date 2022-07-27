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


#configuration
"""odrv0.config.brake_resistance = 0.5
odrv0.config.enable_dc_bus_overvoltage_ramp = True
odrv0.config.dc_bus_overvoltage_ramp_start = 12 + 2
odrv0.config.dc_bus_undervoltage_trip_level = 8.0
odrv0.config.dc_bus_overvoltage_trip_level = 24.0


#motor
odrv0.axis0.motor.config.current_lim = 20
odrv0.axis0.motor.config.pole_pairs = 14
odrv0.config.enable_brake_resistor = True
odrv0.config.dc_max_negative_current = -3.0
odrv0.axis0.motor.config.calibration_current = 12
odrv0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT



odrv0.axis0.motor.config.torque_constant = 8.27 / 120
odrv0.axis0.motor.config.torque_lim = 1
odrv0.axis0.motor.config.current_control_bandwidth = 2000
odrv0.save_configuration()"""

##calibration motors 
odrv0.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION


##sensorless mode
odrv0.axis0.controller.config.vel_gain = 0.01
odrv0.axis0.controller.config.vel_integrator_gain = 0.05
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
odrv0.axis0.controller.config.vel_limit = 400 / (2*3.14 * 21)
odrv0.axis0.sensorless_estimator.config.pm_flux_linkage = 5.51328895422 / (21 * 120)
odrv0.axis0.config.enable_sensorless_mode = True
odrv0.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION


print("torque" + str(odrv0.axis1.motor.config.torque_lim) + "bandwidth" + str(odrv0.axis1.motor.config.current_control_bandwidth))
print("errors ..")
print(dump_errors(odrv0))





