import board
import busio
from time import sleep
import adafruit_bno055
from sys import exit
from digitalio import DigitalInOut, Direction, Pull

# default location of IMU calibration offsets
IMU_CALIBRATION_PROFILE = "/imu_profile.txt" 

# IMU class. Inherits adafruit bno055 
class Inertial_Measurement_Unit(adafruit_bno055.BNO055_I2C):
    def __init__(self, i2c, rst=0, sensor_mode=0):
        # initialize class assets from adafruit_bno055.BNO055
        super().__init__(i2c)
        # configure to default modes
        self.set_normal_mode()
        # TODO need to set mode in accordance to mode passed through class initiator (sensor_mode)
        self.mode = adafruit_bno055.NDOF_MODE
        self.calibration_mode_T = sensor_mode

        # setting up reset pin
        if rst != 0:
            self.reset_T = digitalio.DigitalInOut(rst)
            self.reset_T.direction = digitalio.Direction.OUTPUT
            # TODO need to confirm how reset works on BNO055
            self.reset_T.value = True
        else:
            self.reset_T = 0

        # calibration 
        # offsets stored as arrays  x  y  z
        self.gyr_offsets_T =         [0, 0, 0]
        self.acc_offsets_T =         [0, 0, 0]
        self.mag_offsets_T =         [0, 0, 0]
        # calibration statuses initialized to 0
        self.cal_stats_T = {
                "sys":   0,
                "gyro":  0,
                "accel": 0,
                "mag":   0
        }

    def fetch_calibration_status(self):
        try:
            tmp = list(self.calibration_status)
        except OSError:
            print("IMU: ERROR: Bad read on calibration register(s).")
            if self.reset_T == 0:
                sys.exit()
            else:
                print("IMU: WARNS: Hardware reset initiated by calibration.")
                self.hware_reset()
                return
        else:
            self.cal_stats_T["sys"]   = tmp[0] 
            self.cal_stats_T["gyro"]  = tmp[1] 
            self.cal_stats_T["accel"] = tmp[2] 
            self.cal_stats_T["mag"]   = tmp[3] 

    # mode determines what sensors need to be calibrated for the IMU to consider itself calibrated
    #  0 -> spacecraft mode (sys, gyro, mag)
    #  1 and all other -> full mode (sys, gyro, mag)
    # def is_calibrated(self, mode=self.calibration_mode_T):
    def is_calibrated(self, mode=0):
        for sensor in self.cal_stats_T:
            if self.cal_stats_T[sensor] != 3 and (mode != 0 or (mode == 0 and sensor != "accel")):
                return False
        return True

    def read_IMU_offsets(self):
        self.gyr_offsets_T = list(self.offsets_gyroscope)
        self.acc_offsets_T = list(self.offsets_accelerometer)
        self.mag_offsets_T = list(self.offsets_magnetometer)

    def read_profile_offsets(self, profile=IMU_CALIBRATION_PROFILE):
        #with open(profile, "r") as infile:
        # TODO need to fully fill
        return False
            

    def write_IMU_offsets(self):
        pass

    def write_profile_offsets(self, profile=IMU_CALIBRATION_PROFILE):
        try: 
            with open(profile, "w") as outfile:
                outfile.write("{x} {y} {z}\n".format(x=self.gyr_offsets_T[0], y=self.gyr_offsets_T[1], z=self.gyr_offsets_T[2]))
                outfile.write("{x} {y} {z}\n".format(x=self.acc_offsets_T[0], y=self.acc_offsets_T[1], z=self.acc_offsets_T[2]))
                outfile.write("{x} {y} {z}\n".format(x=self.mag_offsets_T[0], y=self.mag_offsets_T[1], z=self.mag_offsets_T[2]))
                outfile.flush()
        except OSError as err:
            if err.args[0] == 28:
                print("SYS: ERROR: Filesystem full. Unable to write file {s:s}.".format(s=profile))
            else:
                print("SYS: ERROR: Filesystem not writable. Unable to write file {s:s}.".format(s=profile))

    def calibrate(self, profile=IMU_CALIBRATION_PROFILE, auto_cal=True, inter_cal=True):
        if self.is_calibrated() is True:
            print("IMU: ANCMT: IMU calibrated.")
        else:
            print("IMU: ANCMT: IMU not calibrated.")
            
            if auto_cal is True:
                err = self.read_profile_offsets(profile=profile)
                if err is False:
                    print("IMU: DEBUG: Read calibration offsets from file {s:s}. Mode is {e}.".format(s=profile, e=self.calibration_mode_T))
                    self.write_IMU_offsets()
                else:
                    print("IMU: ANCMT: IMU not calibrated.")
                    return

                self.fetch_calibration_status()
                for sensor in self.cal_stats_T:
                    print("   " + sensor + ": " + str(self.cal_stats_T[sensor]) + "   ")

                if self.is_calibrated() is True:
                    print("IMU: ANCMT: IMU calibrated.")
                else:
                    print("IMU: ANCMT: IMU not calibrated.")

            elif inter_cal is True:
                print("IMU: ANCMT: Entering interactive calibration--mode is {e}.".format(e=self.calibration_mode_T))
                while self.is_calibrated() is False:
                    self.fetch_calibration_status()
                    print("\r   ", end="")
                    for sensor in self.cal_stats_T:
                        print(sensor + ": " + str(self.cal_stats_T[sensor]) + "   ", end="")
                    sleep(0.2)
                print("")

                self.read_IMU_offsets()
                self.write_profile_offsets()

    def check_init(self, i2c):
        if type(self) is not type(Inertial_Measurement_Unit(i2c)):
            print("IMU: ERROR: IMU improperly initialized.")
            return 1
        else:
            print("IMU: DEBUG: IMU connected.")
            return 0

    def hware_reset(self):
        # uncomment below when ready to use
        # self.reset_T.value = False
        # sleep(0.05)
        # self.reset_T.value = True
        print("IMU: DEBUG: Performed hardware reset.")
