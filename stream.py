#Importing libraries
import numpy as np
import cv2
import time

cap =cv2.VideoCapture(0)  #You can record and put the address of the video btw the parenthesis in " "
                          #0 here signifies the webcam no. if the laptop has only 1 webcam then write 0
                          #only to tell which webcam is to be used.

time.sleep(3)             #2 sec of time for the camera to adjust to the environment
background = 0            #To display the background when the cloak is on

#Capturing the background
for i in range(30):    #30 times chalega
  ret, background = cap.read()

while(cap.isOpened()):
  ret, img = cap.read()

  if not ret:
    break
  
  #Converting the BGR to HSV
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  lower_red = np.array([0, 120, 70])
  upper_red = np.array([10, 255, 255])
  mask1 = cv2.inRange(hsv, lower_red, upper_red)  #Seperating the cloak part

  lower_red = np.array([170, 120, 70])
  upper_red = np.array([180, 255, 255])
  mask2 = cv2.inRange(hsv, lower_red, upper_red)

  mask1 = mask1 + mask2  # + wroks as OR

  mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN,
                           np.ones((3,3), np.uint8), iterations = 2)  #Noise removal
  mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE,
                           np.ones((3,3), np.uint8), iterations = 1)
  
  mask2 = cv2.bitwise_not(mask1)

  res1 = cv2.bitwise_and(background, background, mask=mask1)  #Used for segmentation of the colour
  res2 = cv2.bitwise_and(img, img, mask=mask2)  #Used to substitute the cloak
  final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

  cv2.imshow('Done!!',final_output)
  k = cv2.waitKey(10)
  if k == 27:
    break

cap.release()
cv2.destroyAllWindows()