from knn_model import osnr_parse_file
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json
import base64

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
        try:
            
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
            parsed_data = osnr_parse_file(str(osnr_data))
            #============================================================================
            return {'success': True, 'data_updated': True, 'data' : parsed_data }, 200  # return data with 200 OK
        except:
            return {'data': 'An exception occurred'}, 500 
    pass

    
api.add_resource(OSNR, '/osnr')  # '/users' is our entry point for Users
#api.add_resource(Locations, '/locations')  # and '/locations' is our entry point for Locations


if __name__ == '__main__':
    app.run()  # run our Flask app