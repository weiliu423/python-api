from file_manager import osnr_parse_file
from upload_files import upload_osnr_file, upload_osnr_data_file, init
from flask import Flask, request, render_template, make_response
from flask_restful import Resource, Api, reqparse
import json
import base64
import os
import time

app = Flask(__name__)
api = Api(app)

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
        # try:
            
            #=============== Use Uri Parameter as input ===================
            #parser = reqparse.RequestParser()  # initialize
            
            # parser.add_argument('userId', required=True)  # add args
            # parser.add_argument('name', required=True)
            # parser.add_argument('city', required=True)
            
            #args = parser.parse_args()  # parse arguments to dictionary
            
            # create new dataframe containing new values
            
            # 'userId': args['userId'],
            # 'name': args['name'],
            # 'city': args['city'],
            # 'locations': [[]]
            #==================== Use Json request body =================================
            data = request.get_json()
            osnr_data = base64.b64decode(data["base64"])
            init()
            osnr_updated = upload_osnr_file(osnr_data)
            parsed_data = osnr_parse_file(str(osnr_data))
            osnr_data_updated = upload_osnr_data_file(parsed_data)
            #============================================================================
            return {'success': True, 'osnr': osnr_updated, 'osnr_parsed_data': osnr_data_updated, 'data' : parsed_data }, 200  # return data with 200 OK
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

api.add_resource(OSNR, '/osnr')  # '/users' is our entry point for Users
#api.add_resource(Locations, '/locations')  # and '/locations' is our entry point for Locations


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))