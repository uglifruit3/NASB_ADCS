# This is the custom driver for the L293D H-bridges, which control the 3 onboard magnetic coils

import board
import pwmio

#==========================#
# Custom classes           #
#==========================#

class H_Bridge_Coil():
    # accepts the digital output pins (board.DX, for example) for use as the forward and backward signals to the H-bridge
    def __init__(self, f_pin, b_pin):
        # state is -1 for backward, 0 for off, 1 for forward
        self.state = 0
        self.forward  = pwmio.PWMOut(f_pin, frequency=5000, duty_cycle=0)
        self.backward = pwmio.PWMOut(b_pin, frequency=5000, duty_cycle=0)

    # accepts a number between 0 and 1, self.state should be set to specify direction
    def set_duty_cycle(self, dc):
        # 65535 is 2**15, duty_cycle requires a fraction of 16-bit max int
        # abs(self.state) and (-1|+1 + self.state)/2 sets power in either direction
        self.backward.duty_cycle = abs(self.state*int((-1+self.state)*dc*65535 / 2))
        self.forward.duty_cycle  = abs(self.state*int((1+self.state)*dc*65535 / 2))

#==========================#
# Custom functions         #
#==========================#

def init_hbridge_coils(C1F, C1B, C2F, C2B, C3F, C3B):
    return ( H_Bridge_Coil(C1F, C1B), 
             H_Bridge_Coil(C2F, C2B),
             H_Bridge_Coil(C3F, C3B) )

#==========================#
# Global declarations      #
#==========================#

D_COILS = init_hbridge_coils(board.D2, board.D3, board.D4, board.D5, board.D6, board.D7)
