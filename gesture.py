import cv2
import numpy as np
import math
import time
cap = cv2.VideoCapture(0)
temp_finger=0
predif_arr = [5,4,3,1,2,3,3,4,5] 
fing_arr = [0,0,0]
while(cap.isOpened()):
    ret, img = cap.read()
    cv2.rectangle(img,(600,600),(100,100),(0,255,0),0)
    crop_img = img[100:300, 100:300]
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    cv2.imshow('greyscale', blurred)
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow('Thresholded', thresh1)
    img, contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
            cv2.CHAIN_APPROX_NONE)
    max_area = -1
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
    cnt=contours[ci]
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img,far,1,[0,0,255],-1)
        #dist = cv2.pointPolygonTest(cnt,far,True)
        cv2.line(crop_img,start,end,[0,255,0],2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)
    if count_defects == 1:
    	finger1 = 1
    	# print("It is 1")
    elif count_defects == 2:
        finger1 = 2
        # print("It is 2")
    elif count_defects == 3:
        finger1 = 3
        # print("It is 3")
    elif count_defects == 4:
        finger1 = 4
        # print("It is 4")
    else:
        finger1 = 5
        # print("It is 5")
    cv2.imshow('drawing', drawing)
    cv2.imshow('end', crop_img)
    
    if finger1!=temp_finger:
    	print(finger1)
    	temp_finger = finger1
    	fing_arr[0] = fing_arr[1]
    	fing_arr[1] = fing_arr[2]
    	fing_arr[2] = temp_finger
    	for x in xrange(0,3):
    		y=x*3
    		if fing_arr == predif_arr[y:y+3]:
    	 		if x == 0:
    	 			print("Send Water")
    	 			fing_arr = [0,0,0]
    	 		elif x == 1:
    	 			print("Send food")
    	 			fing_arr = [0,0,0]
    	 		else:
    	 			print("Send personell")
    	 			fing_arr = [0,0,0]	 	 
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)
    k = cv2.waitKey(10)
    if k == 27:
        break
