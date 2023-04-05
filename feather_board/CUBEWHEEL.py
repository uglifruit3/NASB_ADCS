# This is the custom driver for the CubeSpace CubeWheel over I2C

# python and circuitpython libraries
from time import sleep
from digitalio import DigitalInOut, Direction, Pull

from CFG import *
# system routine libraries
import MASTER_PROCESS

#==========================#
# Custom classes           #
#==========================#

# I2C addresses
write_addr = 0xD0
read_addr  = 0xD1
# To be used in sending command IDs over I2C
commands = {
        # telecommands
        "reset":              b'\x01', 
        "set_wheel_refspeed": b'\x02',
        "set_wheel_duty":     b'\x03',
        "set_motor_power":    b'\x07',
        "set_enc_power":      b'\x08',
        "set_hall_power":     b'\x09',
        "set_ctrl_mode":      b'\x0A',
        "set_backup_mode":    b'\x0C',
        "clr_errors":         b'\x15',
        # telemetry requests
        "get_wheel_status":     b'\x82',
        "get_wheel_speed":      b'\x85',
        "get_wheel_refspeed":   b'\x85',
        "get_wheel_current":    b'\x87',
        "get_wheel_data":       b'\x89',
        "get_status_errors":    b'\x91'
        }
ctrl_modes = {
        "idle":       0,
        "no_ctrl":    1,
        "dc_input":   2,
        "speed_ctrl": 4
        }

class Reaction_Wheel():
    def __init__(self, i2c_in):
        # initialize communication protocol and check if device present on lines
        self.i2c = i2c_in
        # TODO use isinstance(i2c, busio.i2c) to check validity
        addrs = MASTER_PROCESS.i2c_scan(self.i2c)
        if write_addr not in addrs or read_addr not in addrs:
            raise ValueError
        # initialize error field
        self.errors = {
                "telemetry":   False,
                "telecommand": False,
                "encoder":     False,
                "i2c":         False,
                "config":      False,
                "speed":       False,
                "wheel":       False
                }
        # self.errors = self.get_errors()
        # ^^uncomment when ready
        self.refspeed = 0
        self.ctrl_mode = ctrl_modes["idle"]

    def get_errors(self):
        pass
    def reset(self):
        # the argument to this command must be set to 85
        writeto(write_addr, commands["reset"]+(85).to_bytes(1,'little'))
        # await wheel to come back online
        while write_addr not in MASTER_PROCESS.i2c_scan(self.i2c):
            pass
        return 
