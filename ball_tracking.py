import numpy as np
import cv2

cap = cv2.VideoCapture(0)
count = 0

while(True):
    # Capture frame-by-frame
    count += 1
    if count % 1 == 0:
    	ret, frame = cap.read()
    
    	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    	gray = cv2.add(gray, np.array([-150.0]))

    	frame_blurred = cv2.blur(gray, (12,12))

    	# Display the resulting frame

    	detected_circles = cv2.HoughCircles(frame_blurred,  
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
               param2 = 30, minRadius = 1, maxRadius = 40) 

    	if detected_circles is not None:
    		detected_circles = np.uint16(np.around(detected_circles))
    		print(detected_circles)
    		for pt in detected_circles[0, :]: 
        		a, b, r = pt[0], pt[1], pt[2] 
  
        		# Draw the circumference of the circle. 
        		cv2.circle(frame, (a, b), r, (0, 255, 0), 2) 
  
        		# Draw a small circle (of radius 1) to show the center. 
        		cv2.circle(frame, (a, b), 1, (0, 0, 255), 3) 


    	cv2.imshow('frame', frame)
    	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break



# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# X, Y, RADIUS
# Where X gets higher --> right, and Y gets higher V