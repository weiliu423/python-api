# Install the following packages:

# pip install google-cloud-storage
# pip install firebase
# pip install firebase_admin
# pip install pandas

print("Load file system from firebase server...")
import os

import urllib3

filePath = 'C:\\Users\\Wei\\OneDrive\\UCC\\Project\\'

def osnr_parse_file(data):
    
    each_lines = ""
    exclude = '\\\n'
    if not data:
        http = urllib3.PoolManager()
        r = http.request('GET', 'https://firebasestorage.googleapis.com/v0/b/mininet-optical-file-system.appspot.com/o/OSNR.txt?alt=media&token=01bb2232-e8da-4291-b43a-4c7df4b9a2c4')
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




    

