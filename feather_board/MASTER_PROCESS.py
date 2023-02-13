# This is the system routine library for the master process.

from time import monotonic
import board
from busio import I2C

from CFG import *

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

# scans for I2C devices and returns a list of found device addresses
def i2c_scan(i2c):
    while i2c.try_lock() is False:
        pass

    a = i2c.scan()
    i2c.unlock()
    return a
