import numpy as np
import cv2
import imutils
from collections import deque

cap = cv2.VideoCapture(0)
pts = deque(maxlen=10)

while(True):


    ret, frame = cap.read()

    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    lower_white = np.array([0,0,0], dtype=np.uint8)
    upper_white = np.array([0,0,255], dtype=np.uint8)
    
    
    

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    greenLower = (0, 160, 160)
    greenUpper = (10, 255, 255)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    	c = max(cnts, key=cv2.contourArea)
    	((x, y), radius) = cv2.minEnclosingCircle(c)
    	M = cv2.moments(c)
    	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    	# only proceed if the radius meets a minimum size
    	if radius > 10:
    		# draw the circle and centroid on the frame,
    		# then update the list of tracked points
    		cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
    		cv2.circle(frame, center, 5, (0, 0, 255), -1)
    # update the points queue
    pts.appendleft(center)
    if center != None:
    	print(center)
    # loop over the set of tracked points
    for i in range(1, len(pts)):
    	# if either of the tracked points are None, ignore
    	# them
    	if pts[i - 1] is None or pts[i] is None:
    		continue
    	# otherwise, compute the thickness of the line and
    	# draw the connecting lines
    	thickness = int(np.sqrt(10 / float(i + 1)) * 2.5)
    	cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
    	break




cap.release()
cv2.destroyAllWindows()

# X, Y, RADIUS
# Where X gets higher --> right, and Y gets higher V