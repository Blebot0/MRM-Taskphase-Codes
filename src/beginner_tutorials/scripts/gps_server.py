#!/usr/bin/env python

import rospy
from beginner_tutorials.srv import send,sendResponse,sendRequest
import serial
gps = serial.Serial("/dev/ttyUSB0",4800)

def send_coord(req):
    while True:
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
            return sendResponse(lat,lon)

def gps_server():
    rospy.init_node('gps_server')
    s= rospy.Service('send', send, send_coord)
    rospy.spin()

if __name__=="__main__":
    gps_server()
