import board
import busio
import time
import test

I2C = busio.I2C(scl=board.D0, sda=board.D1)

def main():
    time.sleep(.2)
    print("Scanning I2C addresses:")
    addrs = test.addr_scan(I2C)
    if addrs == []:
            print(" None found.")
    else:
            print(" Addresses found:")
            print("  ", end="")
            print([hex(dev_addr) for dev_addr in addrs])

main()
IMU = test.IMU_init(I2C)

test.IMU_calibrate(IMU, 0)

while True:
    print(IMU.euler)
    time.sleep(0.25)
