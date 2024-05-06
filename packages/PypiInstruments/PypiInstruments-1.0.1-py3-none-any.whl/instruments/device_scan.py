import pyvisa
from instruments_name import *
# 创建VISA资源管理器

rm = pyvisa.ResourceManager()

# 获取所有连接的设备列表
instruments = rm.list_resources()

# 打印出所有设备
print("Connected VISA devices:")
for instrument in instruments:
    print(instrument)