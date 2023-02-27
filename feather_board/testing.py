# python and circuitpython libraries
from math import sin
# import adafruit_bno055
from time import monotonic, sleep

from CFG import *
# system routine libraries
import MASTER_PROCESS 

# command routine libraries
import CMDS_0
import CMDS_2
import CMDS_4

def test_bdot():
    cnt = 0
    while True:
        t_i = monotonic()
        while monotonic()-t_i < 0.9:
            pass

        for i in D_COILS:
            i.set_duty_cycle(0)
        cnt+=1

        print(f"[{cnt}] B_body: {CMDS_2.QUERY_MAGNETIC_FIELD_DATA()}")
        t_start = monotonic()
        m = CMDS_4.bdot_controller()
        print(f"[{cnt}] Ordered m = {m} in {monotonic()-t_start}s\n")
        while monotonic()-t_i < 1.0:
            pass

        for i in range(0,3):
            dc = CMDS_4.m_to_dutycycle(m[i])
            D_COILS[i].set_duty_cycle(dc)

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
    while True:
        t_start = monotonic()
        cnt = 0
        B_tot = [0, 0, 0]
        while monotonic()-t_start < 0.045:
            data = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
            cnt += 1
            print(f"{data[0]:03.1f} {data[1]:03.1f} {data[2]:03.1f}", end="")
            for i in range(0,3):
                B_tot[i] += data[i]
            print(f" || {B_tot[0]/cnt:03.2f} {B_tot[1]/cnt:03.2f} {B_tot[2]/cnt:03.2f}", end="\r")
        print("")


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
