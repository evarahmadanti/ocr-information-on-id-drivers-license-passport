import PIL, hashlib, cv2, numpy, datetime, os
from flask import Flask, request
from flask_restful import Resource, Api
from controller.engine import *
from controller.ktp_ocr import ktp_engine
from elasticsearch import Elasticsearch

es = Elasticsearch(host="localhost", port=9200)
app = Flask(__name__)
api = Api(app)
index = "ocr"

class MainAPI(Resource):
    def create_index(self, index):
        es.indices.create(index=index, ignore=400)

    def get(self):
        return {'status': 200, 'message': 'Engine is working!', 'data': None}

    def post(self):
        # Get current time
        current_time = datetime.datetime.now()
        current_time = current_time.strftime('%d%m%y%H%M%S')
        md5_current_time = hashlib.md5(current_time.encode()).hexdigest()

        # Create a directory path
        path = os.path.join(os.getcwd(), 'static', current_time, "")
        file_path = path + md5_current_time
        os.mkdir(path)
        
        # Get image from API request and save
        try:
            if ('ktp' in request.files):
                filename = file_path + '_ktp.jpg'
                image = PIL.Image.open(request.files['ktp']).save(filename)
                # Processing image to engine
                data = engine(filename, file_path, 400)
                data = data.ktp_proc(file_path)

            elif ('sim' in request.files):
                filename = file_path + '_sim.jpg'
                image = PIL.Image.open(request.files['sim']).save(filename)
                # Processing image to engine
                data = engine(filename, file_path, 400)
                data = data.sim_proc(file_path)

            elif ('paspor' in request.files):
                filename = file_path + '_paspor.jpg'
                image = PIL.Image.open(request.files['paspor']).save(filename)
                # Processing image to engine
                data = engine(filename, file_path, 400)
                data = data.paspor_proc(file_path)

            elif ('sim_new' in request.files):
                filename = file_path + '_sim.jpg'
                image = PIL.Image.open(request.files['sim_new']).save(filename)
                # Processing image to engine
                data = engine(filename, file_path, 400)
                data = data.sim_new_proc(file_path)
            
            # Insert data to elasticsearch
            self.create_index(index)
            res = es.index(index=index, doc_type="doc", id=md5_current_time, body=data)
            return {'status': 200, 'message': 'Success', 'data': data}

        except Exception as e:
            return {'status': 500, 'message': str(e), 'data': None}

api.add_resource(MainAPI, '/')

if __name__ == "__main__" :
    app.run(host='0.0.0.0', debug=True)



