import board
import gc
import time
print("DEBUG: preload  " + str(gc.mem_free()) + " bytes free")
import adafruit_bno055
print("DEBUG: postload " + str(gc.mem_free()) + " bytes free")

IMU_CALIBRATION_PROFILE = "imu_profile.txt" 
class IMU_calibrator:
    def __init__(self, gyr_offset, acc_offset, mag_offset):
        self.gyr_offest = [0, 0, 0]
        self.acc_offest = [0, 0, 0]
        self.mag_offest = [0, 0, 0]

def I2C_check_init(i2c):
    if i2c != board.I2C():
        print("Error: Board I2C improperly initialized.")
        return 1
    else:
        return 0

def addr_scan(i2c):
    if i2c.try_lock() == True:
        addrs = i2c.scan()
        i2c.unlock()
        return addrs
    else:
        return []

def IMU_init(i2c):
    IMU = 0
    IMU = adafruit_bno055.BNO055_I2C(i2c) 
    IMU.set_normal_mode()
    IMU.mode = adafruit_bno055.NDOF_MODE
    if IMU:
        print("DEBUG: IMU connected")
        return IMU
    else:
        print("DEBUG: IMU not connected")
        return 1

def IMU_calibrate(IMU, IMU_calibration_profile):
    if IMU.calibrated is True:
        print(" IMU: IMU calibrated")
    else:
        print(" IMU: IMU not calibrated")
        while IMU.calibrated is not True:
            cal = list(IMU.calibration_status)
            things = ["sys:   ", "gyro:  ", "accel: ", "mag:   "]
            print("     -> Calibration:")
            for i in range(0,4):
                print("          -> " + things[i] + str(cal[i]))
            time.sleep(1)
