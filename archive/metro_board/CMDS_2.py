# This is the system routine library for all 2XX series commands

from CFG import *

import MASTER_PROCESS

import CMDS_0

def QUERY_MAGNETIC_FIELD_DATA():
    try:
        tmp = list(D_IMU.magnetic)
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on gyroscope register(s).", cmd=202)
        CMDS_0.IMU_RESET()
        return [float('nan'), float('nan'), float('nan')]
    else:
        return tmp
    
def QUERY_RATE_DATA():
    try:
        tmp = list(D_IMU.gyro)
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on gyroscope register(s).", cmd=202)
        CMDS_0.IMU_RESET()
        return [float('nan'), float('nan'), float('nan')]
    else:
        return tmp

def QUERY_SYSTEM_TEMPERATURE():
    try:
        tmp = D_IMU.temperature
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on temperature register.", cmd=205)
        CMDS_0.IMU_RESET()
        return float('nan')
    else:
        return tmp
