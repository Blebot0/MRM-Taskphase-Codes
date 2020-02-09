import smbus

bus = smbus.SMBus(1)

dev_add = 0x15
dev_regmod = 0x00
dev_regout = 0x1d

bus.read_i2c_block_data(dev_add, )
