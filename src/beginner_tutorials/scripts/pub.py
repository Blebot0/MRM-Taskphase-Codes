#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64
import serial

gps = serial.Serial("/dev/ttyUSB0",4800)


def talker():
    pub = rospy.Publisher('pubsub', Float64, queue_size=10)
    rospy.init_node('pub', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        while 1:
            line = gps.readline()
            line = line.decode('utf-8')
            line = line.split(",")
            if line[0] == "$GPRMC":
                lat = line[3]
                lon = line[5]
                lat = float(lat)
                lon = float(lon)
                lat = lat / 100
                lon = lon / 100

                pub.publish(lat)
                rate.sleep()



if __name__ == '__main__':
    try:   
        talker()
    except:
        break

