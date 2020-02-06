import socket
import pickle
import cv2
import numpy as np
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.43.58', 2025))

while True:
    data = []
    print("a")
    while True:
        packet= s.recv(10000000)
        if not packet:
            break
        data.append(packet)
        try:
            if pickle.loads(packet)=="stop":
                break
        except:
            pass
    try:
        print("c")
        m,data_arr = pickle.loads(b"".join(data))
        data_arr = cv2.imdecode(data_arr, cv2.IMREAD_ANYCOLOR)
        data_arr=cv2.resize(data_arr,(640,480))
        cv2.imshow('output', data_arr)
    except:
        pass
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
s.close()


