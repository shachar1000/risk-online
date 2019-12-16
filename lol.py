import cv2
import numpy as np


#bgSubtractor = cv2.createBackgroundSubtractorMOG2()
#withoutBg = bgSubtractor.apply(grayFrame)
cap = cv2.VideoCapture(0)
_, firstFrame = cap.read()
firstFrameGray = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)
firstFrameBlurrred = cv2.GaussianBlur(firstFrameGray, (5, 5), 0)

def largestContour(contours):
    maxIndex = 0
    maxSize = 0
    for i in range(len(contours)):
        cnt = contours[i]
        size = cv2.contourArea(cnt)
        if size > maxSize:
            maxSize = size
            maxIndex = i
    return contours[maxIndex]


while (True):
    _, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurredFrame = cv2.GaussianBlur(grayFrame, (5, 5), 0)
    difference = cv2.absdiff(firstFrameBlurrred, blurredFrame)
    _, difference = cv2.threshold(difference, 50, 255, cv2.THRESH_BINARY)

    kernal = np.ones((4, 4), np.uint8)
    mask = cv2.morphologyEx(difference, cv2.MORPH_OPEN, kernal, iterations=2)
    mask = cv2.morphologyEx(difference, cv2.MORPH_CLOSE, kernal, iterations=2)
    final = cv2.bitwise_and(frame, frame, mask=mask)

    final_gray = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)

    contours, hierarchy = cv2.findContours(final_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        maxContour = largestContour(contours)
        cv2.drawContours(final, maxContour, -1, (0,255,0), 3)
    cv2.imshow("final", final)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
