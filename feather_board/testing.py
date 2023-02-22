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
        print("Coils off")
        cnt+=1

        while monotonic()-t_i < 1.0:
            pass
        print(f"[{cnt}] B_body: {CMDS_2.QUERY_MAGNETIC_FIELD_DATA()}")
        m = CMDS_4.bdot_controller()
        print(f"[{cnt}] Ordered m = {m}")

        for i in range(0,3):
            dc = CMDS_4.m_to_dutycycle(m[i])
            if dc < 0:
                D_COILS[i].state = -1
            elif dc > 0:
                D_COILS[i].state = 1
            else:
                D_COILS[i].state = 0

            D_COILS[i].set_duty_cycle(abs(dc))
        print("\nCoils on")

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
    while True:
        data = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        print("{c1:06.2f}> {e1:06.2f} {e2:06.2f} {e3:06.2f}".format(c1=monotonic()-t_start, e1=data[0], e2=data[1], e3=data[2]), end="\r")

def fade_hbridge():
    for i in D_COILS:
        i.state = 1
    while True:
        pwr = (sin(cnt) + 1) / 2
        for i in D_COILS:
            if pwr == 0:
                i.state = i.state*-1
            i.set_duty_cycle(pwr)
        print(f"\rDuty cycle: {pwr:.4f}", end="")
        cnt += 0.001
        sleep(0.001)

def mag_timer():
    t_0 = monotonic()
    B_0 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    B_1 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    t_1 = monotonic()
    dt = t_1 - t_0

    return dt
