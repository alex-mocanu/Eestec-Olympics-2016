# import the necessary packages
import numpy as np
import cv2
import time

# lower and upper bounds for red and blue
redLower = (28, 100, 100)
redUpper = (40, 255, 255)
BlueLower = (102, 190, 200)
BlueUpper = (105, 255, 255)

# decide if to click
click = 0
center = (0, 0)

SERVER_STATE_UPDATE_FREQUENCY_SECONDS = 0.01

camera = cv2.VideoCapture(0)

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Find red figure
    maskRed = cv2.inRange(hsv, redLower, redUpper)
    maskRed = cv2.erode(maskRed, None, iterations=2)
    maskRed = cv2.dilate(maskRed, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(maskRed.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    #center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        click = 1
    else:
        click = 0

    # Find Blue figure
    maskBlue = cv2.inRange(hsv, BlueLower, BlueUpper)
    maskBlue = cv2.erode(maskBlue, None, iterations=2)
    maskBlue = cv2.dilate(maskBlue, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(maskBlue.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

    print center[0],
    print center[1],
    print click
    time.sleep(SERVER_STATE_UPDATE_FREQUENCY_SECONDS)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()