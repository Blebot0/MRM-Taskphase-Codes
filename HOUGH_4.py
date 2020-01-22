import cv2 as cv
import numpy as np
cap = cv.VideoCapture(-1)
cap.set(3, 640)
cap.set(4, 480)
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # CHANGING BGR TO HSV
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HLS_FULL)
        # CREATING MASK RANGE
        mask = cv.inRange(hsv_frame, (36, 38, 52), (82, 255, 255))  # 31,136,59  126,255,255
        res = cv.bitwise_and(frame, frame, mask=mask)
        kernel = np.ones((3, 3), np.uint8)
        res = cv.dilate(res, kernel, iterations=1)
        res = cv.erode(res, kernel, iterations=1)
        res = cv.dilate(res, kernel, iterations=2)
        # CONTOUR
        gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 127, 255, 0)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        hough = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
        # output = res.copy()
        res = cv.medianBlur(res, 5)
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            asp_ratio= w/h

            if w > 45 and h > 45 and asp_ratio<1.2 and asp_ratio >0.8 and w<150 and h<150:
                x = x - 60
                y = y - 60
                w = w + 150
                h = h + 150
                X = x
                Y = y
                W = w
                H = h
                res = cv.rectangle(res, (x, y), (x + w, y + h), (255, 255, 0), 2)
                circles = cv.HoughCircles(hough, cv.HOUGH_GRADIENT, 1, 200, param1=35, param2=30, minRadius=20, maxRadius=150)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for (x, y, r) in circles[0, :]:
                        if x<X+H and y<W+Y and x>X and y>Y :
                            cv.putText(res, "BALL DETECTED", (500, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            cv.circle(res, (x, y), r, (0, 255, 0), 3)
                            cv.circle(res, (x, y), 2, (0, 0, 255), 3)
        # output= cv.bitwise_or(res,output,)
        cv.imshow("output", res)
        # cv.imshow('CIRCLE',output)
        # GETIING OUT WITH PRESSING Q
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
cv.destroyAllWindows()
