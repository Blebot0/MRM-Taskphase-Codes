import socket
import pickle
import cv2
import numpy as np

#Network Protocol : TCP
#Data packet = start bit | frame data | stop bit

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.43.58', 2025))
flag=0
while True:
    data = []
    while True:
        if flag==0:
            packet1 = s.recv(65536)
            flag=1
        if pickle.loads(packet1)=="start":
            packet= s.recv(65536)
            if not packet: break

            print(pickle.loads(packet))
            if pickle.loads(packet) == "stop":
                break
            else:
                data.append(packet)
    m, data_arr = pickle.loads(b"".join(data))
    data_arr = cv2.imdecode(data_arr, cv2.IMREAD_ANYCOLOR)
    print(data_arr)
    cv2.imshow('output', data_arr)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
s.close()


