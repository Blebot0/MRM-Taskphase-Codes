import cv2
import numpy as np
import socket

while True:
    a = np.ones((640, 480))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.43.55", 2000))
    a = s.recv(1024)
    a = a.decode()

    print(a)
    if (cv2.waitkey(1) & 0xFF == ord("q")) :
        break
s.close()