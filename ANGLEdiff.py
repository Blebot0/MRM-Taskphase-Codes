import serial
from haversine import haversine, Unit
import smbus
import math
import time


gps = serial.Serial("/dev/ttyUSB0",4800)

dev_add = 0x1E
reg_A = 0x00
reg_B = 0x01
mode_reg = 0x02

bus = smbus.SMBus(1)

bus.write_byte_data(dev_add, reg_A, 0x70)
bus.write_byte_data(dev_add, reg_B, 0xA0)
bus.write_byte_data(dev_add, mode_reg, 0x00)


while 1:
    declination = -0.00669
    pi = 3.14159265359
    time.sleep(0.6)
    mag_angle=0
    def read(addr):
        data = bus.read_i2c_block_data(dev_add, reg_B, 8)
        high = data[addr]
        low = data[addr + 1]

        # concatenate higher and lower value
        value = ((high << 8) | low)
        # to get signed value from module
        if (value > 32768):
            value = value - 65536
        return value
    try:
        x = read(2)
        y = read(4)
        z = read(6)
        # print(x,y,z)

        heading = math.atan2(y, x) + declination

        # Due to declination check for >360 degree
        if (heading > 2 * pi):
            heading = heading - 2 * pi

            # check for sign
        if (heading < 0):
            heading = heading + 2 * pi

            # convert into angle
        mag_angle = heading * 180.00000000 / pi
        #print("Heading Angle = %d°" % heading_angle)
    except:
        pass

    line = gps.readline()
    line = line.decode('utf-8')
    line = line.split(",")

    if line[0] == "$GPRMC":
        lat= line[3]
        lon= line[5]
        lat= float(lat)
        lon = float(lon)
        lat1 = lat/100
        lon1 = lon/100
        coord = (lat1, lon1)
        coord2=(13.34786166, 74.7921699)
        dist= haversine(coord, coord2)

    Angle_diff = mag_angle - gps_angle

    lat2 = 13.34786166
    lon2 = 74.79216999

    lon_change = math.radians(lon2 - lon1)
    lat_change = math.radians(lat2 - lat1)

    x = math.sin(lon_change) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(lon_change))

    bearing = math.degrees(math.atan2(x, y))
    gps_angle = (bearing + 360) / 360
    print("Distance: ",dist)
    print(abs("Angle: ",Angle_diff))

    if Angle_diff > 0:
        if Angle_diff < 180:
            print("turn left")
        elif Angle_diff > 180:
            print("turn right")
    elif Angle_diff < 0:
        if Angle_diff < 180:
            print("turn right")
        elif Angle_diff > 180:
            print("turn left")

