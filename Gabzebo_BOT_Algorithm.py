#!/usr/bin/env python

'''
Code for a 4-wheeled bot with skid steer drive having IMU, GPS, Kinect and ultrasonic sensor plugins.
IMU and GPS are used for finding the inclination for positioning of the bot.
uS sensor is used for setting a threshold distance for navigating around the objects,
threshold distance = 1.5 gazebo units
'''
import rospy
from sensor_msgs.msg import Imu, NavSatFix, Range
from tf.transformations import euler_from_quaternion
import math
import time
from pyproj import Geod
from geometry_msgs.msg import Twist
yaw =0 
gps_angle=0
lat1=0
lon1=0
thresh_dist = 0
lat2 = 49.8999542451
lon2 = 8.90011251418




def callback(pose):
    global yaw
    quaternion = (pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)

    euler = euler_from_quaternion(quaternion)
    yaw= math.degrees(euler[2]) +180
    yaw = abs(yaw-360)
    yaw = yaw%360


def callback2(data):
    global lat1 
    lat1= data.latitude
    global lon1 
    lon1= data.longitude

def callback3(rang):
    global thresh_dist
    thresh_dist = rang.range
    


def listener():
    rospy.init_node('bot_yaw','bot_gps', anonymous=True,disable_signals= True) 
    rospy.Subscriber("imu", Imu, callback)
    rospy.Subscriber("fix", NavSatFix, callback2) 
    rospy.Subscriber("/sensor/sonar_front", Range, callback3)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rate = rospy.Rate(10) # 10hz
    twist = Twist()  
    
    while 1:
        
	geodesic =Geod(ellps='WGS84')
	bearing, reverse_bearing, dist = geodesic.inv(lon1,lat1,lon2,lat2)
        bearing = bearing +180
	angle_diff = yaw- bearing
#        print("Yaw: ", yaw, "Bearing: ", bearing)
        print("Angle: ", angle_diff)       
        if angle_diff>1:
            if angle_diff<180:
                twist.angular.z=0.7
            elif angle_diff>180:
                twist.angular.z=-0.7
            pub.publish(twist)

        elif angle_diff<-1:
            angle_diff = abs(angle_diff)
            if angle_diff<180:
                twist.angular.z = -0.7
            elif angle_diff>180:
                twist.angular.z = 0.7
            pub.publish(twist)
        
        if angle_diff<1 and angle_diff>-1:
            break

    while 1:
        geodesic =Geod(ellps='WGS84')
        bearing, reverse_bearing, dist = geodesic.inv(lon1,lat1,lon2,lat2)
        bearing = bearing +180
        angle_diff = yaw- bearing
        flag=0
        if thresh_dist < 1.5:
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x=0
            twist.angular.y=0
            twist.angular.z=1
            twist.linear.x= 0
            pub.publish(twist)
            print("Threshold distance: ", thresh_dist)
            flag=220

        if flag == 220 and thresh_dist>1.5 :
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x=0
            twist.angular.y=0
            twist.angular.z=0.0
            twist.linear.x = -1
            pub.publish(twist)
            time.sleep(1)
            while 1:
                geodesic =Geod(ellps='WGS84')
                bearing, reverse_bearing, dist = geodesic.inv(lon1,lat1,lon2,lat2)
                bearing = bearing +180
                angle_diff = yaw- bearing
                if angle_diff>1:
                    if angle_diff<180:
                        twist.linear.y = 0
                        twist.linear.z = 0
                        twist.angular.x=0
                        twist.angular.y=0
                        twist.linear.x = 0
                        twist.angular.z=0.7
                    elif angle_diff>180:
                        twist.linear.y = 0
                        twist.linear.z = 0
                        twist.angular.x=0
                        twist.angular.y=0
                        twist.linear.x = 0

                        twist.angular.z=-0.7
                    pub.publish(twist)

                elif angle_diff<-1:
                    angle_diff = abs(angle_diff)
                    if angle_diff<180:
                        twist.linear.y = 0
                        twist.linear.z = 0
                        twist.angular.x=0
                        twist.angular.y=0
                        twist.linear.x = 0

                        twist.angular.z = -0.7
                    elif angle_diff>180:
                        twist.linear.y = 0
                        twist.linear.z = 0
                        twist.angular.x=0
                        twist.angular.y=0
                        twist.linear.x = 0

                        twist.angular.z = 0.7
                    pub.publish(twist)

                if angle_diff<1 and angle_diff>-1:
                    flag=1
                    break

        if  dist>2 and thresh_dist>1.5:
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x=0
            twist.angular.y=0
            twist.angular.z=0
            twist.linear.x= -0.8
            print("Distance: ", dist)
            pub.publish(twist)
            flag=0
        
        elif dist<2:
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x=0
            twist.angular.y=0
            twist.angular.z=0
            twist.linear.x = 0
            pub.publish(twist)
            break

        
    rospy.spin()

if __name__ == '__main__':
    listener()



