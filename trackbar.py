<<<<<<< HEAD
import cv2 as cv
=======
mport
cv2 as cv
>>>>>>> origin/master
import numpy as np


def nothing(x):
    print(x)


cap = cv.VideoCapture(-1)

cv.namedWindow('Tracking')
cv.createTrackbar('LH', 'Tracking', 0, 255, nothing)
cv.createTrackbar('LS', 'Tracking', 0, 255, nothing)
cv.createTrackbar('LV', 'Tracking', 0, 255, nothing)
cv.createTrackbar('UH', 'Tracking', 255, 255, nothing)
cv.createTrackbar('US', 'Tracking', 255, 255, nothing)
cv.createTrackbar('UV', 'Tracking', 255, 255, nothing)

cap.set(3, 1280)
cap.set(4, 700)

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HLS_FULL)

        l_h = cv.getTrackbarPos('LH', 'Tracking')
        l_s = cv.getTrackbarPos('LS', 'Tracking')
        l_v = cv.getTrackbarPos('LV', 'Tracking')

        u_h = cv.getTrackbarPos('UH', 'Tracking')
        u_s = cv.getTrackbarPos('US', 'Tracking')
        u_v = cv.getTrackbarPos('UV', 'Tracking')

        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])

        mask = cv.inRange(hsv, l_b, u_b)

        res = cv.bitwise_and(frame, frame, mask=mask)
        cv.imshow('gray', mask)

        cv.imshow('Frame', res)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv.destroyAllWindows