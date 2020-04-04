import json
import flask

class ktp_json(object):
    def __init__(self, file_path):
        self.provinsi = ""
        self.kota = ""
        self.nik = ""
        self.nama = ""
        self.tempat = ""
        self.jenis_kelamin = ""
        self.golongan_darah = ""
        self.alamat = ""
        self.rt = ""
        self.desa = ""
        self.kecamatan = ""
        self.agama = ""
        self.status = ""
        self.pekerjaan = ""
        self.kewarganegaraan = ""
        self.berlaku = ""
        self.file_path = file_path

    def toJson(self):
        data = {
            "provinsi" : self.provinsi,
            "kota" : self.kota,
            "nik" : self.nik,
            "nama" : self.nama, 
            "tempat" : self.tempat,
            "jenis_kelamin" : self.jenis_kelamin,
            "golongan_darah" : self.golongan_darah,
            "alamat" : self.alamat,
            "rt_rw" : self.rt,
            "kel_desa" : self.desa,
            "kecamatan" : self.kecamatan,
            "agama" : self.agama,
            "status_perkawinan" : self.status,
            "pekerjaan" : self.pekerjaan,
            "kewarganegaraan" : self.kewarganegaraan,
            "berlaku_hingga" : self.berlaku
        }

        # Write data object to json file
        name = self.file_path + '.json'
        with open(name, "w") as f:
            json.dump(data, f)
        return data


