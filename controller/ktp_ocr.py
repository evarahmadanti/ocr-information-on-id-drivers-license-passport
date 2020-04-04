import imutils
import cv2
import pytesseract
import json
import re
import numpy as np
from controller.normalize import Normalize
from model.ktp_json import ktp_json

class ktp_engine(object):
	def __init__(self, orig, cnts, file_path):		
		self.cnts = cnts
		self.orig = orig
		self.gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
		self.ar_list = []
		self.crWidth_list = []
		self.data_result = ktp_json(file_path)
		result = self.cropping()
		self.extract(result)
	
	def cropping(self):
		for c in self.cnts:
			(x, y, w, h) = cv2.boundingRect(c)
			ar = w / float(h)
			crWidth = w / float(self.gray.shape[1])
			(origH, origW) = self.orig.shape[:2]
			if ar > 1.2 and crWidth > 0.5:
				# padding the bounding box
				pX = int((w - x) * 0.04)
				pY = int((h - y) * 0.09)
				x = max((0, x - pX)*2)
				y = max((0, y - pY)*2)
				w = min(origW, w + (pX * 4))
				h = min(origH, h + (pY * 2))

				# extract the ROI
				roi = self.orig[y:y + h, x:x + w - 2].copy()
				roi = imutils.resize(roi, height=600)
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
						cv2.rectangle(roi, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
						flag = "info"
						raw_info = self.text_detection(roi_info, flag, 600)
						continue
					
					if ar_roi == self.ar_list[1] and crWidth_roi == self.crWidth_list[1] :
						# padding the bounding box
						px1 = int((x1 + w1) * 0.05)
						py1 = int((y1 + h1) * 0.2)
						(x1, y1) = (x1 - px1, y1 - py1)
						(w1, h1) = (w1 + (px1 * 2), h1 + (py1 * 2))
						# ex1tract the ROI
						roi_prov = roi[y1:y1 + h1, x1:x1 + w1].copy()
						cv2.rectangle(roi, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
						flag = "prov"
						raw_prov = self.text_detection(roi_prov, flag, 100)
						continue
					
					if ar_roi == self.ar_list[2] and crWidth_roi == self.crWidth_list[2] :
						# padding the bounding box
						pX1 = int((x1 + w1) * 0.10)
						pY1 = int((y1 + h1) * 0.13)
						(x1, y1) = (x1 - pX1, y1 - pY1)
						(w1, h1) = (w1 + (pX1 * 2), h1 + (pY1 * 2))
						# extract the ROI
						roi_nik = roi[y1:y1 + h1, x1:x1 + w1].copy()
						cv2.rectangle(roi, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), -1)
						flag = "nik"
						raw_nik = self.text_detection(roi_nik, flag, 100)
						continue

		raw_result = raw_nik + raw_prov + raw_info
		return raw_result

	def text_detection(self, roi, flag, size):
		img = imutils.resize(roi, height=size)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
		threshed = cv2.GaussianBlur(gray,(3,3),0)
		th, threshed = cv2.threshold(threshed, 100, 255, cv2.THRESH_TRUNC)
		threshed = cv2.GaussianBlur(threshed,(3,3),0)
		threshed = cv2.adaptiveThreshold(threshed,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
		if flag == "nik":
			result = pytesseract.image_to_string((threshed), lang="nik")
		else :
			result = pytesseract.image_to_string((threshed), lang="Arial(1)+ind")
		result = result.replace("\n\n", "\n").replace(":", "").replace(";", "").replace(".", "").replace("  ", " ").split("\n")
		print(result)
		return result

	def list_to_string(self, s):
		string = " "
		return (string.join(s))
	
	def extract(self, result):
		self.data_result.nik = Normalize.number_converter(result[0])
		self.data_result.kota = Normalize.letter_converter(result[2])
		for word in result:
			if re.match("PROVINSI", word) is not None:
				provinsi = Normalize.letter_converter(word)
				provinsi = provinsi.split(' ')
				provinsi.pop(0)
				self.data_result.provinsi = self.list_to_string(provinsi)
				continue

			if re.match("Nama|Name", word) is not None:
				nama = word.split(' ')	
				nama.pop(0)
				if "Tempat" not in result[4]:
					nama = Normalize.letter_converter(self.list_to_string(nama) + " " + result[4])
				self.data_result.nama = nama
				continue

			if re.match("Tompat|Tempat|Lahir|/Tgl|Tgi|tempat|lahir|Lahlr", word) is not None:
				tempat = word.split(' ')
				del tempat[:2]
				self.data_result.tempat = self.list_to_string(tempat)
				continue

			if re.match("Kelamin|kelamin|Jenis|jenis|Jems|jems|keiamin|keiamln", word) is not None :
				jenis_kelamin = word.split(' ')
				del jenis_kelamin[:2]
				self.data_result.jenis_kelamin = Normalize.letter_converter(jenis_kelamin[0])
				self.data_result.golongan_darah = Normalize.letter_converter(jenis_kelamin[-1])
				continue

			if re.match("Alamat", word) is not None :
				alamat = word.split(" ")
				alamat.pop(0)
				alamat = self.list_to_string(alamat)
				if re.match("Tempat", result[4]) is None and re.match("RT|Rw|RW", result[8]) is None:
					alamat = alamat + " " + result[8]
				else :
					if re.match("Alamat", result[6]) is not None and re.match("RT|Rw|RW", result[7]) is not None:
						alamat = alamat + " " + result[7]
					else :
						alamat = alamat
				self.data_result.alamat = alamat
				continue

			if re.match("RT|Rw|RW", word) is not None:
				rt = word.split(" ")
				rt.pop(0)
				self.data_result.rt = self.list_to_string(rt)
				continue

			if re.match("Kel|Ket|Desa|desa|kei|/Desa", word) is not None:
				desa = word.split(' ')
				desa.pop(0)
				self.data_result.desa = self.list_to_string(desa)
				continue

			if re.match("Kecamatan", word) is not None:
				kecamatan = Normalize.letter_converter(word)
				kecamatan = kecamatan.split(' ')
				kecamatan.pop(0)
				self.data_result.kecamatan = self.list_to_string(kecamatan)
				continue

			if re.match("Agama", word) is not None:
				agama = Normalize.letter_converter(word)
				agama = agama.split(" ")
				agama.pop(0)
				self.data_result.agama = self.list_to_string(agama)
				continue

			if re.match("Status", word) is not None:
				status = Normalize.letter_converter(word)
				status = status.split(" ")
				del status[:2]
				self.data_result.status = self.list_to_string(status)
				continue

			if re.match("Pekerja", word) is not None:
				pekerjaan = Normalize.letter_converter(word)
				pekerjaan = pekerjaan.split(" ")
				pekerjaan.pop(0)
				self.data_result.pekerjaan = self.list_to_string(pekerjaan)
				continue

			if re.match("Kewarganegaraan", word) is not None:
				kewarganegaraan  = Normalize.letter_converter(word)
				kewarganegaraan = kewarganegaraan.split(" ")
				kewarganegaraan.pop(0)
				self.data_result.kewarganegaraan = self.list_to_string(kewarganegaraan)
				continue

			if re.match("Berlaku|Hingga", word) is not None:
				berlaku = word.split(" ")
				del berlaku[:2]
				self.data_result.berlaku = self.list_to_string(berlaku)
				continue

	def to_json(self):
		return self.data_result.toJson()