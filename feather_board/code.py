from CFG import *
# system routine libraries
import MASTER_PROCESS 

import SUNSENSOR

# command routine libraries
import CMDS_0
import CMDS_2
import CMDS_4

# testing routines
import testing

def main():
    MASTER_PROCESS.startup_delay()
    CMDS_0.QUERY_FREE_MEMORY()

# =================== #
#       MAIN          #
# =================== #

main()
# cnt = 0
# sum_t = 0
# hi = 0
# while True:
#     cnt += 1
#     t = testing.mag_timer()
#     if t > hi:
#         hi = t
#     sum_t += t
#     avg = sum_t/cnt
#     print(f"\rTime between reads: {t:10.8f} {avg:10.8f} {hi:10.8f}", end="")
testing.coil_runup(10, 1, 1) 
