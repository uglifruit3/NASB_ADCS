from CFG import *
# system routine libraries
import MASTER_PROCESS 

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
D_IMU.calibrate()
testing.get_bdot_realtime()
