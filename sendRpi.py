import serial
import pickle
import time

def send(var):
    ser = serial.Serial('/dev/ttyUSB0')
    var= str(var)
    var= var.encode()
    ser.write(var)
