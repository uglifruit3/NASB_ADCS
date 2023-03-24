import board
from analogio import AnalogIn

from MASTER_PROCESS import announce_event

class Sun_Sensor():
    def __init__(self, input_pin):
        self.input = AnalogIn(input_pin)
        # these values are hardware-specific
        self.min_voltage = 0.425
        self.max_voltage = 3.142
    def voltage(self):
        return self.input.value*3.3 / 65536
    def light_level(self):
        return (self.voltage()-self.min_voltage) / (self.max_voltage-self.min_voltage)

# initializes an array of sun sensors, each specified in the array of analog input pins
def init_sun_sensors(input_pins):
    cnt = 0
    sensors = []
    for i in input_pins:
        sensors.append(Sun_Sensor(i))
        cnt += 1

    announce_event("CSS", "DEBUG", f"Initialized array of {cnt} coarse sun sensors.")
    return sensors
