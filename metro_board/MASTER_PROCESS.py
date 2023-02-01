# This is the system routine library for the master process.

from time import monotonic
import board
from busio import I2C

#==========================#
# Custom classes           #
#==========================#

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

#==========================#
# Global declarations      #
#==========================#

# global system state tracker
SYS_STATE = system_state()
# I2C protocol object
P_I2C = I2C(scl=board.SCL, sda=board.SDA)

#==========================#
# Custom functions         #
#==========================#

# announces an event, sending it to the system log and/or printing it to the serial console
def announce_event(origin, level, message, cmd=SYS_STATE.command):
    # dictionary for referencing level of event importance
    EVENT_LEVELS = {
        "DEBUG":3,
        "INFO":2,
        "WARNING":1,
        "ERROR":0 
    }
    if EVENT_LEVELS[level] > SYS_STATE.log_level:
        return

    if cmd == -1:
        out_str = f"---:{origin}:{level:>7}: {message}"
    else:
        out_str = f"{cmd:03d}:{origin}:{level:>7}: {message}"

    if SYS_STATE.system_read_only is False:
        with open(LOG.txt, "a") as outfile:
            outfile.write(out_str)
    if SYS_STATE.terminal_output is True:
        print(out_str)
        
# after booting, delays the system startup if the system setting startup_delay_s is other than 0
def startup_delay():
    delay = SYS_STATE.startup_delay
    if delay == 0:
        return
    announce_event("SYS", "INFO", f"Delaying startup by {delay} seconds.", cmd=0)

    t_i = monotonic()
    t_c = t_i
    while (t_c-t_i < delay):
        t_c = monotonic()

    return
