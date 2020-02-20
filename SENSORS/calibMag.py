import smbus2
import math
import time

bus = smbus2.SMBus(1)

dev_add = 0x1E
reg_A = 0x00
reg_B = 0x01
mode_reg = 0x02

bus.write_byte_data(dev_add, reg_A, 0x70)
bus.write_byte_data(dev_add, reg_B, 0xA0)
bus.write_byte_data(dev_add, mode_reg, 0x00)

declination = -0.00669
pi =3.14159265359

time.sleep(0.6)

def read(addr):
    data=bus.read_i2c_block_data(dev_add, reg_B, 8)
    high = data[addr]
    low = data[addr+1]

        #concatenate higher and lower value
    value = ((high << 8) | low)

        #to get signed value from module
    if(value > 32768):
        value = value - 65536
    return value



