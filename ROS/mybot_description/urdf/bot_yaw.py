#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu, NavSatFix
from tf.transformations import euler_from_quaternion
import math

yaw =0 
gps_angle=0

def callback(pose):
    global yaw
    quaternion = (pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)

    euler = euler_from_quaternion(quaternion)
    yaw= math.degrees(euler[2]) +180
   # print("yaw: ", yaw)
    
def callback2(data):
    global gps_angle
    lat1 = data.latitude
    lon1 = data.longitude

    lat2 = 13.347
    lon2 = 74.7921

    lon_change = math.radians(lon2 - lon1)
    lat_change = math.radians(lat2 - lat1)

    x = math.sin(lon_change) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(lon_change))

    bearing = math.degrees(math.atan2(x, y))
    gps_angle = (bearing + 360) / 360
   # print("gps angle", gps_angle)
    print("Angle Difference: ",yaw-gps_angle)


def listener():
    rospy.init_node('bot_yaw','bot_gps', anonymous=True) 
    rospy.Subscriber("imu", Imu, callback)
    rospy.Subscriber("fix", NavSatFix, callback2)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except:    
        pass
