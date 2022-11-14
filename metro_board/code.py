import board
from busio import I2C
from  gc import mem_free
import adafruit_bno055
from time import sleep

import testing
import imu

I2C = I2C(scl=board.D0, sda=board.D1)

PRINT_MODE = 1
#  0 -> newline output (for serial interpretation)
#  1 -> fancy output with carriage returns (for readability)

def main():
    print("SYS: DEBUG: " + str(mem_free()) + " bytes free post-load.")
    write_pin = testing.init_dig_input(board.D7)
    testing.chk_fs_waccess(write_pin)

    testing.disp_I2C_scan(I2C)

    IMU = imu.Inertial_Measurement_Unit(I2C)
    IMU.check_init(I2C)

    IMU.calibrate()

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


# =================== #
#       MAIN          #
# =================== #
# delay in sec
boot_delay = 10
print("")
while boot_delay >= 0:
    print("\rSYS: ANCMT: Start delay: {t:1.0f} seconds remain.".format(t=boot_delay), end="")
    boot_delay -= 1
    sleep(1)
print("")

main()
