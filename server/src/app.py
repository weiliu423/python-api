from file_manager import osnr_parse_file, monitor_data_parse, sigtrace_data_parse
from upload_files import upload_osnr_file, upload_osnr_data_file, init
from knn_model import KNN
from flask import Flask, request, render_template, make_response
from flask_restful import Resource, Api, reqparse
import json
import base64
import os
import time
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class OSNR(Resource):
    def get(self):   
        try:
            data = json.dumps(osnr_parse_file(""))
            if(data != '[]'):       
                return {'data': json.loads(data)}, 200  # return data and 200 OK code
            else:
                return {'data': 'No data found'}, 404
        except:
            return {'data': 'An exception occurred'}, 500 

    def post(self):
        try:
            data = request.get_json()
            if data["data"] != "":
                osnr_data = data["data"]
            else:
                osnr_data = base64.b64decode(data["base64"])
            init()
            osnr_updated = upload_osnr_file(osnr_data)
            parsed_data = osnr_parse_file(str(osnr_data))
            osnr_data_updated = upload_osnr_data_file(parsed_data)
            #============================================================================
            return {'success': True, 'osnr': osnr_updated, 'osnr_parsed_data': osnr_data_updated, 'data' : parsed_data }, 200  # return data with 200 OK
        except:
            return {'data': 'An exception occurred'}, 500 
    pass

class monitor(Resource):
    def get(self):   
        try:
            data = monitor_data_parse("")
            if(data != '[]'):       
                return {'data': json.loads(data)}, 200  # return data and 200 OK code
            else:
                return {'data': 'No data found'}, 404
        except:
            return {'data': 'An exception occurred'}, 500 

    def post(self):
        try:            
            data = request.get_json()
            if data["data"] != "":
                monitor_data = data["data"]
            else:
                monitor_data = base64.b64decode(data["base64"])
            init()

            #============================================================================
            return {'success': True, 'monitor_data': True, 'data' : "" }, 200  # return data with 200 OK
        except:
            return {'data': 'An exception occurred'}, 500 
    pass

class sigtrace(Resource):
    def get(self):   
        try:
            data = sigtrace_data_parse("")
            if(data != '[]'):       
                return {'data': json.loads(data)}, 200  # return data and 200 OK code
            else:
                return {'data': 'No data found'}, 404
        except:
            return {'data': 'An exception occurred'}, 500 

class knn(Resource):
    def get(self):   
        #try:
            data = sigtrace_data_parse("")
            knn_result = KNN(data)
            if(data != '[]'):       
                return {'data':knn_result}, 200  # return data and 200 OK code
            else:
                return {'data': 'No data found'}, 404
        # except:
        #     return {'data': 'An exception occurred'}, 500 

    pass

def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)

@app.route('/')
def index():
    context = { 'server_time': format_server_time() }
    return render_template('index.html', context=context)

api.add_resource(OSNR, '/osnr')  # '/osnr' is the entry point for osnr
api.add_resource(monitor, '/monitors')  # and '/monitors' is the entry point for monitors
api.add_resource(sigtrace, '/sigtrace')  # and '/sigtrace' is the entry point for sigtrace
api.add_resource(knn, '/knn')  # and '/knn' is the entry point for knn

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))