# Install the following packages:

# pip install google-cloud-storage
# pip install firebase
# pip install firebase_admin
# pip install pandas

print("Load file system from firebase server...")
import os
import urllib.request  # the lib that handles the url stuff
import pandas as pd
import numpy as np
import re
import base64
import urllib3

filePath = 'C:\\Users\\Wei\\OneDrive\\UCC\\Project\\'

def osnr_parse_file(data):
    
    each_lines = ""
    exclude = '\\\n'
    if not data:
        http = urllib3.PoolManager()
        r = http.request('GET', 'https://firebasestorage.googleapis.com/v0/b/mininet-optical-file-system.appspot.com/o/OSNR_data.txt?alt=media&token=ca0cf500-b765-4457-ad05-fdc8abafc1f3')
        each_line = str(r.data).replace("b'", "")
        # f = open(filePath + "OSNR_data.txt", "r")
        # # data_bytes = f.read().encode("utf-8")
        # # x = base64.b64encode(data_bytes)
        # each_line = f.read().split('<')
    else:
        each_line = str(data).replace("b'", "")
    
    filter_line = ''.join(ch for ch in each_line if ch not in exclude)  
    each_lines = filter_line.split('<')
    #print(each_line)
    device_header = ['device_name', 'link_component', 'mode', 'channel', 'OSNR(dB)', 'gOSNR(dB)']
    device_info = []
    #========================= Parse File ==========================================
    for line in each_lines:
        device_data = []
        if('name' in line):
            components = list(filter(None, line.strip().replace(' ', '').split(',')))
            components = [name.split(':')[1].replace('>','') for name in components]
        if('ch' in line):
            info = line.split('>')
            channel = info[0].replace('>', '')
            info = list(filter(None,info[1].replace('\n','').replace('dBrn', 'dB').replace('dBn', 'dB').split('dB')))
            data_value = 0
            for each_component in components:
                device_data.append(each_component)
            device_data.append(channel)
            for data in info:
                if 'OSNR' in data:
                    data_value = data.split(':')[1].replace(' ', '')
                elif 'gOSNR' in data:
                    data_value = data.split(':')[1].replace(' ', '')
                device_data.append(data_value)
        if device_data:
            device_info.append(device_data)
    #========================= Data Mapping ===========================================       
    for each_device in device_info:
        for index ,deviceinfo in enumerate(each_device):
            each_device[index] = device_header[index] + ":" + deviceinfo
    return device_info

def update_data():
    CredfilePath = filePath + 'cred.json'
    if os.stat(CredfilePath).st_size == 0:
        with open(CredfilePath, 'w') as writefile:
            for line in urllib.request.urlopen("https://raw.githubusercontent.com/weiliu423/Mininet_optical_visualisation/b7e613b3541c8f4fd9d34e5a1c11382319a62113/mininet-optical-file-system-3c125a1f0763.json?token=GHSAT0AAAAAABV3KZ36Z5JUA4WBSU7WXAWQYWEYVVA"):
                print(line.decode('utf-8'))
                writefile.write(line.decode('utf-8'))
    else:
        from firebase_admin import credentials, initialize_app, storage
        # Init firebase with your credentials
        cred = credentials.Certificate(CredfilePath)
        initialize_app(cred, {'storageBucket': 'mininet-optical-file-system.appspot.com'})

        # source_blob_name = "OSNR_data.txt"
        # bucket_name = "mininet-optical-file-system.appspot.com"
        # #The path to which the file should be downloaded
        # destination_file_name = filePath + source_blob_name

        # bucket = storage.bucket()
        # blob = bucket.blob(source_blob_name)
        # blob.download_to_filename(destination_file_name)

def KNN(df):  
    df['OSNR(dB)'] = pd.to_numeric(df['OSNR(dB)'])
    df['gOSNR(dB)'] = pd.to_numeric(df['gOSNR(dB)'])
    df = df.fillna(0)
    print(df)

    # Import train_test_split function
    from sklearn.model_selection import train_test_split 
    from sklearn.neighbors import KNeighborsClassifier   
    # Split dataset into training set and test set
    # X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.3) # 70% training and 30% test

    # #Create KNN Classifier
    # knn = KNeighborsClassifier(n_neighbors=5)

    # #Train the model using the training sets
    # knn.fit(X_train, y_train)

    # #Predict the response for test dataset
    # y_pred = knn.predict(X_test)

    #Import scikit-learn metrics module for accuracy calculation
    from sklearn import metrics
    # Model Accuracy, how often is the classifier correct?
    
    # f1 = open(filePath + "osnr_processed.txt", "w")
    # f1.write("Now the file has more content!")
    # print(f.read())
    # f1.close()    
    #print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


    

