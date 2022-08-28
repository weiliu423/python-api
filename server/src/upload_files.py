# Install the following packages:

# pip install google-cloud-storage
# pip install firebase
# pip install firebase_admin

import json
import os
import urllib3
from firebase_admin import credentials, initialize_app, storage

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\'

def init():
    # exclude = '\\r\\n'
    # http = urllib3.PoolManager()
    # r = http.request('GET', 'https://firebasestorage.googleapis.com/v0/b/mininet-optical-file-system.appspot.com/o/cred.json?alt=media&token=f97ebb5f-f8e2-44f3-ba34-0792a8f5986d')
    # # Init firebase with your credentials
    # filter_line = ''.join(ch for ch in str(r.data).replace("b'", "") if ch not in exclude)  
    # print(filter_line)
    cred = credentials.Certificate(os.path.join(__location__, 'cred.json'))
    initialize_app(cred, {'storageBucket': 'mininet-optical-file-system.appspot.com'})

def upload_nodes_file():
    fileName = "nodes.txt"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(__location__ + fileName)
    blob.make_public()
    print(__location__, blob.public_url)

def upload_link_file():
    fileName = "links.txt"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(__location__ + fileName)
    blob.make_public()
    print(__location__, blob.public_url)

def upload_osnr_file(data):
    try:
        fileName = "OSNR.txt"
        bucket = storage.bucket()
        blob = bucket.blob(fileName)

        if(data != ""):
            with open(__location__ + fileName, 'w') as osnr:
                osnr.write(str(data).replace("b'", ""))
            
        blob.upload_from_filename(__location__ + fileName)

        blob.make_public()
        print(__location__+ fileName, blob.public_url)
        return True
    except:
        return False

def upload_osnr_data_file(data):
    try:
        fileName = "OSNR_data.txt"
        bucket = storage.bucket()
        blob = bucket.blob(fileName)

        if(data != ""):
            with open(__location__ + fileName, 'w') as osnr_data:
                osnr_data.write(str(data))
          
        blob.upload_from_filename(__location__ + fileName)

        blob.make_public()
        print(__location__ + fileName, blob.public_url)
        return True
    except:
        return False

if __name__ == '__main__':
    init()