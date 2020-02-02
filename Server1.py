import socket
import cv2
import numpy as np
import pickle
import time

cap = cv2.VideoCapture(-1)

cap.set(3, 200)
cap.set(4, 150)
s = socket.socket()
s.bind(('', 2020))
s.listen(4)
a, c = s.accept()
flag = 0

time.sleep(3)
while (True):
    ret, frame = cap.read()
    if ret == True:
        if flag==0:
            ja = pickle.dumps("start")
            a.sendall(ja)
            flag=1
        frame = cv2.imencode('.jpg', frame)
        frame = pickle.dumps(frame)
        a.sendall(frame)
        time.sleep(0.01)
        aja = pickle.dumps("stop")
        a.sendall(aja)
a.close()
cap.release()
cv2.destroyAllWindows()