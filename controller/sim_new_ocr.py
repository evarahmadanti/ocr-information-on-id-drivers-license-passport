import imutils
import cv2
import pytesseract
import json
from controller.normalize import Normalize
from model.sim_new_json import sim_new_json

class sim_new_engine(object):
    def __init__(self, orig, cnts, file_path):		
    	# Open image with opencv and optimizing
        self.cnts = cnts
        self.orig = imutils.resize(orig, height=400)
        self.data_result = sim_new_json(file_path)
        self.master_process()

    def text_detection(self):
    	for c in self.cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            gray = cv2.cvtColor(self.orig, cv2.COLOR_BGR2GRAY)
            th, gray = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
            crWidth = w / float(gray.shape[1])
            (origH, origW) = self.orig.shape[:2]
            if ar > 0.9 and crWidth > 0.4:
                # padding the bounding box
                pX = int((w - x) * 0.058)
                pY = int((h - y) * 0.03)
                (x, y) = (x - pX, y - pY)
                (w, h) = (w + (pX * 2), h + (pY * 2))
                # Extract the roi
                roi = self.orig[y:y + h, x:x + w].copy()
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
                threshed = cv2.adaptiveThreshold(threshed,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
                threshed = cv2.GaussianBlur(threshed,(3,3),0)
                result = pytesseract.image_to_string(threshed, lang="ind(1)+arialocr+Arial(1)")
                return result

    def extract(self,result):
        result = result.replace("\n\n","\n")
        result = result.replace("\n\n\n","\n")
        result = result.split("\n")
        
        jenis_sim = result[0]
        jenis_sim = jenis_sim.split(" ")
        jenis_sim = Normalize.letter_converter(jenis_sim[-1])
        self.data_result.jenis_sim = jenis_sim
        
        no_sim = Normalize.number_converter(result[1])
        self.data_result.no_sim = no_sim
        
        nama = Normalize.letter_converter(result[2])
        self.data_result.nama = nama
        
        tempat_tgl_lahir = result[3]
        tempat_tgl_lahir = tempat_tgl_lahir.split(" ")
        tempat_tgl_lahir = Normalize.letter_converter(tempat_tgl_lahir[-2]) + ", " + Normalize.number_converter(tempat_tgl_lahir[-1])
        self.data_result.tempat_tgl_lahir = tempat_tgl_lahir
        
        gol_darah_jenis_kelamin = Normalize.letter_converter(result[4])
        self.data_result.gol_darah_jenis_kelamin = gol_darah_jenis_kelamin
        
        alamat = result[5]+" "+result[6]+" "+result[7]
        self.data_result.alamat = alamat
        
        pekerjaan = Normalize.letter_converter(result[8])
        self.data_result.pekerjaan = pekerjaan
        
        provinsi = Normalize.letter_converter(result[9])
        provinsi = Normalize.sign_converter(provinsi)
        self.data_result.provinsi = provinsi

    def master_process(self):
        raw_result = self.text_detection()
        self.extract(raw_result)

    def to_json(self):
	    return self.data_result.toJson()