# python and circuitpython libraries
# import board
# from busio import I2C
from  gc import mem_free
# import adafruit_bno055
from time import sleep
from math import sin, pi

# system routine libraries
import MASTER_PROCESS 
# importing protocol names
from MASTER_PROCESS import P_I2C, SYS_STATE

# custom device drivers
import HBRIDGE
import BNO055
# importing device names
from HBRIDGE import D_COILS

# command routine libraries
import CMDS_0
import CMDS_2

# P_I2C = I2C(scl=board.SCL, sda=board.SDA)

# D_COILS = HBRIDGE.init_hbridge_coils(board.D2, board.D3, board.D4, board.D5, board.D6, board.D7)
# D_IMU = BNO055.Inertial_Measurement_Unit(P_I2C, rst=board.D8)

# TODO need to clean out old files from metroboard
def main():
    MASTER_PROCESS.startup_delay()
    MASTER_PROCESS.announce_event("SYS", "INFO", f"{mem_free()} bytes free.")
    
    for i in D_COILS:
        i.state = -1
        i.set_duty_cycle(1)


    #print(CMDS_2.QUERY_MAGNETIC_FIELD_DATA())
    print(BNO055.D_IMU.fetch_mag_data())
    print(CMDS_2.QUERY_RATE_DATA())
    print(CMDS_2.QUERY_SYSTEM_TEMPERATURE())
    print("----")

    CMDS_0.IMU_RESET()

    while True:
        print(CMDS_2.QUERY_MAGNETIC_FIELD_DATA())
        print(CMDS_2.QUERY_RATE_DATA())
        print(CMDS_2.QUERY_SYSTEM_TEMPERATURE())
        print("----")
        sleep(0.2)


# =================== #
#       MAIN          #
# =================== #

main()
