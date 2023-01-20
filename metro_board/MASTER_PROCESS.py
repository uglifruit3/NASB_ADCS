from time import monotonic
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
                "system_mode":0,
                "output_mode":0,
                "system_read_only":0,
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

        self.system_mode = switch["system_mode"]
        self.output_mode = switch["output_mode"]
        self.system_read_only = switch["system_read_only"]
        self.startup_delay = switch["startup_delay"]
        self.log_level = switch["log_level"]

# global system state tracker
SYS_STATE = system_state()

# global dictionary for referencing level of event importance
EVENT_LEVELS = {
        "DEBUG":3,
        "INFO":2,
        "WARNING":1,
        "ERROR":0 
        }
# displays an event, sending it to the system log and/or printing it to the serial console
def display_event(sys_state, origin, level, message, command=0):
    if EVENT_LEVELS[level] > sys_state.log_level:
        return

    out_str = f"{command:03d}:{origin}:{level:>7}: {message}"

    if (sys_state.output_mode == "log" or sys_state.output_mode == "both") and sys_state.system_read_only == "false":
        with open(LOG.txt, "a") as outfile:
            outfile.write(out_str)
    if sys_state.output_mode != "log":
        print(out_str)
        
# after booting, delays the system startup if the system setting startup_delay_s is other than 0
def startup_delay():
    delay = SYS_STATE.startup_delay
    if delay == 0:
        return
    display_event(SYS_STATE, "SYS", "INFO", f"Delaying startup by {delay} seconds.")

    t_i = monotonic()
    t_c = t_i
    while (t_c-t_i < delay):
        t_c = monotonic()

    return
