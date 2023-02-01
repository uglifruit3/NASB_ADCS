import board
from digitalio import DigitalInOut, Direction, Pull
from math import atan2, asin, pow
from time import sleep
from storage import remount

def addr_scan(i2c):
    if i2c.try_lock() == True:
        addrs = i2c.scan()
        i2c.unlock()
        return addrs
    else:
        return []

def disp_I2C_scan(i2c):
    print("I2C: DEBUG: Scanning I2C addresses:")
    addrs = addr_scan(i2c)
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

def init_dig_input(pin=0):
    if pin == 0:
        return 0

    inp = DigitalInOut(pin)
    inp.direction = Direction.INPUT
    inp.pull = Pull.DOWN

    return inp

def init_dig_output(pin=0):
    if pin == 0:
        return 0

    out = DigitalInOut(pin)
    out.direction = Direction.OUTPUT

    return out

def chk_fs_waccess(write_pin):
    if write_pin == 0 or write_pin.value is False:
        print("SYS: DEBUG: Filesystem unwriteable.")
        return False
    else:
        print("SYS: DEBUG: Filesystem writeable.")
        return True

def boot_sequence():
    w_access_pin = board.D7
    write_pin = init_dig_input(board.D7)

    if chk_fs_waccess(write_pin) is True:
        remount("/", False)
