#!/usr/bin/env python

import sys
import rospy
from beginner_tutorials.srv import *

def gps_client():
    rospy.wait_for_service('send')
    try:
        s = rospy.ServiceProxy('send', send)
        a = s()
        print(a.lat, a.lon)
    except rospy.ServiceException, e:
        print("Service call failed: %s"%e)

if __name__ == "__main__":
    gps_client()
