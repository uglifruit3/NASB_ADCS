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
def bdot_controller(Bdot=[float('nan'), float('nan'), float('nan')]):
    # Get B_dot
    if not isnan(Bdot[0]):
        B_dot = Bdot
    else:
        t_i = monotonic()
        B_old = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        sleep(0.02)
        B = CMDS_2.QUERY_MAGNETIC_FIELD_DATA()
        dt = monotonic() - t_i

        B_dot = [ (B[0] - B_old[0])/(dt*1e6),
                  (B[1] - B_old[1])/(dt*1e6),
                  (B[2] - B_old[2])/(dt*1e6) 
                ]

    print(f"     B_dot = {B_dot} T/s")

    # B_dot control constants
    # ensure that these values are correct and usable
    KBdot = 1e5 # gain
    Bdotmin = 0.1e-6 # minimum rate of change for motor use
    msat = 0.1 # max dipole moment commandable

    # compute required dipole moment
    m = [0, 0, 0]
    if sqrt(sum(pow(i,2) for i in B_dot)) > Bdotmin:
        m[0] = -1*KBdot*B_dot[0]
        m[1] = -1*KBdot*B_dot[1]
        m[2] = -1*KBdot*B_dot[2]

    # limit commanded dipole moment
    for i in range(0,3):
        if abs(m[i]) > msat:
            m[i] = (m[i]/abs(m[i])) * msat

    return m
