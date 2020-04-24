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
            
'''
This algorithm works after the alignment of the bot. It works in a while loop that I have omitted for now as I'll be making some changes to the codes soon. 
var: thresh_dist was extracted from the range sensor using sensor message callback. 
var: twist is an object to Twist message for control of the bot
flag has been created to avoid repetition.
'''
