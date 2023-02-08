# python and circuitpython libraries
from  gc import mem_free
# import adafruit_bno055
from time import monotonic

from CFG import *
# system routine libraries
import MASTER_PROCESS 

# command routine libraries
import CMDS_0
import CMDS_2

def main():
    global D_IMU 
    global P_I2C

    MASTER_PROCESS.startup_delay()
    MASTER_PROCESS.announce_event("SYS", "INFO", f"{mem_free()} bytes free.")

    cnt = 0
    while True:

        t_i = monotonic()
        for i in D_COILS:
            i.state = -1
            i.set_duty_cycle(1)
        print("Coils on")

        while monotonic()-t_i < 0.95:
            pass

        for i in D_COILS:
            i.set_duty_cycle(0)
        print("Coils off")
        cnt+=1
        print(f"[{cnt}] {CMDS_2.QUERY_MAGNETIC_FIELD_DATA()}")
        print(f"[{cnt}] {CMDS_2.QUERY_RATE_DATA()}")
        print(f"[{cnt}] {CMDS_2.QUERY_SYSTEM_TEMPERATURE()}")

        while monotonic()-t_i < 1.0:
            pass
        


# =================== #
#       MAIN          #
# =================== #

main()
