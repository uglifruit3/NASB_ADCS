import board
import busio
import time
import gc
import adafruit_bno055
from math import atan2, asin, pow

import test

I2C = busio.I2C(scl=board.SCL, sda=board.SDA)

PRINT_MODE = 1
#  0 -> newline output (for serial interpretation)
#  1 -> fancy output with carriage returns (for readability)

def main():
    print("SYS: DEBUG: " + str(gc.mem_free()) + " bytes free post-load")

    disp_I2C_scan(I2C)

    IMU = test.Inertial_Measurement_Unit(I2C)
    IMU.check_init(I2C)

    #IMU.calibrate()

    if PRINT_MODE == 1:
        print("")
        ret_char = "\r"
        end_char = ""
    elif PRINT_MODE == 0:
        ret_char = ""
        end_char = "\n"
    while True:
        try:
            data = IMU.quaternion
        except OSError:
            print("\nIMU: WARNS: Bad read on attitude register(s).")
            print("IMU: WARNS: Hardware reset initiated by main.")
            IMU.hware_reset()
        else:

            if len(data) == 3:
                print("{c1:s}>{e1:06.2f} {e2:06.2f} {e3:06.2f}".format(c1=ret_char, e1=data[0], e2=data[1], e3=data[2]), end=end_char)
            elif len(data) == 4:
                print("{c1:s}>{e1:06.3f} {e2:06.3f} {e3:06.3f} {e3:06.3f}".format(c1=ret_char, e1=data[0], e2=data[1], e3=data[2], e4=data[3]), end=end_char)

def disp_I2C_scan(I2C):
    print("I2C: DEBUG: Scanning I2C addresses:")
    addrs = test.addr_scan(I2C)
    if addrs == []:
            print(" -> None found.")
    else:
            print(" -> Addresses found:")
            print("    ", end="")
            print([hex(dev_addr) for dev_addr in addrs])

def quat_to_euler(q0, q1, q2, q3):
    e = [0, 0, 0]

    e[0] = atan2(2*(q0*q1 + q2*q3), 1 - 2*(pow(q1,2)+pow(q2,2)))
    e[1] = asin(2*(q0*q2 - q3*q1))
    e[2] = atan2(2*(q0*q3 + q1*q2), 1 - 2*(pow(q2,2)+pow(q3,2)))

    return e




# =================== #
#       MAIN          #
# =================== #
main()
