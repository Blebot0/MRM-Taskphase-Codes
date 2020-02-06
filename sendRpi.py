import serial
import time


ser = serial.Serial('/dev/ttyS0')
ser.flushInput()

while True:
    try:
        time.sleep(0.01)
        ser_bytes = ser.read(9)
        decode = ser.decode(10)
        decode = str(decode)
        if decode[0] == 'b' and decode[5] == "c":
            right = decode[1:5]
            right_dir = decode[4]
            left = decode[6:10]
            left_dir=decode[9]
            print(right, '\t', right_dir, '\t', left, '\t', left_dir)
    except:
        print("Keyboard Interrupt")
        break