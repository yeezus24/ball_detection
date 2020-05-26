import numpy as np
from numpy import *
import cv2
import imutils
from collections import deque
import math
from matplotlib.pyplot import *
from matplotlib import pyplot as plt
import cmath
cap = cv2.VideoCapture(0)
pts = deque(maxlen=1000)

count = 0







def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
    y1 = 480 - y1
    y2 = 480 - y2
    y3 = 480 - y3
    denom = (x1-x2) * (x1-x3) * (x2-x3);
    A = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom;
    B = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom;
    C = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom;

    return A, B, C


while(True):


    ret, frame = cap.read()

    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    lower_white = np.array([0,0,0], dtype=np.uint8)
    upper_white = np.array([0,0,255], dtype=np.uint8)
    
    
    

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    greenLower = (0, 150, 150)
    greenUpper = (20, 255, 255)
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
        count += 1
        if count == 1:
            x1 = center[0]
            y1 = center[1]
        elif count == 2:
            if center[0] != x1:
                x2 = center[0]
                y2 = center[1]
            else:
                count -= 1
        elif count == 3:
            if center[0] != x2:
                x3 = center[0]
                y3 = center[1]
                a, b, c = calc_parabola_vertex(x1, y1, x2, y2, x3, y3)
                d = (b**2) - (4*a*c)

                # find two solutions
                sol1 = (-b-cmath.sqrt(d))/(2*a) 
                sol2 = (-b+cmath.sqrt(d))/(2*a) 
                x = np.linspace(0, 640, num=5000)
                y = (a * x**2) + (b*x) + c
                axes = plt.gca()
                axes.set_xlim([0,640])
                axes.set_ylim([0,480])
                plt.plot(x, y)
                #plt.show()
                print("(" + str(sol1) + ", 0)")
                print("(" + str(sol2) + ", 0)")
            else:
                count -= 1
            #x = calc_x(a, b, c)
            #print("(" + str(x) + ", 10)")
        #elif count == 5:
         #   plt.show()
        print(str(count) + " - " + str(center))
    # loop over the set of tracked points
    for i in range(1, len(pts)):
    	# if either of the tracked points are None, ignore
    	# them
    	if pts[i - 1] is None or pts[i] is None:
    		continue
    	# otherwise, compute the thickness of the line and
    	# draw the connecting lines
    	thickness = int(np.sqrt(1000 / float(i + 1)) * 2.5)
    	cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
    	break
    if key == ord("g"):
        plt.show()




cap.release()
cv2.destroyAllWindows()

# X, Y, RADIUS
# Where X gets higher --> right, and Y gets higher V




