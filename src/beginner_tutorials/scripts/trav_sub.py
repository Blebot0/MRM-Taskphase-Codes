#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    print("values ", data.val)


def listener():
    rospy.init_node('trav_sub', anonymous=True)
    rospy.Subscriber("traversal", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

