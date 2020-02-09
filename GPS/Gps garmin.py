import serial
from haversine import haversine, Unit
gps = serial.Serial("/dev/ttyUSB0",4800)

while True:
    line = gps.readline()
    line = line.decode('utf-8')
    line = line.split(",")
    if line[0] == "$GPRMC":
        lat= line[3]
        lon= line[5]
        lat= float(lat)
        lon = float(lon)
        lat = lat/100
        lon = lon/100

        coord = (lat, lon)
        coord2=(13.34776166 , 74.79217166)
        print(haversine(coord, coord2))
        print("Latitude: ", lat,"N")
        print("Longitude: ", lon,"E")

