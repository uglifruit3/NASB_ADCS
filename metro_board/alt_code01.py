# python and circuitpython libraries
# import board
# from busio import I2C
from  gc import mem_free
import board
from time import sleep
import adafruit_bno055
from sys import exit
from digitalio import DigitalInOut, Direction, Pull
from time import sleep
from math import sin, pi

# system routine libraries
import MASTER_PROCESS 
# importing protocol names
from MASTER_PROCESS import P_I2C, SYS_STATE

def main():
    MASTER_PROCESS.startup_delay()
    MASTER_PROCESS.announce_event("SYS", "INFO", f"{mem_free()} bytes free.")
    
    # CMDS_0.IMU_RESET()
    #for i in D_COILS:
    #    i.state = -1
    #    i.set_duty_cycle(1)

    sensor = adafruit_bno055.BNO055_I2C(P_I2C)
    while True:
        print(sensor.gyro)
        print(sensor.magnetic)
        print(sensor.temperature)
        print("----")
        sleep(0.2)


# =================== #
#       MAIN          #
# =================== #

main()
