import socket
import pickle
import cv2
import numpy as np

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(('localhost', 2000))

while True:
    data = []
    while True:
        packet= s.recv(65536)

        if not packet:break
        try:
            print(pickle.loads(packet))
            if pickle.loads(packet)=="stop":
                break
            else:
                data.append(packet)
        except:
            pass
    m,data_arr = pickle.loads(b"".join(data))
    data_arr = cv2.imdecode(data_arr, cv2.IMREAD_ANYCOLOR)
    print(data_arr)
    cv2.imshow('output', data_arr)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cv2.destroyAllWindows()
s.close()


