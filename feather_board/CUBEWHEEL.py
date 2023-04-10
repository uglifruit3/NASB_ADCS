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

# I2C addresses and device info
write_addr = 0xD0
read_addr  = write_addr+1
byte_order = 'little'
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
        if isinstance(i2c_in, busio.I2C) == False:
            raise ValueError("I2C object not correctly initialized")
        else:
            self.i2c = i2c_in
        # check for wheel addresses on i2c lines
        addrs = MASTER_PROCESS.i2c_scan(self.i2c)
        if write_addr not in addrs or read_addr not in addrs:
            raise ValueError(f"CubeWheel not found at addresses {hex(write_addr)} (write) and {hex(read_addr)} (read)")

        # initialize error field
        self.errors = [
                [0, "telemetry",   False],
                [1, "telecommand", False],
                [2, "encoder",     False],
                [4, "i2c",         False],
                [6, "config",      False],
                [7, "speed",       False],
                [8, "wheel",       False],
                ]
        # self.errors = self.get_errors()
        # ^^uncomment when ready
        self.refspeed = 0
        self.ctrl_mode = ctrl_modes["idle"]

    #==============#
    # telecommands # 
    #==============#
    def reset(self):
        # the argument to this command must be set to 85
        self.i2c.writeto(write_addr, 
                commands["reset"]+(85).to_bytes(1,byte_order,signed=False))
        # await wheel to come back online
        while write_addr not in MASTER_PROCESS.i2c_scan(self.i2c):
            pass
        return 

    def set_wheel_refspd(self, speed):
        self.i2c.writeto(write_addr, 
                commands["set_wheel_refspd"]+int(speed*2).to_bytes(2,byte_order,signed=True))
        return

    def set_wheel_duty(self, dc):
        if dc < 0 or dc > 1:
            raise ValueError("Duty cycle must be a number between 0 and 1")
        dc *= 100
        self.i2c.writeto(write_addr, 
                commands["set_wheel_duty"]+int(dc).to_bytes(2,byte_order,signed=True))
        return

    def set_motor_power(self, bool_pwr):
        if bool_pwr = True:
            pwr = 255
        else:
            pwr = 0 
        self.i2c.writeto(write_addr,
                commands["set_motor_power"]+(pwr).to_bytes(1,byte_order,signed=False))
        return
    
    def set_enc_power(self, bool_pwr):
        if bool_pwr = True:
            pwr = 255
        else:
            pwr = 0 
        self.i2c.writeto(write_addr,
                commands["set_enc_power"]+(pwr).to_bytes(1,byte_order,signed=False))
        return

    def set_hall_power(self, bool_pwr):
        if bool_pwr = True:
            pwr = 255
        else:
            pwr = 0 
        self.i2c.writeto(write_addr,
                commands["set_hall_power"]+(pwr).to_bytes(1,byte_order,signed=False))
        return

    def set_ctrl_mode(self, mode):
        if mode not in range(0,5):
            raise ValueError("Mode must be int 0-4")
        self.i2c.writeto(write_addr,
                commands["set_ctrl_mode"]+(mode).to_bytes(1,byte_order,signed=False))
        return

    def set_backup_mode(self, bool_backup_on):
        if bool_backup_on = True:
            backup = 255
        else:
            backup = 0 
        self.i2c.writeto(write_addr,
                commands["set_backup_mode"]+(backup).to_bytes(1,byte_order,signed=False))
        return

    def clr_errors(self):
        self.i2c.writeto(write_addr, 
                commands["clr_errors"]+(85).to_bytes(1,byte_order,signed=False))
        return

    #==============#
    # telemetry    # 
    #==============#
    def get_wheel_status(self):
        pass
    def get_wheel_speed(self):
        pass
    def get_wheel_refspeed(self):
        pass
    def get_wheel_current(self):
        pass
    def get_wheel_data(self):
        pass
    def get_status_errors(self):
        # read output into in_buffer
        in_buffer = bytes(1)
        self.i2c.writeto_then_readfrom(write_addr, 
                commands["get_status_errors"],
                in_buffer)
        # check against bitmask to obtain error flags
        errs = int.from_bytes(in_buffer, byte_order)
        for i in range(0,6):
            if (in_buffer >> self.errors[i][0]) & 1 == 1:
                self.errors[i][2] = True
            else:
                self.errors[i][2] = False
        return
