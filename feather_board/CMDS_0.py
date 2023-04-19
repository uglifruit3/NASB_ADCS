from digitalio import DigitalInOut, Direction
from time import sleep
from  gc import mem_free

from CONFIG import *
import MASTER_PROCESS

from BNO055 import Inertial_Measurement_Unit

def _000_SYSTEM_RESET():
    pass

def _001_IMU_RESET():
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

def _002_SET_IMU_POWER():
    pass

def _003_QUERY_SOH():
    pass

def _004_SET_SH_MODE():
    pass

def _005_QUERY_MODE():
    pass

def _006_QUERY_FREE_MEMORY():
    mem = mem_free()
    MASTER_PROCESS.announce_event("SYS", "INFO", f"{mem} bytes free.", cmd=006)
    return mem

def _007_QUERY_FREE_FILESYSTEM_STORAGE():
    pass

def _008_QUERY_TLE():
    pass

def _009_SET_TLE():
    pass

def _010_QUERY_SYSTEM_TIME():
    pass

def _011_SET_SYSTEM_TIME():
    pass

def _012_QUERY_UPTIME():
    pass
