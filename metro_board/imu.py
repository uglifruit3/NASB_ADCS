import board
import busio
from time import sleep
import adafruit_bno055
from sys import exit
from digitalio import DigitalInOut, Direction, Pull

# default location of IMU calibration offsets
IMU_CALIBRATION_PROFILE = "imu_profile.txt" 

# IMU class. Inherits adafruit bno055 
class Inertial_Measurement_Unit(adafruit_bno055.BNO055_I2C):
    def __init__(self, i2c, rst=0):
        # initialize class assets from adafruit_bno055.BNO055
        super().__init__(i2c)
        # configure to default modes
        self.set_normal_mode()
        self.mode = adafruit_bno055.NDOF_MODE

        # setting up reset pin
        if rst != 0:
            self.reset = digitalio.DigitalInOut(rst)
            self.reset.direction = digitalio.Direction.OUTPUT
            # TODO need to confirm how reset works on BNO055
            self.reset.value = True
        else:
            self.reset = 0

        # calibration offsets
        # stored as arrays  x  y  z
        self.gyr_offsets = [0, 0, 0]
        self.acc_offsets = [0, 0, 0]
        self.mag_offsets = [0, 0, 0]

    def read_IMU_offsets(self):
        self.gyr_offsets = list(self.offsets_gyroscope)
        self.acc_offsets = list(self.offsets_accelerometer)
        self.mag_offsets = list(self.offsets_magnetometer)

    def read_profile_offsets(self, profile=IMU_CALIBRATION_PROFILE):
        pass

    def write_IMU_offsets(self):
        pass

    def write_profile_offsets(self, profile=IMU_CALIBRATION_PROFILE):
        # TODO need to guard against case that filesystem not writeable by Python
        profile_obj = open(profile, "w")

        profile_obj.write("{x} {y} {z}".format(x=self.gyr_offsets[0], y=self.gyr_offsets[1], z=self.gyr_offsets[2]))
        profile_obj.write("{x} {y} {z}".format(x=self.acc_offsets[0], y=self.acc_offsets[1], z=self.acc_offsets[2]))
        profile_obj.write("{x} {y} {z}".format(x=self.mag_offsets[0], y=self.mag_offsets[1], z=self.mag_offsets[2]))

        profile_obj.close()

    def calibrate(self, profile=IMU_CALIBRATION_PROFILE, auto_calibrate=True):
        if self.calibrated is True:
            print("IMU: DEBUG: IMU calibrated.")
        else:
            print("IMU: DEBUG: IMU not calibrated.")
            print("IMU: ANCMT: Entering interactive calibration:")

            is_calibrated = False
            while is_calibrated is False:
                try:
                    is_calibrated = self.calibrated
                    tmp = self.calibration_status
                except OSError:
                    print("IMU: WARNS: Bad read on calibration register(s).")
                    if self.reset == 0:
                        sys.exit()
                    else:
                        print("IMU: WARNS: Hardware reset initiated by calibration.")
                        self.hware_reset()
                else:
                    cal = list(tmp)
                    things = ["sys", "gyro", "accel", "mag"]
                    print("\r   ", end="")
                    for i in range(0,4):
                        print(things[i] + ": " + str(cal[i]) + "   ", end="")
                sleep(0.2)
            print("")

        # TODO work out a means to write the profile

    def check_init(self, i2c):
        if type(self) is not type(Inertial_Measurement_Unit(i2c)):
            print("IMU: ERROR: IMU improperly initialized.")
            return 1
        else:
            print("IMU: DEBUG: IMU connected.")
            return 0

    def hware_reset(self):
        # uncomment below when ready to use
        # self.reset.value = False
        # sleep(0.05)
        # self.reset.value = True
        print("IMU: DEBUG: Performed hardware reset.")
