import pygame
import serial
import time

pygame.init()
print("Joystics: ", pygame.joystick.get_count())
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
clock = pygame.time.Clock()


def send(var):
    ser = serial.Serial('/dev/ttyUSB0')
    var= str(var)
    var = var.encode()
    ser.write(var)


def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def constrain(var, min, max):
    if var > max:
        var = max
    elif var < min:
        var = min
    return var


def directionC(var):
    if var <= 0:
        var = abs(var)
        var = str(var)
        var = var + "0"
    else:
        var = str(var)
        var = var + "1"
    var = "b" + var
    return int(var)


def ZeroAddandSend(var, var2):
    var = "{0:0=4d}".format(var)
    var2 = "{0:0=4d}".format(var2)
    var = str(var)
    var2 = str(var2)
    var = var + var2
    time.sleep(0.05)
    send(var)
    print(var)


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            x = my_joystick.get_axis(0)
            y = my_joystick.get_axis(1)
            x = -1 * map(x, -1, 1, -1023, 1023)
            y = map(y, -1, 1, -1023, 1023)
            clock.tick(120)

            right = 0
            left = 0
            if y > 0:
                right = map(y, 0, 1023, 0, 255)
                left = map(y, 0, 1023, 0, 255)

            elif y < 0:
                right = map(y, 0, -1023, 0, -255)
                left = map(y, 0, -1023, 0, -255)

            else:
                right = 0
                left = 0
            if x < 0:
                X = map(x, 0, -1023, 0, 255)
                right = right + X
                left = left - X

            elif x > 0:
                X = map(x, 0, 1023, 0, 255)
                right = right - X
                left = left + X

            left = constrain(left, -255, 255)
            right = constrain(right, -255, 255)
            #            print(right, " ", left)

            right = directionC(right)
            left = directionC(left)

            ZeroAddandSend(right, left)

pygame.quit()