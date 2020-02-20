import Gps_garmin
import math
import AngleHead

mag_angle = AngleHead.Mag_angle()
lat1, lon1 = Gps_garmin.gps()

lat2= int(input())
lon2= int(input())

lon_change = math.radians(lon2-lon1)
lat_change = math.radians(lat2-lat1)

x = math.sin(lon_change)*math.cos(lat2)
y = math.cos(lat1)*math.sin(lat2)- (math.sin(lat1)*math.cos(lat2)*math.cos(lon_change))

bearing = math.degrees(math.atan2(x,y))
gps_angle = (bearing+360) * 360

Angle_diff = abs(gps_angle-mag_angle)
while 1:
    if Angle_diff<180:
        print("move left")
        print("check ")
