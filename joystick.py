import pygame
import serial

pygame.init()
print("Joystics: ", pygame.joystick.get_count())
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
clock = pygame.time.Clock()


def send(var):
    ser = serial.Serial('/dev/ttyUSB0')
    var = str(var)
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


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            x = my_joystick.get_axis(0)
            y = my_joystick.get_axis(1)
            x = -1 * map(x, -1, 1, -1023, 1023)
            y = map(y, -1, 1, -1023, 1023)
            clock.tick(1000)

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

            left= constrain(left, -255, 255)
            right = constrain(right, -255, 255)
            print(right, " ", left)

            if right>-10 and right<10:
                if right<0:
                    right= abs(right)
                    right = str(right)
                    right = "00" + right + "0"
                elif right>0:
                    right = str(right)
                    right = "00" + right + "1"
                send(right)
                right = int(right)

            if left>-10 and left<10:
                if left<0:
                    left= abs(left)
                    left = str(left)
                    left = "00" + left + "0"
                elif left>0:
                    left = str(left)
                    left = "00" + left + "1"
                send(left)
                left = int(left)

            if right>-100 and right<100:
                if right<0:
                    right=abs(right)
                    right = str(right)
                    right = "0" + right + "0"
                elif right>0:
                    right = str(right)
                    right = "0" + right + "1"
                send(right)
                right = int(right)

            if left>-10 and left<10:
                if left<0:
                    left =abs(left)
                    left = str(left)
                    left = "0" + left + "0"
                elif left>0:
                    left = str(left)
                    left = "0" + left + "1"
                send(left)
                left = int(left)

pygame.quit()
