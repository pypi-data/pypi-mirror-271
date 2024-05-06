from smu_keithley_2450 import *
import hid
import instruments_name

"""使用SMU测试的例子"""
from instruments_name import *

smuid = smu_2460_id

smu = SmuKeithley2450(pyvisa.ResourceManager(), smuid)

# smu.smu2450_reset()

# smu.sum2450_force_volt_sens_cur_init(3.3,1,5,1,0.01)

# smu.smu2450_set_volt_output(5)

# smu.smu2450_read_sense_curr(1)

# print(smu.smu_2450_meas_v())

# print(smu.smu_meas_v())

"""以下是测试用例"""
"""强制电流测电压初始化并且改变提供电流并且测量电压"""
smu.sum2450_force_cur_sens_volt_init(-0.1, 5,2, 5, 0.1) # 初始化
#
# smu.smu_sour_ii(-0.6,1) # 提供电流 1是能提供的最大电流
# print(smu.smu_2450_meas_v(1)) # 测量电压 四线



"""只测量电压"""
""" 两线 且应该先将SMU设置为电压表模式 """
# print(smu.smu_2450_meas_v(0))

"""测量电流"""
""" 两线 且应该先将SMU设置为电压表模式 """
# print(smu.smu_2450_meas_i(0))
