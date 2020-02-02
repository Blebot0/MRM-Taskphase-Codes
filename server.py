import socket
import cv2
import numpy as np
import pickle
import base64
cap = cv2.VideoCapture(0)

cap.set(3, 400)
cap.set(4, 300)
s = socket.socket()
s.bind(('', 2000))
s.listen(4)
client, c = s.accept()
flag = 0
if cap.isOpened()== True:
    print("Y")
while(True):
    ret, frame = cap.read()
    if ret== True:

        frame = cv2.imencode('.jpeg', frame)
        frame = pickle.dumps(frame)
        a.sendall(frame)
        aja = pickle.dumps("stop")
        a.sendall(aja)

a.close()
cap.release()
cv2.destroyAllWindows()