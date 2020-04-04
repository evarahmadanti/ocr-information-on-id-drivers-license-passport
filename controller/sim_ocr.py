import imutils
import cv2
import pytesseract
import json
import re
import numpy as np
from controller.normalize import Normalize
from model.sim_json import sim_json

class sim_engine(object):
    def __init__(self, orig, cnts, file_path):		
    	# Open image with opencv and optimizing
        self.cnts = cnts
        self.orig = imutils.resize(orig, height=400)
        self.ar_list = []
        self.crWidth_list = []
        self.data_result = sim_json(file_path)
        self.master_process()

    def text_detection(self):
    	for c in self.cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            gray = cv2.cvtColor(self.orig, cv2.COLOR_BGR2GRAY)
            th, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
            crWidth = w / float(gray.shape[1])
            (origH, origW) = self.orig.shape[:2]
            if ar > 1.1 and crWidth >= 0.4:
                # padding the bounding box
                pX = int((w - x) * 0.058)
                pY = int((h - y) * 0.03)
                (x, y) = (x - pX, y - pY)
                (w, h) = (w + (pX * 2), h + (pY * 2))

                roi = self.orig[y:y + h, x:x + w].copy()
                roi = imutils.resize(roi, height=800)
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
                sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
                gray_roi = cv2.GaussianBlur(gray_roi, (3, 3), 0)
                blackhat = cv2.morphologyEx(gray_roi, cv2.MORPH_BLACKHAT, rectKernel)
                gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
                gradX = np.absolute(gradX)
                (minVal, maxVal) = (np.min(gradX), np.max(gradX))
                gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
                gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
                thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
                thresh = cv2.erode(thresh, None, iterations=4)	
                cnts_roi = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts_roi = imutils.grab_contours(cnts_roi)
                cnts_roi = sorted(cnts_roi, key=cv2.contourArea, reverse=True)

                for c_roi in cnts_roi:
                    (x1, y1, w1, h1) = cv2.boundingRect(c_roi)
                    ar_roi = w1 / float(h1)
                    crWidth_roi = w1 / float(gray_roi.shape[1])
                    self.ar_list.append(ar_roi)
                    self.crWidth_list.append(crWidth_roi)
                    (origH1, origW1) = roi.shape[:2]
                    if ar_roi == self.ar_list[0] and crWidth_roi == self.crWidth_list[0] :
                        # padding the bounding box
                        pX1 = int((x1 + w1) * 0.03)
                        pY1 = int((y1 + h1) * 0.02)
                        (x1, y1) = (x1 - pX1, y1 - pY1)
                        (w1, h1) = (w1 + (pX1 * 2), h1 + (pY1 * 2))
                        # extract the ROI
                        roi_info = roi[y1:y1 + h1, x1:x1 + w1].copy()
                        cv2.rectangle(roi_info, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
                        img = imutils.resize(roi_info, height=600)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
                        th, threshed = cv2.threshold(gray, 100, 255, cv2.THRESH_TRUNC)
                        result = pytesseract.image_to_string((threshed), lang="Arial(1)+ind")
                        result = result.replace("\n\n", "\n").replace("\n\n\n","\n").replace(":", "").replace(";", "").replace(".", "").replace("  ", " ").split("\n")
                        print(result)
                        return result

    def list_to_string(self, s):
        string = " "
        return (string.join(s))                    

    def extract(self,result):
        for word in result:
            if re.match("Nama", word) is not None:
                nama = Normalize.letter_converter(word).split(' ')
                nama.pop(0)
                self.data_result.nama = self.list_to_string(nama)
                print(nama)
                continue

            if re.match("Alamat", word) is not None:
                alamat = word.split(" ")
                alamat.pop(0)
                self.data_result.alamat = self.list_to_string(alamat)
                print(alamat)
                continue

            if re.match("Tempat",word) is not None:
                tempat_lahir = word.split(" ")
                tempat_lahir.pop(0)
                self.data_result.tempat_lahir = self.list_to_string(tempat_lahir)
                print(tempat_lahir)
                continue

            if re.match("Tgl|Lah",word) is not None:
                tanggal_lahir = Normalize.number_converter(word).split(" ")
                del tanggal_lahir[:2]
                self.data_result.tanggal_lahir = self.list_to_string(tanggal_lahir)
                continue

            if re.match("Tinggi|Tlgg", word) is not None:
                tinggi = Normalize.number_converter(word).split(" ")
                tinggi.pop(0)
                self.data_result.tinggi = self.list_to_string(tinggi)
                print(tinggi)
                continue

            if re.match("Peke", word) is not None:
                kerja = Normalize.letter_converter(word).split(" ")
                kerja.pop(0)
                self.data_result.kerja = self.list_to_string(kerja)
                print(kerja)
                continue

            if re.match("No", word) is not None:
                no = Normalize.number_converter(word).split(" ")
                del no[:2]
                self.data_result.no = self.list_to_string(no)
                print(no)
                continue

            if re.match("s/d", word) is not None:
                berlaku = Normalize.number_converter(word).split(" ")
                berlaku.pop(0)
                self.data_result.berlaku = self.list_to_string(berlaku)
                print(berlaku)
                continue

            if re.match("Berlaku", word) is not None:
                berlaku = Normalize.number_converter(word).split(" ")
                berlaku.pop(0)
                self.data_result.berlaku = self.list_to_string(berlaku)
                print(berlaku)
                continue

    def master_process(self):
        raw_result = self.text_detection()
        self.extract(raw_result)

    def to_json(self):
	    return self.data_result.toJson()