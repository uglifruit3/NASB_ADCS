# python and circuitpython libraries
from math import sin
# import adafruit_bno055
from time import monotonic, sleep

from CFG import *
# system routine libraries
import MASTER_PROCESS 

# command routine libraries
import CMDS_0
import CMDS_2
import CMDS_4

def main():
    MASTER_PROCESS.startup_delay()
    CMDS_0.QUERY_FREE_MEMORY()

    cnt = 0
    # while True:

    #     t_i = monotonic()
    #     for i in D_COILS:
    #         i.state = -1
    #         i.set_duty_cycle(1)
    #     print("Coils on")

    #     while monotonic()-t_i < 0.95:
    #         pass

    #     for i in D_COILS:
    #         i.set_duty_cycle(0)
    #     print("Coils off")
    #     cnt+=1
    #     print(f"[{cnt}] B_body: {CMDS_2.QUERY_MAGNETIC_FIELD_DATA()}")
    #     print(f"[{cnt}]Ordered m = {CMDS_4.bdot_controller()}")

    #     while monotonic()-t_i < 1.0:
    #         pass
      
    #=========================#
    # t_start = monotonic()
    # while True:
    #     data = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    #     print("{c1:06.2f}> {e1:06.2f} {e2:06.2f} {e3:06.2f}".format(c1=monotonic()-t_start, e1=data[0], e2=data[1], e3=data[2]), end="\r")

    #=========================#
    for i in D_COILS:
        i.state = 1
    while True:
        pwr = (sin(cnt) + 1) / 2
        for i in D_COILS:
            if pwr == 0:
                i.state = i.state*-1
            i.set_duty_cycle(pwr)
        print(f"\rDuty cycle: {pwr:.4f}", end="")
        cnt += 0.001
        sleep(0.001)

# =================== #
#       MAIN          #
# =================== #

main()
