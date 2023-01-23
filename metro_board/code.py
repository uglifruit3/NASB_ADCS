import board
from busio import I2C
from  gc import mem_free
import adafruit_bno055
from time import sleep
from math import sin

import testing
import imu
import MASTER_PROCESS 
import HBRIDGE

# I2C = I2C(scl=board.D0, sda=board.D1)

def main():
    MASTER_PROCESS.startup_delay()
    MASTER_PROCESS.display_event(MASTER_PROCESS.SYS_STATE, "SYS", "INFO", f"{mem_free()} bytes free.")
    
    c1 = HBRIDGE.H_Bridge_Coil(board.D2, board.D3)
    c2 = HBRIDGE.H_Bridge_Coil(board.D4, board.D5)
    c3 = HBRIDGE.H_Bridge_Coil(board.D6, board.D7)

    t = 0.00
    while True:
        power = sin(t) 
        if power < 0:
            power = abs(power)
            state = -1
        else:
            state = 1

        c1.state = state
        c1.set_duty_cycle(power)
        c2.state = state
        c2.set_duty_cycle(power)
        c3.state = state
        c3.set_duty_cycle(power)

        t += 0.002
    
# =================== #
#       MAIN          #
# =================== #

main()
