from CONFIG import *
# system routine libraries
import MASTER_PROCESS 

# command routine libraries
import CMDS_0
import CMDS_2
import CMDS_4

# testing routines
import testing

def main():
    MASTER_PROCESS.startup_delay()
    CMDS_0._006_QUERY_FREE_MEMORY()

# =================== #
#       MAIN          #
# =================== #

main()
# cnt = 0
# sum_t = 0
# hi = 0
# while True:
#     cnt += 1
#     t = testing.mag_timer()
#     if t > hi:
#         hi = t
#     sum_t += t
#     avg = sum_t/cnt
#     print(f"\rTime between reads: {t:10.8f} {avg:10.8f} {hi:10.8f}", end="")
MASTER_PROCESS.i2c_scan(P_I2C)
print(D_WHEEL.get_wheel_current())
D_WHEEL.get_status_errors()
print(D_WHEEL.errors)
D_WHEEL.clr_errors()
D_WHEEL.get_status_errors()
print(D_WHEEL.errors)
D_WHEEL.reset()
D_WHEEL.get_status_errors()
print(D_WHEEL.errors)
D_WHEEL.get_wheel_status()
print(f"Runtime: {D_WHEEL.sec_runtime}")
