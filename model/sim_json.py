import json
import flask

class sim_json(object):
        def __init__(self, file_path):
                self.file_path = ""
                self.nama= ""
                self.tempat_lahir= ""
                self.tanggal_lahir=""
                self.tinggi=""
                self.kerja= ""
                self.no= ""
                self.alamat= ""
                self.berlaku=""                

        def toJson(self):
                data = {
                        "nama" : self.nama,
                        "tempat_lahir" : self.tempat_lahir,
                        "tanggal_lahir" : self.tanggal_lahir,
                        "tinggi_badan" : self.tinggi,
                        "pekerjaan" : self.kerja,
                        "no_sim" : self.no,
                        "alamat" : self.alamat,
                        "masa_berlaku" : self.berlaku
                }
                
                # Write data object to json file
                name = self.file_path + '.json'
                with open(name, "w") as f:
                        json.dump(data, f)
                return data