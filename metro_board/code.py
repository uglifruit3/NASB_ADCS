import board
import busio
import time
import gc
import adafruit_bno055

import test

I2C = busio.I2C(scl=board.SCL, sda=board.SDA)

PRINT_MODE = 1
#  0 -> newline output (for serial interpretation)
#  1 -> fancy output with carriage returns (for readability)

# TODO need to verify calibrated sensor accuracies and obtain un-calibrated sensor accuracies

def main():
    print("SYS: DEBUG: " + str(gc.mem_free()) + " bytes free post-load")

    disp_I2C_scan(I2C)

    IMU = test.Inertial_Measurement_Unit(I2C)
    IMU.check_init(I2C)

    IMU.calibrate()

    while True:
        try:
            data = IMU.euler
        except OSError:
            print("\nIMU: WARNS: Bad read on attitude register(s).")
            print("IMU: WARNS: Hardware reset initiated by main.")
            IMU.hware_reset()
        else:
            if PRINT_MODE == 0:
                print("> {e1:6.2f} {e2:6.2f} {e3:6.2f}".format(e1=data[0], e2=data[1], e3=data[2]))
            elif PRINT_MODE == 1:
                print("\r> {e1:6.2f} {e2:6.2f} {e3:6.2f}".format(e1=data[0], e2=data[1], e3=data[2]), end="")

def disp_I2C_scan(I2C):
    print("I2C: DEBUG: Scanning I2C addresses:")
    addrs = test.addr_scan(I2C)
    if addrs == []:
            print(" -> None found.")
    else:
            print(" -> Addresses found:")
            print("    ", end="")
            print([hex(dev_addr) for dev_addr in addrs])


# =================== #
#       MAIN          #
# =================== #
main()
