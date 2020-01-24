import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
cap.set(3, 400)
cap.set(4, 300)
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # CHANGING BGR TO HSV
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HLS_FULL)
        # CREATING MASK RANGE
        mask = cv.inRange(hsv_frame, (40, 37, 34), (86, 255, 255))  # 31,136,59  126,255,255
        res = cv.bitwise_and(frame, frame, mask=mask)
        kernel = np.ones((3, 3), np.uint8)
        res = cv.dilate(res, kernel, iterations=1)
        res = cv.erode(res, kernel, iterations=2)
        res = cv.dilate(res, kernel, iterations=3)
        # CONTOUR
        contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        hough = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
        # output = res.copy()
        res = cv.medianBlur(res, 5)
        print(hierarchy)
        for cnt in contours:
            x, y, w, h = cv.boundingRect(cnt)
            asp_ratio= w/h

            area = cv.contourArea(cnt)
            hull = cv.convexHull(cnt)
            hull_area = cv.contourArea(hull)
            if hull_area != 0:
                solidity = float(area) / hull_area
                #print(solidity)
            if w > 20 and h > 20 and asp_ratio<1.2 and asp_ratio >0.8 and w<100 and h<100 and solidity>0.9 :
                x = x - 30
                y = y - 30
                w = w + 80
                h = h + 80
                X = x
                Y = y
                W = w
                H = h
                res = cv.rectangle(res, (x, y), (x + w, y + h), (255, 255, 0), 2)
                circles = cv.HoughCircles(hough, cv.HOUGH_GRADIENT, 1, 200, param1=30, param2=32, minRadius=0, maxRadius=0)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for (x, y, r) in circles[0, :]:
                        if x<X+H and y<W+Y and x>X and y>Y and solidity >0.9:
                            cv.putText(res, "BALL DETECTED", (213,20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            cv.circle(res, (x, y), r, (0, 255, 0), 5)
                            cv.circle(res, (x, y), 2, (0, 0, 255), 5)

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
