# This is the system routine library for all 4XX series commands

from time import monotonic, sleep
from math import sqrt, isnan

from CFG import *
import MASTER_PROCESS

import CMDS_2

#==========================#
# Assist functions         #
#==========================#
# TODO remove testing once fully validated and simplified
# TODO low-pass filter to remove noisy data
def get_bdot_v0():
    # Get B_dot
    t_i = monotonic()
    B_old = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    sleep(0.02)
    B = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    dt = monotonic() - t_i

    B_dot = [ (B[0] - B_old[0])/dt,
              (B[1] - B_old[1])/dt,
              (B[2] - B_old[2])/dt 
            ]

    return B_dot

# TODO consider obtaining more sample passes to better de-noise the data
def get_bdot_v1():
    # define time constant
    # N_d = 10 is calibrated for current refresh every ~0.02 sec
    N_d = 10
    # get samples
    t_0 = monotonic()
    B_0 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    sleep(0.02)
    B_1 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    t_1 = monotonic()
    dt = t_1 - t_0

    # perform low-pass filtering of samples
    # using tustin-transformed 1st order xfer function for de-noising. 
    # Tuned to body rotation rate of 0.025Hz w/decade separation
    B_dot01 = [ (B_1[0]-B_0[0]) / dt,
                (B_1[1]-B_0[1]) / dt,
                (B_1[2]-B_0[2]) / dt
              ]

    # get another B_body sample
    sleep(0.02)
    B_2 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    t_2 = monotonic()
    dt = t_2 - t_1
    # perform second pass of filtering; return this value
    B_dot12 = [ ((B_dot01[0]/N_d) + B_1[0]-B_0[0]) / (dt+(1/N_d)),
                ((B_dot01[1]/N_d) + B_1[1]-B_0[1]) / (dt+(1/N_d)),
                ((B_dot01[2]/N_d) + B_1[2]-B_0[2]) / (dt+(1/N_d))
              ]

    return B_dot12

def get_bdot_v2(time_up):
    # need to optimize for avg sample time ~0.00623
    # define time constant
    # N_d = 10 is calibrated for .025Hz
    N_d = 8
    B_dot = [0, 0, 0]

    t_start = monotonic()
    # initialize sample
    t_0 = monotonic()
    B_0 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    while monotonic()-t_start < (time_up-0.01):
        # get new sample and dt
        B_1 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        t_1 = monotonic()
        dt = t_1 - t_0

        # perform low-pass filtering of samples
        # using tustin-transformed 1st order xfer function for de-noising. 
        # Tuned to body rotation rate of 0.025Hz w/decade separation
        B_dot = [ ((B_dot[0]/N_d) + B_1[0]-B_0[0]) / (dt+(1/N_d)),
                  ((B_dot[1]/N_d) + B_1[1]-B_0[1]) / (dt+(1/N_d)),
                  ((B_dot[2]/N_d) + B_1[2]-B_0[2]) / (dt+(1/N_d))
                ]

        t_0 = t_1
        B_0 = B_1

    return B_dot

def get_bdot_v3(time_up):
    # TODO attempt to implement an averaging filter to denoise bdot data?
    # TODO consider collecting time history of B_body to analyze noise
    t_start = monotonic()
    # for averaging
    B_dot_tot = [0, 0, 0]
    cnt = 0

    while monotonic()-t_start < time_up:
        t_0 = monotonic()
        B_0 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        B_1 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        t_1 = monotonic()
        dt = t_1-t_0

        B_dot_tot[0] += (B_1[0]-B_0[0]) / dt
        B_dot_tot[1] += (B_1[1]-B_0[1]) / dt
        B_dot_tot[2] += (B_1[2]-B_0[2]) / dt
        cnt += 1

    #print(f"Bdot in {cnt} passes")
    B_dot_tot[0] = B_dot_tot[0] / cnt
    B_dot_tot[1] = B_dot_tot[1] / cnt
    B_dot_tot[2] = B_dot_tot[2] / cnt
    return B_dot_tot

def get_bdot_v4(time_up):
    # need to optimize for avg sample time ~0.00623
    # define time constant
    # N_d = 10 is calibrated for .025Hz
    N_d = 8
    B_dot = [0, 0, 0]
    B_dot_tot = [0, 0, 0]
    cnt = 0

    t_start = monotonic()
    # initialize sample
    t_0 = monotonic()
    B_0 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    while monotonic()-t_start < (time_up-0.01):
        # get new sample and dt
        B_1 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        t_1 = monotonic()
        dt = t_1 - t_0

        # perform low-pass filtering of samples
        # using tustin-transformed 1st order xfer function for de-noising. 
        # Tuned to body rotation rate of 0.025Hz w/decade separation
        B_dot = [ ((B_dot[0]/N_d) + B_1[0]-B_0[0]) / (dt+(1/N_d)),
                  ((B_dot[1]/N_d) + B_1[1]-B_0[1]) / (dt+(1/N_d)),
                  ((B_dot[2]/N_d) + B_1[2]-B_0[2]) / (dt+(1/N_d))
                ]

        t_0 = t_1
        B_0 = B_1

        B_dot_tot[0] += B_dot[0]
        B_dot_tot[1] += B_dot[1]
        B_dot_tot[2] += B_dot[2]
        cnt += 1

    B_dot_tot[0] /= cnt
    B_dot_tot[1] /= cnt
    B_dot_tot[2] /= cnt
    return B_dot

def get_bdot_v5(time_up):
    # TODO attempt to implement an averaging filter to denoise bdot data?
    # TODO consider collecting time history of B_body to analyze noise
    t_start = monotonic()
    # for averaging
    alpha = 0.5
    B_dot_tot = [0, 0, 0]
    cnt = 0

    t_0 = monotonic()
    B_0 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
    while monotonic()-t_start < time_up-0.01:
        B_1 = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        t_1 = monotonic()
        dt = t_1-t_0
        B_1[0] = alpha*B_1[0] + (1-alpha)*B_0[0]
        B_1[1] = alpha*B_1[1] + (1-alpha)*B_0[1]
        B_1[2] = alpha*B_1[2] + (1-alpha)*B_0[2]

        B_dot_tot[0] += (B_1[0]-B_0[0]) / dt
        B_dot_tot[1] += (B_1[1]-B_0[1]) / dt
        B_dot_tot[2] += (B_1[2]-B_0[2]) / dt
        cnt += 1

        t_0 = t_1
        B_1 = B_0

    print(f"Bdot in {cnt} passes")
    B_dot_tot[0] = B_dot_tot[0] / cnt
    B_dot_tot[1] = B_dot_tot[1] / cnt
    B_dot_tot[2] = B_dot_tot[2] / cnt
    return B_dot_tot

def get_bdot_v6(time_up):
    cnt = 0
    B_0 = [0, 0, 0]
    t_start = monotonic()
    while monotonic()-t_start < (time_up/2)-.05:
        data = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        cnt += 1
        for i in range(0,3):
            B_0[i] += data[i]
    t_0 = monotonic()
    for B in B_0:
        B /= cnt

    cnt = 0
    B_1 = [0, 0, 0]
    t_start = monotonic()
    while monotonic()-t_start < (time_up/2)-.05:
        data = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        cnt += 1
        for i in range(0,3):
            B_1[i] += data[i]
    t_1 = monotonic()
    for B in B_1:
        B /= cnt

    dt = t_1 - t_0
    B_dot = [ (B_1[0] - B_0[0])/dt,
              (B_1[1] - B_0[1])/dt,
              (B_1[2] - B_0[2])/dt 
            ]

    return B_dot

def bdot_controller():
    B_dot = get_bdot_v3(0.1)

    # for testing purposes
    print(f"     B_dot = {B_dot} T/s")

    # B_dot control constants
    # TODO ensure that these values are correct and usable
    # original sim values below:
    # KBdot = 1e5      # gain
    # Bdotmin = 0.1e-6 # (T) minimum rate of change for motor use
    # msat = 0.1       # (A/m^2) max dipole moment commandable
    # experimental values
    KBdot = 1e-2      # gain
    Bdotmin = 0.1e-6 # (T) minimum rate of change for motor use
    msat = 0.0359       # (A/m^2) max dipole moment commandable

    # compute required dipole moment
    m = [0, 0, 0] # initialize to 0
    if sqrt(sum(pow(i,2) for i in B_dot)) > Bdotmin:
        m[0] = -1*KBdot*B_dot[0]
        m[1] = -1*KBdot*B_dot[1]
        m[2] = -1*KBdot*B_dot[2]

    # limit commanded dipole moment
    for i in range(0,3):
        if abs(m[i]) > msat:
            m[i] = (m[i]/abs(m[i])) * msat

    return m

def bdot_controller_timer(t):
    B_dot = get_bdot_v3(0.1)

    # for testing purposes
    print(f">{t:.5f} {B_dot[0]} {B_dot[1]} {B_dot[2]}")

    # B_dot control constants
    # TODO ensure that these values are correct and usable
    # original sim values below:
    # KBdot = 1e5      # gain
    # Bdotmin = 0.1e-6 # (T) minimum rate of change for motor use
    # msat = 0.1       # (A/m^2) max dipole moment commandable
    # experimental values
    KBdot = 1e-2      # gain
    Bdotmin = 0.1e-6 # (T) minimum rate of change for motor use
    msat = 0.0359       # (A/m^2) max dipole moment commandable

    # compute required dipole moment
    m = [0, 0, 0] # initialize to 0
    if sqrt(sum(pow(i,2) for i in B_dot)) > Bdotmin:
        m[0] = -1*KBdot*B_dot[0]
        m[1] = -1*KBdot*B_dot[1]
        m[2] = -1*KBdot*B_dot[2]

    # limit commanded dipole moment
    for i in range(0,3):
        if abs(m[i]) > msat:
            m[i] = (m[i]/abs(m[i])) * msat

    return m

def m_to_dutycycle(m):
    v = (m*18.9*4) / (300*3.1415*0.02*0.02)
    return v/7.2
