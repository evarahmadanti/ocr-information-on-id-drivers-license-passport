import imutils
import cv2
import pytesseract
import json
import passporteye
from passporteye import read_mrz
from controller.normalize import Normalize
from model.paspor_json import paspor_json

class paspor_engine(object):
    def __init__(self, orig, cnts, file_path):		
        self.cnts = cnts
        self.file_name = file_path + '_mrz.jpg'
        self.gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        self.data_result = paspor_json(file_path)
        self.master_process()

    def text_detection(self):
    	for c in self.cnts:
            (x,y,w,h) = cv2.boundingRect(c)
            ar = w / float(h)
            crWidth = w / float(self.gray.shape[1])
            
            if ar >= 5.0 and crWidth >= 0.75:
                pX = int((x + w)*0.03)
                pY = int((y + h)*0.03)
                (x,y) = (x - pX, y - pY)
                (w,h) = (w + (pX*2), h + (pY*2))
                roi = self.gray[y:y + h, x:x + w].copy()
                roi = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY)[1]
                roi = imutils.resize(roi, width=600)
                cv2.imwrite(self.file_name, roi)

    def read(self):
        self.data_result.mrz_type = self.mrz['mrz_type']
        self.data_result.number = self.mrz['number']
        self.data_result.country = self.mrz['country']
        self.data_result.nationality = self.mrz['nationality']
        self.data_result.name = self.mrz['names']
        self.data_result.surname = self.mrz['surname']
        self.data_result.date_of_birth = self.mrz['date_of_birth']
        self.data_result.gender = self.mrz['sex']
        self.data_result.expiration_date = self.mrz['expiration_date']
        self.data_result.validscore = self.mrz['valid_score']

    def master_process(self):
        self.text_detection()
        self.mrz = read_mrz(self.file_name)
        self.mrz = self.mrz.to_dict()
        self.read()

    def to_json(self):
	    return self.data_result.toJson()