import json
import flask

class paspor_json(object):
	def __init__(self, file_path):
		self.file_path = file_path
		self.mrz_type= ""
		self.number= ""
		self.country= ""
		self.nationality= ""
		self.name= ""
		self.surname= ""
		self.date_of_birth= ""
		self.gender= ""
		self.expiration_date= ""
		self.validscore= ""

	def toJson(self):
		data = {
            "mrz_type" : self.mrz_type,
            "passport_umber" : self.number,
            "country" : self.country,
            "nationality" : self.nationality,
            "names" : self.name,
            "surname" : self.surname,
            "birth Date" : self.date_of_birth,
            "gender" : self.gender,
            "expired_date" : self.expiration_date,
            "valid_score" : self.validscore
        }
        # Write data object to json file
		name = self.file_path + '.json'
		with open(name, "w") as f:
			json.dump(data, f)
		return data