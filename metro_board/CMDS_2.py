# This is the system routine library for all 2XX series commands

import MASTER_PROCESS
from MASTER_PROCESS import SYS_STATE

from BNO055 import D_IMU

# WHY WONT THESE COMMANDS RETURN GOOD VALUES???
def QUERY_MAGNETIC_FIELD_DATA():
    return D_IMU.fetch_mag_data()
    
def QUERY_RATE_DATA():
    try:
        tmp = list(D_IMU.gyro)
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on gyroscope register(s).", cmd=202)
    else:
        return tmp

def QUERY_SYSTEM_TEMPERATURE():
    try:
        tmp = D_IMU.temperature
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on temperature register.", cmd=205)
    else:
        return tmp
