import numpy as np
import cv2

#1 cm = 37.795276px
PIXEL_IN_CENTIMETER = 37.795275591
VIDEO_WIDTH =1280
VIDEO_HEIGHT = 720

def get_thresholded(hsv):
    # red = cv2.inRange(hsv,np.array((30,150,50)),np.array((255,255,180)))
    yellow = cv2.inRange(hsv,np.array((20,100,100)),np.array((30,255,255)))
    # blue = cv2.inRange(hsv,np.array((100,100,100)),np.array((120,255,255)))
    # both = cv2.add(red,yellow,blue)
    return yellow

def get_size(w,h):
	size = ''

	rect_width = w/PIXEL_IN_CENTIMETER
	rect_height = h/PIXEL_IN_CENTIMETER
	rect_area = (rect_width*rect_height)

	if rect_area > 50:
		size = 'L'
	elif rect_area > 20 and rect_area < 30:
		size = 'M'
	else:
		size = 'S'
	return size

def find_contours(image):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	threshed = get_thresholded(hsv)
	ret,thresh = cv2.threshold(threshed,127,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	areas = [cv2.contourArea(c) for c in contours]
	max_index = np.argmax(areas)
	return contours[max_index]

def calculate(cnt,image):
	x,y,w,h = cv2.boundingRect(cnt)
	(x,y),radius = cv2.minEnclosingCircle(cnt)
	center = (int(x),int(y))
	radius = int(radius)
	cv2.circle(image,center,radius,(0,255,0),2)

	size = get_size(w,h)
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(image, 'size: '+size, (40, 80), font, 2.0, (0, 255, 0), 2)

def track(image):
	cnt = find_contours(image)
	calculate(cnt,image)
	cv2.imshow("Show",image)

if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    capture.set(3,VIDEO_WIDTH)
    capture.set(4,VIDEO_HEIGHT)

    while True:
        okay, image = capture.read()
        if okay:
            track(image)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
           print 'Capture failed'
           break

