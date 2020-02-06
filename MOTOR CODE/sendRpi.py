import time
import serial
ser = serial.Serial('/dev/ttyS0')
ser.flushInput()

while True:
    try:
        # time.sleep(0.01)
        ser_bytes = ser.read(10)
        decode = str(ser_bytes.decode('utf-8'))
        try:
            if decode[0] == 'b':
                right = decode[1:4]
                right_dir = decode[4]
                left = decode[6:9]
                left_dir = decode[9]
                print(right, '\t', right_dir, '\t', left, '\t', left_dir)
        except:
            pass
    except:
        break