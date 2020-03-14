import threading
import cv2
import time

def cam1():
    cap1 = cv2.VideoCapture(2)
    while (cap1.isOpened()):
        ret,frame1= cap1.read()
        if ret== True:
            cv2.imshow("output",frame1)
            time.sleep(0.01)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def cam2():
    cap2 = cv2.VideoCapture(0)
    while (cap2.isOpened()):
        ret1,frame2= cap2.read()
        if ret1== True:
            cv2.imshow("output1",frame2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break




t1= threading.Thread(target=cam1)
t2= threading.Thread(target= cam2)

if __name__=="__main__":
    t1.start()
    t2.start()
    t1.join()
    t2.join()