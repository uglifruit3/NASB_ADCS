# python and circuitpython libraries
from math import sin,sqrt
# import adafruit_bno055
from time import monotonic, sleep
from analogio import AnalogIn
import board

from CFG import *
# system routine libraries
import MASTER_PROCESS

# command routine libraries
import CMDS_0
import CMDS_2
import CMDS_4

def test_detumble():
    cnt = 0
    B = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    B_dot = [0, 0, 0]
    quit = False
    while quit is False:
        try:
            t_i = monotonic()
            while monotonic()-t_i < 0.9:
                pass

            for i in D_COILS:
                i.set_duty_cycle(0)
            cnt+=1

            t_start = monotonic()
            data = CMDS_4.get_bdot(0.1, B, B_dot)
            B = data[0]
            B_dot = data[1]
            print(f"[{cnt}] B: {data[0]} || B_dot: {data[1]}, mag: {sqrt(sum(pow(i,2) for i in data[1]))}")
            m = CMDS_4.bdot_controller(data[1])
            print(f"[{cnt}] Ordered m = {m} in {monotonic()-t_start}s\n")
            while monotonic()-t_i < 1.0:
                pass

            for i in range(0,3):
                dc = CMDS_4.m_to_dutycycle(m[i])
                D_COILS[i].set_duty_cycle(dc)
        except KeyboardInterrupt:
            quit = True

def get_bdot_realtime():
    while True:
        t_i = monotonic()
        B_old = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        sleep(0.05)
        B = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        dt = monotonic() - t_i

        B_dot = [ (B[0] - B_old[0])/(dt*1e6),
                  (B[1] - B_old[1])/(dt*1e6),
                  (B[2] - B_old[2])/(dt*1e6)
                ]

        print(f"\r     B_dot = {B_dot[0]:+02.6e}, {B_dot[1]:+02.6e}, {B_dot[2]:+02.6e} T/s", end="")


def test_mag_data():
    t_start = monotonic()
    B = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    B_dot = [0, 0, 0]
    quit = False
    while quit is False:
        try:
            data = CMDS_4.get_bdot_v2(0.1, B, B_dot)
            B = data[0]
            B_dot = data[1]
            data3 = [0, 0, 0, 0, 0, 0]
            for i in range(0,3):
                data3[i]   = B[i]*1e5
                data3[i+3] = B_dot[i]*1e6
            print((data3[3], data3[4], data3[5]))
            sleep(0.9)
        except KeyboardInterrupt:
            quit = True


def fade_hbridge():
    cnt = 0
    while True:
        pwr = sin(cnt)
        for i in D_COILS:
            i.set_duty_cycle(pwr)
        print(f"\rDuty cycle: {pwr:.4f}", end="")
        cnt += 0.004
        sleep(0.001)

def mag_timer():
    t_0 = monotonic()
    B_0 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    B_1 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    t_1 = monotonic()
    dt = t_1 - t_0

    return dt

def mag_history():
    t_0 = monotonic()
    while True:
        CMDS_4.bdot_controller_timer(monotonic()-t_0)
        sleep(0.9)

# TODO need to figure out best pull-down resistance for biggest voltage range
def test_photor():
    ain = AnalogIn(board.A0)
    while True:
        print(f"Voltage: {ain.value*3.3/65536:4.2f}V", end="\r")
        sleep(0.1)
