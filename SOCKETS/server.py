import socket
import cv2
import numpy as np
import pickle
import time
cap = cv2.VideoCapture(0)

cap.set(3, 200)
cap.set(4, 150)
s = socket.socket()
s.bind(('', 2020))
s.listen(4)
a, c = s.accept()
flag = 0
if cap.isOpened()== True:
    print("Y")
time.sleep(3)
while(True):
    ret, frame = cap.read()
    if ret== True:
        time.sleep(0.01)
        frame = cv2.imencode('.jpeg', frame)
        frame = pickle.dumps(frame)
        a.sendall(frame)
        aja = pickle.dumps("stop")
        a.sendall(aja)

a.close()
cap.release()
cv2.destroyAllWindows()