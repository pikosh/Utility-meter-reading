import numpy as np
import cv2
import sys
from PIL import Image
import imutils
import os.path

def measure_image2(input_file):
	#input_file="image1.jpg"
	img = cv2.imread(input_file)
	img = imutils.resize(img, height=500)
	#cv2.imshow("an",img)

	## Change to LAB space
	lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	l,a,b = cv2.split(lab)
	#imglab = np.hstack((l,a,b))

	## normalized the a channel to all dynamic range
	na = cv2.normalize(a, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

	## Threshold to binary
	_, threshed = cv2.threshold(na, thresh = 180,  maxval=255, type=cv2.THRESH_BINARY)

	## Do morphology
	kernel = cv2.getStructuringElement( cv2.MORPH_ELLIPSE , (3,3))
	opened = cv2.morphologyEx(threshed, cv2.MORPH_OPEN,kernel)
	res = np.hstack((threshed, opened))

	## Find contourss
	_, contours, _ = cv2.findContours(opened, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

	## Draw Contours
	res = img.copy()
	#cv2.drawContours(res, contours, -1, (255,0,0), 10)
	#cv2.imwrite("region_contours.png", res)
	## Filter Contours
	angle =0
	for _, contour in enumerate(contours):
		bbox = cv2.boundingRect(contour)
		area = bbox[-1] * bbox[-2]
		print(area)
		if area < 2150:
			continue
		(x, y, w1, h) = cv2.boundingRect(contour)
		cy = y
		cx = x
		w = w1
		return(cx, cy, w, h, angle)
		#res = cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
		res = cv2.putText(res, "Red contour bound", (x+w, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 1, lineType=cv2.LINE_AA) 
		cv2.imwrite("img15_2.png", res)
		#cropped = img[x0:x1, y0:y1]
	

if __name__ == "__main__":
	measure_image2('/home/perizat/Рабочий стол/thesis/rectangles/rectangle3/img15_1.png')


"""
		(x, y, w1, h) = cv2.boundingRect(contour)
		cy = (y + h)*0.9
		w = ((x + w1)/2)*1.3
		cx = w"""
