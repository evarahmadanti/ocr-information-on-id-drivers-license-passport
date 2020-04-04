import json
import flask

class sim_new_json(object):
	def __init__(self, file_path):
		self.file_path = file_path
		self.jenis_sim = ""
		self.no_sim = ""
		self.nama = ""
		self.tempat_tgl_lahir = ""
		self.gol_darah_jenis_kelamin = ""
		self.alamat = ""
		self.pekerjaan = ""
		self.provinsi = ""

	def toJson(self):
		data = {
			"jenis_sim" : self.jenis_sim,
			"no_sim" : self.no_sim,
			"nama" : self.nama,
			"tempat_tgl_lahir" : self.tempat_tgl_lahir,
			"gol_darah_jenis_kelamin" : self.gol_darah_jenis_kelamin,
			"alamat" : self.alamat,
			"pekerjaan" : self.pekerjaan,
			"provinsi" : self.provinsi
        }
		
		# Write data object to json file
		name = self.file_path + '.json'
		with open(name, "w") as f:
			json.dump(data, f)
		return data