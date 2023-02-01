from time import sleep

import MASTER_PROCESS
from MASTER_PROCESS import SYS_STATE

from BNO055 import D_IMU

def IMU_RESET():
    if D_IMU.reset_T == 0:
        MASTER_PROCESS.announce_event("IMU", "INFO", "Unable to perform hardware reset.")
        return

    D_IMU.reset_T.value = False
    sleep(0.05)
    D_IMU.reset_T.value = True
    MASTER_PROCESS.announce_event("IMU", "INFO", "Performed hardware reset.")
    sleep(0.20)
