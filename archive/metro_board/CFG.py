# TODO in process of migrating globals; need to ensure correctness and consistency
from busio import I2C
import board

class system_state():
    # tracks system settings
    # initializes from values specified in STARTUP.txt 
    def __init__(self):
        # accepts variable as a string
        def set_state_variable(var, sw, str_val):
            try:
                sw[var] = int(str_val)
            except ValueError:
                sw[var] = str_val

        switch = {
                "terminal_output":0,
                "system_read_only":0,
                "max_log_entries":0,
                "startup_delay":0,
                "log_level":0
                }

        with open("STARTUP.txt", "r") as infile:
            line = infile.readline()
            while line:
                line_list = line.split(" ")
                line_list[1] = line_list[1].strip("\n")
                line_list[0] = line_list[0].strip(" ")
                set_state_variable(line_list[0], switch, line_list[1])
                line = infile.readline()

        if switch["terminal_output"] == "true":
            self.terminal_output = True
        else:
            self.terminal_output = False
        if switch["system_read_only"] == "true":
            self.system_read_only = True
        else:
            self.system_read_only = False

        self.max_log_entries = switch["max_log_entries"]
        self.startup_delay = switch["startup_delay"]
        self.log_level = switch["log_level"]

        self.active_records = 0
        # tracks the command index currently in execution
        self.command = 0

# imu calibration object
F_IMU_CALIBRATION_PROFILE = "/00_cal_profile.txt" 

# I2C protocol object
P_I2C = I2C(scl=board.SCL, sda=board.SDA)
# global system state tracker
SYS_STATE = system_state()

from BNO055 import Inertial_Measurement_Unit
from HBRIDGE import init_hbridge_coils
# array of 3 h-bridge powered magnetic coils
D_COILS = init_hbridge_coils(board.D2, board.D3, board.D4, board.D5, board.D6, board.D7)
# inertial measurement unit
D_IMU = Inertial_Measurement_Unit(P_I2C, rst=board.D8)
