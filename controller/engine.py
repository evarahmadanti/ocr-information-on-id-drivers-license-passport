import numpy as np
import imutils
import cv2, datetime
import pytesseract
import json
import os
from controller.ktp_ocr import *
from controller.sim_ocr import *
from controller.sim_new_ocr import *
from controller.paspor_ocr import *

class engine(object):
	def __init__(self, filename, file_path, size):
		# Open image with opencv and optimizing
		img = cv2.imread(filename)
		img = imutils.resize(img, height=size)
		self.orig = img.copy()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		th, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
		# Detection processing
		self.face_detect(img, gray, file_path)
		self.text_detection(img, thresh)

	def face_detect(self, image, image_gray, file_path):
		face_cascade = cv2.CascadeClassifier(os.path.join(os.getcwd(), 'model/haarcascade_frontalface_default.xml'))
		faces = face_cascade.detectMultiScale(image_gray, 1.3, 5)

		if len(faces) == 1:
			for (x,y,w,h) in faces:
				if (x,y,w,h) in faces:
					roi_color = image[y-35:y+h+35, x-25:x+w+25]
					people = imutils.resize(roi_color, height=300)
					cv2.rectangle(image, (x-25, y-35), (x+w+25, y+h+105), (255, 255, 255), -1)
					cv2.imwrite("photos.jpg", image)

		elif len(faces) > 1 :
			for (x,y,w,h) in faces:
				fr = w/float(h)
				crfWidth = w / float(image_gray.shape[1])
				if fr >= 1.0 and crfWidth > 0.09:
					fpX = int((fx + fw) * 0.02)
					fpY = int((fy + fh) * 0.04)
					(fx, fy) = (fx - fpX, fy - fpY)
					(fw, fh) = (fw + (fpX * 2), fh + (fpY * 3))
					people = image[fy:fy+fh, fx:fx+fw]
					people = imutils.resize(roi_color, height=300)
					cv2.rectangle(image, (fx, fy-10), (fx+fw, fy+fh+50), (255, 255, 255), -1)
					cv2.imwrite("photos.jpg", image)

		else :
			people = image.copy()
		
		self.img = image.copy()
		name = file_path + '_face.jpg'
		cv2.imwrite(name, people)

	def text_detection(self, image, image_gray):
		rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
		sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
		gray = cv2.GaussianBlur(image_gray, (3, 3), 0)
		blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
		gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
		gradX = np.absolute(gradX)
		(minVal, maxVal) = (np.min(gradX), np.max(gradX))
		gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
		gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
		thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
		thresh = cv2.dilate(thresh,None,iterations=4)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		self.cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

	def ktp_proc(self, file_path):
		data = ktp_engine(self.img, self.cnts, file_path)
		return data.to_json()

	def sim_proc(self, file_path):
		data = sim_engine(self.img, self.cnts, file_path)
		return data.to_json()

	def sim_new_proc(self, file_path):
		data = sim_new_engine(self.img, self.cnts, file_path)
		return data.to_json()

	def paspor_proc(self, file_path):
		data = paspor_engine(self.img, self.cnts, file_path)
		return data.to_json()