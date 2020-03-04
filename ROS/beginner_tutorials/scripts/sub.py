#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64

def callback(dat):
    print(dat)

def listener():

    rospy.init_node('sub', anonymous=True)

    rospy.Subscriber("pubsub", Float64, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
