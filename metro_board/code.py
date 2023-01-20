import board
from busio import I2C
from  gc import mem_free
import adafruit_bno055
from time import sleep

import testing
import imu
import MASTER_PROCESS 

# I2C = I2C(scl=board.D0, sda=board.D1)

def main():
    MASTER_PROCESS.startup_delay()
    MASTER_PROCESS.display_event(MASTER_PROCESS.SYS_STATE, "SYS", "INFO", f"{mem_free()} bytes free.")

# =================== #
#       MAIN          #
# =================== #

main()
