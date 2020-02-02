import cv2

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(-1)

cap.set(3,400)
cap.set(4,300)

while(cap.isOpened() or cap2.isOpened()):
    ret, frame = cap.read()
    ret1, frame1 = cap2.read()
    if ret == True:
        cv2.imshow("output", frame)
        if cv2.waitKey(1) & 0xFF == ord("w"):
            break
    if ret1 == True:
        cv2.imshow("output2", frame1)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
cap.release()
cap2.release()
cv2.destroyAllWindows()
