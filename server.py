import socket
import cv2
import numpy as np
import pickle
import zlib
import base64
cap = cv2.VideoCapture(0)
cap.set(3,200)
cap.set(4,150)
s=socket.socket()
s.bind(('', 2000))
s.listen(4)
a,c = s.accept()
while(True):
    z , frame = cap.read()
    ja = pickle.dumps("start")
    a.sendall(ja)
    if(z==True):
        frame = pickle.dumps(frame)
        compressor = zlib.compressobj(-1, zlib.DEFLATED, -9)
        frame = compressor.compress(frame) + compressor.flush()
        a.sendall(frame)
        lol = pickle.dumps("stop")
        a.sendall(lol)
a.close()
cap.release()
cv2.destroyAllWindows()