# file runs on hard reset or board power on
# configures filesystem for CircuitPython write access

# boot code is contained in testing library so that the sequence can be checked for runtime errors
from testing import boot_sequence

try:
    boot_sequence()
except:
    print("SYS: ERROR: Boot sequence error. Unable to verify boot state.")
