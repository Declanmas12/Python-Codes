from pymeasure.instruments import list_resources
list_resources()

from pymeasure.instruments.keithley import Keithley2400

sourcemeter = Keithley2400("USB0::0x05E6::0x2460::04516939::INSTR")

sourcemeter.id