import pickle
import cv2
import socket

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket1.connect(('', 2020))
socket2.connect(('', 2002))

while True:
    data1 = []
    size1 = 0
    data2 = []
    size2 = 0
    frame_size = 640*480*3
    socket1.send(b'1')
    while size1<=frame_size and size2<=frame_size:
        packet1 = socket1.recv(65536)
        packet2 = socket2.recv(65536)

        if not packet1 or not packet2:
            break
        data1.append(packet1)
        data2.append(packet2)
        size1 += len(packet1)
        size2


