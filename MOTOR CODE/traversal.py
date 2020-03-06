import Gps_garmin
import math
import AngleHead
import time
math.degrees()
time.sleep(3)

while 1:
    mag_angle = AngleHead.Mag_angle()
    lat1, lon1, dist = Gps_garmin.gps()
    Angle_diff = mag_angle - gps_angle

    lat2 = 13.347
    lon2 = 74.7921

    lon_change = math.radians(lon2 - lon1)
    lat_change = math.radians(lat2 - lat1)

    x = math.sin(lon_change) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(lon_change))

    bearing = math.degrees(math.atan2(x, y))
    gps_angle = (bearing + 360) / 360


    print(abs(Angle_diff))

    if Angle_diff > 0:
        if Angle_diff < 180:
            print("turn left")
        elif Angle_diff > 180:
            print("turn right")
    elif Angle_diff < 0:
        Angle_diff = abs(Angle_diff)
        if Angle_diff < 180:
            print("turn right")
        elif Angle_diff > 180:
            print("turn left")





