from digitalio import DigitalInOut, Direction
from time import sleep
from  gc import mem_free

from CFG import *
import MASTER_PROCESS

from BNO055 import Inertial_Measurement_Unit

def IMU_RESET():
    # needed to re-initialize the IMU after reset
    global D_IMU
    # in event that reset not configured for in hardware
    if D_IMU.reset_T == 0:
        MASTER_PROCESS.announce_event("IMU", "INFO", "Unable to perform hardware reset.", cmd=002)
        return

    # rst pin is active low. Set hi, then lo to reset. 
    # reset pin MUST be de-initialized. With an initialized reset pin, buggy behavior occurs with IMU
    with DigitalInOut(D_IMU.reset_T) as tmp:
        tmp.direction = Direction.OUTPUT

        tmp.value = True
        sleep(0.20)
        tmp.value = False
        sleep(0.20)

    # scan for IMU to come online
    while 0x28 not in MASTER_PROCESS.i2c_scan(P_I2C):
        pass
    # re-initialize imu
    D_IMU = Inertial_Measurement_Unit(P_I2C, rst=board.D4)
    MASTER_PROCESS.announce_event("IMU", "INFO", "Performed hardware reset.", cmd=002)

def QUERY_FREE_MEMORY():
    mem = mem_free()
    MASTER_PROCESS.announce_event("SYS", "INFO", f"{mem} bytes free.", cmd=009)
    return mem
