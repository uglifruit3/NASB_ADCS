# This is the system routine library for all 2XX series commands
from time import sleep

from CFG import *
import MASTER_PROCESS

import CMDS_0

#==========================#
# Command functions        #
#==========================#

def _200_QUERY_MAGNETIC_FIELD_DATA():
    try:
        tmp = list(D_IMU.magnetic)
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on magnetometer register(s).", cmd=202)
        CMDS_0._001_IMU_RESET()
        tmp = list(D_IMU.magnetic)

    while tmp[0] == None:
        tmp = list(D_IMU.magnetic)

    for i in range(0,3):
        tmp[i] /= 1e6 # conversion from microT to T

    return tmp

def _201_QUERY_RATE_DATA():
    try:
        tmp = list(D_IMU.gyro)
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on gyroscope register(s).", cmd=201)
        CMDS_0.IMU_RESET()
        tmp = list(D_IMU.gyro)

    while tmp[0] == None:
        tmp = list(D_IMU.gyro)
    return tmp

def _202_QUERY_SUN_SENSOR_DATA():
    l = []
    for sensor in D_CSS:
        l.append(sensor.light_level())

    return l

def _203_QUERY_SUN_VECTOR():
    lvls = QUERY_SUN_SENSOR_DATA()
    
    dx = lvls[0]-lvls[1]
    dy = lvls[2]-lvls[3]
    dz = lvls[4]-lvls[5]

    return [dx, dy, dz]

def _204_QUERY_ATTITUDE():
    pass

def _205_QUERY_SYSTEM_TEMPERATURE():
    try:
        tmp = D_IMU.temperature
    except OSError:
        MASTER_PROCESS.announce_event("IMU", "ERROR", "Bad read on temperature register.", cmd=205)
        CMDS_0._001_IMU_RESET()
        tmp = D_IMU.temperature
    else:
        return tmp

def _206_CALIBRATE_GYROSCOPE():
    pass

def _207_CALIBRATE_MAGNETOMETER():
    pass

def _208_CALIBRATE_SENSOR_SYSTEM():
    pass

def _209_DOWNLINK_SENSOR_DATA():
    pass
