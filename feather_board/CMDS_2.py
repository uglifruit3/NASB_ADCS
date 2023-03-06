# This is the system routine library for all 2XX series commands
from time import sleep

from CFG import *
import MASTER_PROCESS

import CMDS_0

#==========================#
# Command functions        #
#==========================#

def QUERY_RATE_DATA():
    try:
        tmp = list(D_IMU.gyro)
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on gyroscope register(s).", cmd=201)
        CMDS_0.IMU_RESET()
        tmp = QUERY_RATE_DATA()
    else:
        tmp = QUERY_RATE_DATA()

    while tmp[0] == None:
        tmp = QUERY_RATE_DATA()
    return tmp

def QUERY_MAGNETIC_FIELD_DATA():
    try:
        tmp = list(D_IMU.magnetic)
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on magnetometer register(s).", cmd=202)
        CMDS_0.IMU_RESET()
        tmp = list(D_IMU.magnetic)

    while tmp[0] == None:
        tmp = list(D_IMU.magnetic)

    for i in range(0,3):
        tmp[i] /= 1e6 # conversion from microT to T

    return tmp
    
def QUERY_SYSTEM_TEMPERATURE():
    try:
        tmp = D_IMU.temperature
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on temperature register.", cmd=205)
        CMDS_0.IMU_RESET()
        tmp = D_IMU.temperature
    else:
        return tmp
