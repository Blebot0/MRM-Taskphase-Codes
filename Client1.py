import socket
import pickle
import cv2
import numpy as np

#Network Protocol : TCP
#Data packet = start bit | frame data | stop bit

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.43.58', 2020))
#s.connect(('localhost', 2020))

flag=0

while True:
    data = []
    print("a")
    while True:
        if flag == 0:
            packet1 = s.recv(10000000)
            flag=1
        if pickle.loads(packet1)=="start":
            packet= s.recv(65536)
            data.append(packet)
            if not packet: break
            try:
                if pickle.loads(packet) == "stop":
                    break
            except:
                pass

    try:
        m, data_arr = pickle.loads(b"".join(data))
        data_arr = cv2.imdecode(data_arr, cv2.IMREAD_ANYCOLOR)
        data_arr = cv2.resize(data_arr,(640,480))
        cv2.imshow('output', data_arr)
    except:
        pass
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()
s.close()


