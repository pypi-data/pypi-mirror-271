"""
    @File : smu_keithley_2450.py \n
    @Contact : yifei.su@pisemi.com \n
    @License : (C)Copyright {} \n
    @Modify Time : 2023/3/21 15:36 \n
    @Author : Yifei Su \n
    @Version : 1.0 \n
    @Description : None \n
    @Create Time : 2023/6/8 15:14 \n
    Modified by Shuai
"""

import pyvisa
import types
import time
from instruments.instruments_name import *

"""
    Class name: SmuKeithley
    Summary: keithley smu class
"""

class SmuKeithley:

    def __init__(self, pRmObject, pInstruID):
        """
        class SmuKeithley object initial function
        :param pRmObject: pyvisa object
        :param pInstruID: smu2450 instrument id
        """
        # print(pRmObject.list_resources())
        self.instrument = pRmObject.open_resource(pInstruID)      # open instrument through instruID
        self.instrument.read_termination = "\n"
        self.instrument.timeout = 100000                          # set instrument timeout
        self.identify_ins = self.instrument.query("*IDN?")


    def smu_quitRemote(self):
        # trigger_mode = self.instrument.query('TRIG:CONT?')
        # print(trigger_mode)
        self.instrument.write("SYSTem:LOCal")       # TODO: no quit remote, without command

    def smu2450_reset(self):
        """
        reset smu2450
        :return:none
        """
        self.instrument.write("*RST")


    def smu2450_init(self):
        """
        smu2450 remote mode initial
        :return: none
        """
        self.instrument.write("*RST")


    def sum2450_force_volt_sens_cur_init(self, pVout, pIlimt, pVrange, pIrange, pNplc):
        """
        configure in force volt sense current mode
        :param pVout: force volt output value
        :param pIlimt: force volt current limit value
        :param pVrange: force volt range
        :param pIrange: sense current range
        :param pNplc: set nplc value
        :return:none
        """
        ''' source configuration '''
        self.instrument.write("*RST")
        self.instrument.write(":SOUR:FUNC VOLT")  # set smu source as voltage
        self.instrument.write(":SOUR:VOLT:IMM " + "%s" % pVout)  # set source voltage output value
        self.instrument.write(":SOUR:VOLT:ILIMIT " + "%s" % pIlimt)  # set source voltage current limit
        if type(pVrange) != type("str"):
            self.instrument.write(":SOUR:VOLT:RANG " + "%s" % pVrange)  # set source voltage range
        else:
            self.instrument.write(":SOUR:VOLT:RANG:AUTO ON")  # set source voltage range as auto
        ''' sense configuration '''
        self.instrument.write(":SENS:FUNC 'CURR'")  # set smu sense as current
        if type(pIrange) != type("str"):
            self.instrument.write(":SENS:CURR:RANG " + "%s" % pIrange)  # set sense current range
        else:
            self.instrument.write(":SENS:CURR:RANG:AUTO ON")  # set sense current range as auto
        self.instrument.write(":SENS:CURR:NPLC " + "%s" % pNplc)  # set sense NPLC


    def smu2450_set_volt_output(self, pVoltValue):
        """
        set force volt output value and turn on output
        :param pVoltValue: volt output value
        :return: none
        """
        self.instrument.write(":*WAI")  # wait until previous overlapped commands are finished
        self.instrument.write(":SOUR:VOLT " + "%s" % pVoltValue) # set output value
        self.instrument.write(":OUTP ON")   # turn on output


    def smu2450_read_sense_curr(self, pCnt, pBufElement):
        """
        measure sense current
        if you want to make multiple read, you can use uncomment code
        :param pCnt: read number
        :param pBufElement: read element
        :return: none
        """
        self.instrument.write(":*WAI")  # wait until previous overlapped commands are finished
        self.instrument.write(":SENS:COUN %d" % pCnt)   # set read number
                                                        # if single read pCnt should be equal 1
        ''' make single read '''
        return self.instrument.query(":READ? 'defbuffer1', %s" % pBufElement)   # read data (single read)
        ''' make multiple read, use below code '''
        # self.instrument.write(":TRAC:MAKE 'currMeasBuf', 100")    # create multiple read buffer
        # return self.instrument.query(":TRAC:DATA? 1, %d, 'currMeasBuf'" % pCnt)   # read data (multiple read)


    def smu2450_outp_Off(self):
        """
        turn off output
        :return:
        """
        self.instrument.write(":*WAI")  # wait until previous overlapped commands are finished
        self.instrument.write(":OUTP OFF")  # turn off output


    def smu2450_4w_meas_res_test(self):
        """
        using 4-wire measure low resistor test
        :return: none
        """
        self.instrument.write("*RST")
        self.instrument.write("TRIG:LOAD 'SimpleLoop', 1")
        self.instrument.write("SENS:FUNC 'RES'")
        self.instrument.write("SENS:RES:RANG:AUTO ON")
        self.instrument.write("SENS:RES:OCOM ON")
        self.instrument.write("SENS:RES:RSEN ON")
        self.instrument.write("DISP:SCR SWIPE_GRAPh")
        self.instrument.write("OUTP ON")
        self.instrument.write("INIT")
        self.instrument.write("*WAI")
        self.instrument.write("OUTP OFF")
        print(self.instrument.query("TRAC:DATA? 1, 1, 'defbuffer1', READ, REL"))





    def sum2450_force_cur_sens_volt_init(self, pIout, pVlimt, pIrange, pVrange, pNplc):
        """
        configure in force current sense volt mode
        :param pIout: force current output value
        :param pVlimt: force current's volt limit value
        :param pIrange: force current range
        :param pVrange: sense volt range
        :param pNplc: set nplc value
        :return:none
        """
        ''' source configuration '''
        self.instrument.write("*RST")
        self.instrument.write(":SOUR:FUNC CURR")                    # set smu source as current
        self.instrument.write(":SOUR:CURR:LEV " + "%s" % pIout)         # set source current output value
        self.instrument.write(":SOUR:CURR:VLIM " + "%s" % pVlimt)       # set source current's voltage limit
        if type(pIrange) != type("str"):
            self.instrument.write(":SOUR:CURR:RANG " + "%s" % pIrange)  # set source current range
        else:
            self.instrument.write(":SOUR:CURR:RANG:AUTO ON")            # set source current range as auto
        ''' sense configuration '''
        self.instrument.write(":SENS:FUNC 'VOLT'")                  # set smu sense as volt
        if type(pVrange) != type("str"):
            self.instrument.write(":SENS:VOLT:RANG " + "%s" % pVrange)  # set sense volt range
        else:
            self.instrument.write(":SENS:VOLT:RANG:AUTO ON")            # set sense volt range as auto
        self.instrument.write(":SENS:CURR:NPLC " + "%s" % pNplc)    # set sense NPLC

####################
    def smu_2450_meas_v(self,on):
        """
        after using func: sum2450_force_cur_sens_volt_init
        """
        self.instrument.write('SENS:FUNC:ON "VOLT"')
        if on == 0 :
            self.instrument.write(":SENSe:VOLTage:RSENse OFF") # 感测开关
        if on == 1 :
            self.instrument.write(":SENSe:VOLTage:RSENse ON")  # 感测开关
        self.instrument.write(":OUTP ON")
        meas_v = self.instrument.query('MEAS:VOLT?')
        return float(meas_v)

    def smu_2450_meas_i(self,on):
        """
        after using func: sum2450_force_volt_sens_cur_init
        """
        self.instrument.write('SENS:FUNC:ON "CURR"')
        if on == 0:
            self.instrument.write(":SENSe:CURRent:RSENse OFF") # 感测开关
        if on == 1:
            self.instrument.write(":SENSe:CURRent:RSENse ON")  # 感测开关
        self.instrument.write(":OUTP ON")
        meas_i = self.instrument.query('MEAS:CURR?')
        return float(meas_i)



    def smu_on(self):
        self.instrument.write(":OUTP ON")

    def smu_off(self):
        self.instrument.write(":OUTP OFF")

    '''源指令'''
    def smu_sour_ii(self, pCurr, pIrange):
        self.instrument.write("SOUR:FUNC:MODE CURR")  # 设置源模式为电流
        self.instrument.write(f"SOUR:CURR:LEV {pCurr}")  # 设置源电流值
        self.instrument.write("SOUR:CURR:VLIM 3.3")  #设置电压限制6V, 可选
        self.instrument.write(":SOUR:CURR:RANG " + "%s" % pIrange)  # set source current range

    def smu_sour_i(self, pCurr):
        self.instrument.write("SOUR:FUNC:MODE CURR")  # 设置源模式为电流
        self.instrument.write(f"SOUR:CURR:LEV {pCurr}")  # 设置源电流值
        self.instrument.write("SOUR:CURR:VLIM 8.0")  #设置电压限制8V, 可选


    def smu_sour_v(self, pVolt):
        self.instrument.write("SOUR:FUNC:MODE VOLT")  # 设置源模式为电压
        self.instrument.write(f'SOUR:VOLT:LEV {pVolt}')  # 设置源电压值
        # self.instrument.write("SOUR:VOLT:ILIM 1.0")  #设置电流限制1A, 可选

    '''测量指令'''
    def smu_meas_i(self):
        self.instrument.write(":SENSe:CURRent:RSENse ON")
        self.instrument.write('SENS:FUNC:ON "CURR"')  #打开电流测量功能
        self.instrument.write("SENS:CURR:RANG:AUTO ON")  # 设置电流自动量程功能
        self.instrument.write(":OUTP ON")
        meas_curr = self.instrument.query('MEAS:CURR?')  # mod = round(float(meas_curr), 4)
        return float(meas_curr)

    def smu_meas_v(self):
        self.instrument.write(":SENSe:VOLTage:RSENse ON")
        self.instrument.write('SENS:FUNC:ON "VOLT"')  # 打开电压测量功能
        self.instrument.write("SENS:VOLT:RANG:AUTO ON")  # 设置电压自动量程功能
        self.instrument.write(":OUTP ON")
        meas_volt = self.instrument.query('MEAS:VOLT?')
        return float(meas_volt)
        # return meas_volt

    # 测量指令
    # self.instrument.write("SENS:FUNC:CONC ON")  # 设置并发测量功能
    def smu_meas_v_diff(self, pGap, pAcq):
        self.instrument.write('SENS:FUNC:ON "VOLT"')
        self.instrument.write("SENS:VOLT:RANG:AUTO ON")
        while 1:
            voltage_is1 = float(self.instrument.query('MEAS:VOLT?'))
            time.sleep(pGap)
            voltage_is2 = float(self.instrument.query('MEAS:VOLT?'))
            if abs(voltage_is1-voltage_is2) < pAcq:
                break
        print("Voltage is: ", voltage_is1)
        return voltage_is1

    def smu_meas_v_avr(self, pCount):
        self.instrument.write('SENS:FUNC:ON "VOLT"')
        self.instrument.write("SENS:VOLT:RANG:AUTO ON")
        time.sleep(1)
        avers = []
        while (pCount):
            time.sleep(0.001)
            aver = float(self.instrument.query('MEAS:VOLT?'))
            avers.append(aver)
            pCount -= 1
        return sum(avers) / len(avers)

    def smu_meas_i_avr(self, pCount):
        self.instrument.write('SENS:FUNC:ON "CURR"')  # 打开电流测量功能
        self.instrument.write("SENS:CURR:RANG:AUTO ON")  # 设置电流自动量程功能
        time.sleep(1)
        avers = []
        while (pCount):
            time.sleep(0.001)
            aver = float(self.instrument.query('MEAS:CURR?'))
            avers.append(aver)
            pCount -= 1
        return sum(avers) / len(avers)


if __name__ == "__main__":
    device = SmuKeithley(pyvisa.ResourceManager(),smu_2450_id)
    # print(device.smu_meas_v()) #measure

    # device.smu2450_reset() # reset the smu
    # device.smu_on()

    # print(device.smu_meas_i())  # measure

