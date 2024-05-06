"""
BP821A functions
"""
import pyvisa
import pyvisa
import time
from instruments.instruments_name import *
class Power_DP821A:

    def __init__(self, pRmObject, pInstruID):
        """
        actual object initial
        :param pRmObject: visa object name
        :param pInstruID: instrument ID
        """
        # print(pRmObject.list_resources())
        self.instrument = pRmObject.open_resource(pInstruID)      # open instrument through instruID
        self.instrument.read_termination = "\n"
        self.instrument.timeout = 100000                          # set instrument timeout
        # print(self.instrument.query("*IDN?"))                   # print instrument ID

    def reset(self):
        "Reset the Device"
        self.instrument.write("*RST")

    def set_volta_current(self,ch = 1,vol = 3.3,current = 1):
        """

        :param ch:
        :param vol:
        :param current:
        :return:
        """
        self.instrument.write(f"SOUR{ch}:VOLT {vol}")
        self.instrument.write(f"SOUR{ch}:CURR {current}")

        if (ch == 1) and (current > 1):
            print("Ch1 can not outpur current over 1")

    def turn_on_off(self,ch,switch):
        """
        :param ch:
        :param switch: "ON"/""OFF
        :return:
        """
        self.instrument.write(f"OUTP CH{ch},{switch}")

    def read_voltage(self,ch):
        voltage = self.instrument.query(f"MEASure:VOLTage? CH{ch}")
        # print(voltage)
        return voltage

    def read_current(self,ch):
        current = self.instrument.query(f"MEASure:CURRent? CH{ch}")
        # print(current)
        return current

    def read_power(self,ch):
        power = self.instrument.query(f"MEASure:POWer? CH{ch}")
        # print(power)
        return power




if __name__ == "__main__":
    power = Power_DP821A(pyvisa.ResourceManager(), "USB0::0x1AB1::0x0E11::DP8E244400636::INSTR")
    power.reset()
    power.set_volta_current(1,3.3,1)
    power.turn_on_off(1,"ON")
    power.read_voltage(1)
    power.read_current(1)
    power.read_power(1)

