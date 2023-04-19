# This is the system routine library for all 4XX series commands

from time import monotonic, sleep
from math import sqrt, isnan

from CONFIG import *
import MASTER_PROCESS

import CMDS_2

#==========================#
# Assist functions         #
#==========================#
def get_bdot(time_up, B_old, B_dot_old):
    # N_d = 0.5 is calibrated for 10 deg/s maximum rate of rotation
    N_d = 0.5

    # initialize filter values to maintain convergence 
    # these MUST be carried over from previous runs
    t_start = monotonic()
    t_0 = t_start-0.9
    B_dot = [B_dot_old[0], B_dot_old[1], B_dot_old[2]]
    B_0 = [B_old[0], B_old[1], B_old[2]]
    while monotonic()-t_start < (time_up-0.01):
        # get new sample and dt
        B_1 = CMDS_2._200_QUERY_MAGNETIC_FIELD_DATA()
        t_1 = monotonic()
        dt = t_1 - t_0

        # perform low-pass filtering of samples
        # using tustin-transformed 1st order xfer function for de-noising.
        B_dot = [ ((B_dot[0]/N_d) + B_1[0]-B_0[0]) / (dt+(1/N_d)),
                  ((B_dot[1]/N_d) + B_1[1]-B_0[1]) / (dt+(1/N_d)),
                  ((B_dot[2]/N_d) + B_1[2]-B_0[2]) / (dt+(1/N_d))
                ]
        # set old samples
        t_0 = t_1
        B_0 = B_1

    # sends back B and B_dot to be used for future filter passes
    return [B_0, B_dot]

def bdot_controller(B_dot):
    # B_dot control constants
    # TODO ensure that these values are correct and usable
    # original sim values below:
    # KBdot = 1e5      # gain
    # Bdotmin = 0.1e-6 # (T) minimum rate of change for motor use
    # msat = 0.1       # (A/m^2) max dipole moment commandable
    # experimental values
    KBdot = 1e4      # gain
    Bdotmin = 0.9e-6 # (T) minimum rate of change for motor use
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
    # compute and return voltage required for magnetorquers
    v = (m*18.9*4) / (300*3.1415*0.02*0.02)
    return v/7.2

# TODO will need to implement asycronous processing with asyncio to handle tasks going forward
# Bdot controller above could need to be written in a manner sensitive to this requirement

def _400_DETUMBLE():
    pass

def _401_ORIENT_TO_NADIR():
    pass

def _402_TERMINATE_ATTITUDE_COMMAND():
    pass
