import pyvisa
import time
from instruments.instruments_name import *

"""
Brand : Gwinstek
Function : dmm_gwinstek_api to get voltage current and frequnecy

"""


class Multimemter:

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


    def volt_meter_initial(self):
        """
        configure DMM work in voltage meter mode
        :note: using immediately trigger mode
        :return: none
        """
        self.instrument.write("CONF:VOLT:DC")
        self.instrument.write("SAMP:COUN 1")
        self.instrument.write("TRIG:SOUR IMM")


    def current_meter_initial(self):
        """
        configure DMM work in current meter mode
        :note: using immediately trigger mode
        :return: none
        """
        self.instrument.write("CONF:CURR:DC")
        self.instrument.write("SAMP:COUN 1")
        self.instrument.write("TRIG:SOUR IMM")


    def frequency_meter_initial(self):
        """
        configure DMM work in frequency meter mode
        :note: using immediately trigger mode
        :return: none
        """
        self.instrument.write("CONF:FREQ")
        self.instrument.write("SAMP:COUN 1")
        self.instrument.write("TRIG:SOUR IMM")


    def measure_data(self):
        """
        read back measurement data
        :note: this function should be used when DMM work in immediately trigger mode
        :return: val_q - measured value. float format
        """
        val_q = self.instrument.query("READ?")
        # print(type(val_q))
        return float(val_q)



    def read_voltage(self):
        """
        read back measurement data
        :note: this function can be used without initial
        :return: val_q - measured value. float format
        """
        vol_q = self.instrument.query("MEASURE:VOLTAGE:DC?")
        return float(vol_q)

    def read_voltage_fine(self):
        """
        read back measurement data
        :note: this function can be used without initial, using double interval collection
        :return: val_q - measured value. float format
        """
        while(1):
            val1 = float(self.instrument.query("MEASURE:VOLTAGE:DC?"))
            time.sleep(0.01)                   # you can set the time's precision when use
            val2 = float(self.instrument.query("MEASURE:VOLTAGE:DC?"))
            if (abs(val1-val2) < 0.0005):      # you can set the voltage's precision when use
                break
        return float((val1+val2)/2)

    def read_current(self):
        """
        read back measurement data
        :note: this function can be used without initial
        :return: cur_q - measured value. float format
        """
        cur_q = float(self.instrument.query("MEASURE:Current:DC?"))
        return cur_q

    def read_freq(self):
        """
        read back measurement data
        :note: this function can be used without initial
        :return: freq_q - measured value. float format
        """
        freq_q = float(self.instrument.query("MEASURE:Frequency?"))
        return freq_q

"""Example"""
if __name__ == '__main__':
    dmm = Multimemter(pyvisa.ResourceManager(),dmm_9060_num14_id)
    dmm = Multimemter(pyvisa.ResourceManager(), dmm_34461_num1_id)
    print(dmm.read_voltage())
    time.sleep(1)
    print(dmm.read_current())
    time.sleep(1)
    print(dmm.read_freq())
