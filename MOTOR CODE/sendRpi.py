import time
import serial
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(18, GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(12,GPIO.OUT)

p1 = GPIO.PWM(18,500)
p2 = GPIO.PWM(19,500)
p3 = GPIO.PWM(13,500)
p4 = GPIO.PWM(12,500)

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

ser = serial.Serial('/dev/ttyS0')
ser.flushInput()



while True:
    try:
        # time.sleep(0.01)
        ser_bytes = ser.read(10)
        decode = str(ser_bytes.decode('utf-8'))
        try:
            if decode[0] == 'b':
                right = int(decode[1:4])
                right_dir = int(decode[4])
                left = int(decode[6:9])
                left_dir = int(decode[9])
                right = right*100/255
                left = left*100/255

                print(right, '\t', right_dir, '\t', left, '\t', left_dir)

                if right_dir == 0 :
                    p2.ChangeDutyCycle(right)
                elif right_dir == 1:
                    p2.ChangeDutyCycle(right)

                if left_dir == 0:
                    p1.ChangeDutyCycle(left)
                elif left_dir == 1:
                    p3.ChangeDutyCycle(left)


        except:
            pass
    except:
        break