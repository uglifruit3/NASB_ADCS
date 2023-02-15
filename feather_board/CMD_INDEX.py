from CFG import *
# system routine libraries
import MASTER_PROCESS 

# command routine libraries
import CMDS_0
import CMDS_2
import CMDS_4

class Command():
    def __init__(self, index, priority, function, n_args=0):
