# this is the interface for running commands when received by the PIB
from CFG import *
# system routine libraries
import MASTER_PROCESS 

# command routine libraries
import CMDS_0
import CMDS_1
import CMDS_2
import CMDS_3
import CMDS_4

# this class should be extended to include other data as needed
class User_Command():
    def __init__(self, cmd_func, num_arguments):
        self.execute = cmd_func
        self.num_args = num_arguments

# index of all user available commands
CMDS = {
        000: User_Command(CMDS_0._000_SYSTEM_RESET, 0),
        001: User_Command(CMDS_0._001_IMU_RESET, 0),
        002: User_Command(CMDS_0._002_SET_IMU_POWER, 1),
        003: User_Command(CMDS_0._003_QUERY_SOH, 1),
        004: User_Command(CMDS_0._004_SET_SH_MODE, 1),
        005: User_Command(CMDS_0._005_QUERY_MODE, 0),
        006: User_Command(CMDS_0._006_QUERY_FREE_MEMORY, 0),
        007: User_Command(CMDS_0._007_QUERY_FREE_FILESYSTEM_STORAGE, 0),
        008: User_Command(CMDS_0._008_QUERY_TLE, 0),
        009: User_Command(CMDS_0._009_SET_TLE, 1),
        010: User_Command(CMDS_0._010_QUERY_SYSTEM_TIME, 0),
        011: User_Command(CMDS_0._011_SET_SYSTEM_TIME, 1),
        012: User_Command(CMDS_0._012_QUERY_UPTIME, 0),
        100: User_Command(CMDS_1._100_QUERY_SYSTEM_LOG, 1),
        101: User_Command(CMDS_1._101_CLEAR_SYSTEM_LOG, 0),
        102: User_Command(CMDS_1._102_SET_MAX_LOG_ENTRIES, 1),
        200: User_Command(CMDS_2._200_QUERY_MAGNETIC_FIELD_DATA, 0),
        201: User_Command(CMDS_2._201_QUERY_RATE_DATA, 0),
        202: User_Command(CMDS_2._202_QUERY_SUN_SENSOR_DATA, 0),
        203: User_Command(CMDS_2._203_QUERY_SUN_VECTOR, 0),
        204: User_Command(CMDS_2._204_QUERY_ATTITUDE, 1),
        205: User_Command(CMDS_2._205_QUERY_SYSTEM_TEMPERATURE, 0),
        206: User_Command(CMDS_2._206_CALIBRATE_GYROSCOPE, 0),
        207: User_Command(CMDS_2._207_CALIBRATE_MAGNETOMETER, 0),
        208: User_Command(CMDS_2._208_CALIBRATE_SENSOR_SYSTEM, 0),
        209: User_Command(CMDS_2._209_DOWNLINK_SENSOR_DATA, 1),
        300: User_Command(CMDS_3._300_MOMENTUM_WHEEL_SPINUP, 0),
        301: User_Command(CMDS_3._301_MOMENTUM_WHEEL_SPINDOWN, 0),
        302: User_Command(CMDS_3._302_QUERY_MOMENTUM_WHEEL_SPEED, 0),
        304: User_Command(CMDS_3._304_MAGNETIC_DEVICE_RESET, 0),
        305: User_Command(CMDS_3._305_QUERY_MAGNETIC_DEVICE_POWER, 0),
        400: User_Command(CMDS_4._400_DETUMBLE, 3),
        401: User_Command(CMDS_4._401_ORIENT_TO_NADIR, 4),
        402: User_Command(CMDS_4._402_TERMINATE_ATTITUDE_COMMAND 0)
        }

# interface to calling a command by index
# arguments to a command should be passed as an array in args (empty by default)
def run_cmd(cmd_ind, args=[]):
    if len(args) != CMDS[cmd_ind].num_args:
        MASTER_PROCESS.announce_event("SYS", "ERROR", f"Attempted to run command {cmd_ind} with incorrect number of args.", cmd=-1)
        return False
    # * operator unpacks array into list of arguments to be passed
    CMDS[cmd_ind].execute(*args)
