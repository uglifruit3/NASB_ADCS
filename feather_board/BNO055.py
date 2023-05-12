# This is the custom driver for the Adafruit BNO055 Inertial Measurement Unit

# python and circuitpython libraries
import board
from time import sleep
import adafruit_bno055
from sys import exit
from digitalio import DigitalInOut, Direction, Pull

from CONFIG import *
# system routine libraries
import MASTER_PROCESS

#==========================#
# Custom classes           #
#==========================#

# IMU class. Inherits adafruit bno055 
class Inertial_Measurement_Unit(adafruit_bno055.BNO055_I2C):
    def __init__(self, i2c, rst=0):
        # initialize class assets from adafruit_bno055.BNO055
        super().__init__(i2c)
        # configure to default modes
        self.set_normal_mode()
        self.mode = adafruit_bno055.MAGGYRO_MODE

        # setting up reset pin
        self.reset_T = rst

        # calibration 
        # note that the built-in accelerometer is excluded in all calibration routines, as it will not see use in this implementation
        # offsets stored as arrays  x  y  z
        self.gyr_offsets_T =       [0, 0, 0]
        self.mag_offsets_T =       [0, 0, 0]
        # calibration statuses initialized to 0
        self.cal_stats_T = {
                "sys": 0,
                "gyro":0,
                "mag": 0
        }

    # refreshes internal representation of calibration status
    def fetch_calibration_status(self):
        try:
            tmp = list(self.calibration_status)
        except OSError:
            MASTER_PROCESS.announce_event("IMU", "ERROR", f"Bad read on calibration register(s) on read {self.calib_reads}.")
        else:
            self.cal_stats_T["sys"] = tmp[0] 
            self.cal_stats_T["gyro"] = tmp[1] 
            self.cal_stats_T["mag"] = tmp[3] 

    # mode determines what sensors need to be calibrated for the IMU to consider itself calibrated
    # sensor be a key for cal_stats_T dict listed above. Passing sensor="all" will scan all sensors.
    def is_calibrated(self, sensor="all"):
        self.fetch_calibration_status()
        if sensor == "all": 
            for i in self.cal_stats_T:
                if self.cal_stats_T[i] != 3:
                    return False
        else:
            if self.cal_stats_T[sensor] != 3:
                return False

        return True

    # reads current sensor offset settings from IMU registers
    def read_IMU_offsets(self):
        self.gyr_offsets_T = list(self.offsets_gyroscope)
        self.mag_offsets_T = list(self.offsets_magnetometer)

    # reads sensor offset settings from a profile 
    def read_profile_offsets(self, profile=F_IMU_CALIBRATION_PROFILE):
        try:
            infile = open(profile, "r")
        except OSError:
            MASTER_PROCESS.announce_event("IMU", "ERROR", "Could not open calibration profile {s:s}.".format(s=profile))
            return True
        else:
            tmp = infile.readline()
            self.gyr_offsets_T = tmp.split(" ")
            tmp = infile.readline()
            self.mag_offsets_T = tmp.split(" ")
            MASTER_PROCESS.announce_event("IMU", "DEBUG", "Read calibration offsets from file {s:s}.".format(s=profile))
            infile.close()
            return False

    # writes sensor offset settings to IMU registers
    def write_IMU_offsets(self):
        tmp = self.mode
        self.mode = adafruit_bno055.CONFIG_MODE
        self.offsets_gyroscope    = tuple(self.gyr_offsets_T)
        self.offsets_magnetometer = tuple(self.mag_offsets_T)
        self.mode = tmp

    # writes sensor offset settings to profile
    def write_profile_offsets(self, profile=F_IMU_CALIBRATION_PROFILE):
        try: 
            with open(profile, "w") as outfile:
                outfile.write("{x} {y} {z}\n".format(x=self.gyr_offsets_T[0], y=self.gyr_offsets_T[1], z=self.gyr_offsets_T[2]))
                outfile.write("{x} {y} {z}\n".format(x=self.mag_offsets_T[0], y=self.mag_offsets_T[1], z=self.mag_offsets_T[2]))
                outfile.flush()
        except OSError as err:
            if err.args[0] == 28:
                MASTER_PROCESS.announce_event("IMU", "ERROR", "Filesystem full. Unable to write file {s:s}.".format(s=profile))
            else:
                MASTER_PROCESS.announce_event("IMU", "ERROR", "Filesystem not writable. Unable to write file {s:s}.".format(s=profile))


    # calibrates the IMU. 
    # Automatic calibration attempts to read from a profile
    # Interactive calibration waits for the user to correctly calibrate the IMU
    def calibrate(self, auto_cal=True, inter_cal=True, profile=F_IMU_CALIBRATION_PROFILE):
        # if the system is already calibrated
        if self.is_calibrated() is True:
            MASTER_PROCESS.announce_event("IMU", "INFO", "IMU calibrated.")
            return
        # the system must be calibrated
        # read from file to calibrate
        if auto_cal is True:
            err = self.read_profile_offsets(profile=profile)
            if err is False:
                self.write_IMU_offsets()

            self.fetch_calibration_status()
            if self.is_calibrated() is True:
                MASTER_PROCESS.announce_event("IMU", "INFO", "IMU calibrated.")
                return
            else:
                MASTER_PROCESS.announce_event("IMU", "INFO", "IMU not calibrated.")

        # allow user to attempt calibration interactively
        if inter_cal is True and SYS_STATE.terminal_output is True:
            # need to enter fusion mode for calibration algorithm to run
            orig_mode = self.mode
            self.mode = adafruit_bno055.NDOF_MODE
            MASTER_PROCESS.announce_event("IMU", "INFO", "Entering interactive calibration.")

            while self.is_calibrated() is False:
                print("\r   ", end="")
                for sensor in self.cal_stats_T:
                    print(sensor + ": " + str(self.cal_stats_T[sensor]) + "   ", end="")
                sleep(0.1)
            print("")

            # save sensor offsets to default calibration profile and return to original sensor modes
            self.mode = orig_mode
            MASTER_PROCESS.announce_event("IMU", "INFO", "IMU calibrated.")
            if SYS_STATE.system_read_only is False:
                self.read_IMU_offsets()
                self.write_profile_offsets()

    def check_init(self, i2c):
        if type(self) is not type(Inertial_Measurement_Unit(i2c)):
            MASTER_PROCESS.announce_event("IMU", "ERROR", "IMU improperly initialized.")
            return 1
        else:
            MASTER_PROCESS.announce_event("IMU", "DEBUG", "IMU connected.")
            return 0
