import pygame

pygame.init()
print("Joystics: ", pygame.joystick.get_count())
my_joystick = pygame.joystick.Joystick(0)
my_joystick.init()
clock = pygame.time.Clock()

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)
while True:
    for event in pygame.event.get():
        x = my_joystick.get_axis(0)
        y = my_joystick.get_axis(1)
        x = map(x, -1, 1, -512, 512)
        y = map(y, -1, 1, -512, 512)
        print(x, y)
        clock.tick(100)

pygame.quit ()