# Install the following packages:

# pip install google-cloud-storage
# pip install firebase
# pip install firebase_admin
# pip install pandas

print("Load file system from firebase server...")
import json
import os
import re
import urllib3
import json
import pandas as pd
import numpy as np

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

def monitor_data_parse(data):
    # if not data:
    #     http = urllib3.PoolManager()
    #     r = http.request('GET', 'https://firebasestorage.googleapis.com/v0/b/mininet-optical-file-system.appspot.com/o/monitor_data.txt?alt=media&token=4ba6ebb1-dac9-4281-95d9-719be0e14804')
    #     each_line = str(r.data).replace("b'", "")
    # else:
    #     each_line = str(data).replace("b'", "")
    
    data = {
        't1_monitor' : '{"osnr": {"2": {"freq": 191400000000000.0, "osnr": 19.833875729158677, "gosnr": 19.536026801031607, "power": 5.448370706925527e-05, "ase": 5.660816490507191e-07, "nli": 4.0185406218953076e-08}, "4": {"freq": 191500000000000.0, "osnr": 23.49962598505213, "gosnr": 22.837040867182452, "power": 5.480486783898081e-05, "ase": 2.4482543582585587e-07, "nli": 4.035192667872748e-08}, "5": {"freq": 191550000000000.0, "osnr": 21.91041028617704, "gosnr": 21.440123833542444, "power": 5.4697476501408726e-05, "ase": 3.523110475739888e-07, "nli": 4.029312145496667e-08}}}',
        't4_monitor' : '{"osnr": {"1": {"freq": 191350000000000.0, "osnr": 23.503032876710353, "gosnr": 22.839964548947957, "power": 5.4804952823973305e-05, "ase": 2.446338333062684e-07, "nli": 4.035205358409929e-08}, "3": {"freq": 191450000000000.0, "osnr": 21.91268308410258, "gosnr": 21.442177591726622, "power": 5.469759030796161e-05, "ase": 3.5212745314952116e-07, "nli": 4.029191559349638e-08}}}',
        'r1_monitor' : '{"osnr": {"2": {"freq": 191400000000000.0, "osnr": 21.025966597725674, "gosnr": 20.638175092892087, "power": 1.978183837936924e-05, "ase": 1.561960293533683e-07, "nli": 1.4588740966180897e-08}, "4": {"freq": 191500000000000.0, "osnr": 27.01901416277575, "gosnr": 25.64993418202163, "power": 1.989844480690964e-05, "ase": 3.952917209564238e-08, "nli": 1.464917068351393e-08}, "5": {"freq": 191550000000000.0, "osnr": 24.028656065164945, "gosnr": 23.286922170038213, "power": 1.9859453368964834e-05, "ase": 7.854195078631227e-08, "nli": 1.4627829937649161e-08}}}',
        'r2_monitor' : '{"osnr": {"3": {"freq": 191450000000000.0, "osnr": 46.367244352156135, "gosnr": 31.19925937391308, "power": 1.993749643257113e-05, "ase": 4.601995476828715e-10, "nli": 1.4666517569984886e-08}}}',
        'r3_monitor' : '{"osnr": {"1": {"freq": 191350000000000.0, "osnr": 46.36951339338802, "gosnr": 31.199328387387713, "power": 1.9937496672764733e-05, "ase": 4.599591773831054e-10, "nli": 1.4666517746677268e-08}, "2": {"freq": 191400000000000.0, "osnr": 46.36837872458496, "gosnr": 31.19929388051331, "power": 1.9937496552667923e-05, "ase": 4.600793625337122e-10, "nli": 1.466651765833107e-08}, "3": {"freq": 191450000000000.0, "osnr": 27.020148264841495, "gosnr": 25.651120222457997, "power": 1.9898459560613348e-05, "ase": 3.9518880228954335e-08, "nli": 1.4644708846497886e-08}}}',
        'r4_monitor' : '{"osnr": {"1": {"freq": 191350000000000.0, "osnr": 27.022417357786182, "gosnr": 25.652415058059663, "power": 1.9898475663095376e-05, "ase": 3.9498269841391784e-08, "nli": 1.4649216752029018e-08}, "2": {"freq": 191400000000000.0, "osnr": 27.021282663126716, "gosnr": 25.651464791710726, "power": 1.989846384611795e-05, "ase": 3.950856756238637e-08, "nli": 1.4650736008459234e-08}, "3": {"freq": 191450000000000.0, "osnr": 24.030926289079375, "gosnr": 23.28885772312354, "power": 1.9859494689626665e-05, "ase": 7.850106795704342e-08, "nli": 1.46273921050871e-08}}}',
        'r5_monitor' : '{"osnr": {"2": {"freq": 191400000000000.0, "osnr": 24.032061139891034, "gosnr": 23.289743446875843, "power": 1.985951359219094e-05, "ase": 7.848063229592461e-08, "nli": 1.462892520192838e-08}, "5": {"freq": 191550000000000.0, "osnr": 46.36497649580224, "gosnr": 31.199190361535116, "power": 1.9937496192377533e-05, "ase": 4.6043991797684606e-10, "nli": 1.466651739329251e-08}}}',
        'r6_monitor' : '{"osnr": {"2": {"freq": 191400000000000.0, "osnr": 22.275368378068798, "gosnr": 21.765946989103387, "power": 1.9820638645597903e-05, "ase": 1.1737640560780164e-07, "nli": 1.460809848309516e-08}, "4": {"freq": 191500000000000.0, "osnr": 46.36611027594679, "gosnr": 31.199224867587017, "power": 1.993749631247434e-05, "ase": 4.603197328305829e-10, "nli": 1.4666517481638705e-08}, "5": {"freq": 191550000000000.0, "osnr": 27.017880356774793, "gosnr": 25.649386966174017, "power": 1.9898437998488385e-05, "ase": 3.953947973493686e-08, "nli": 1.4645671465473894e-08}}}'    
    }

    #filter_line = ''.join(ch for ch in each_line if ch not in exclude)  
    #each_lines = each_line.split('')
    #print(each_line)
    return json.dumps(data)

def sigtrace_data_parse(data):
    if not data:
        http = urllib3.PoolManager()
        r = http.request('GET', 'https://firebasestorage.googleapis.com/v0/b/mininet-optical-file-system.appspot.com/o/signal_trace.txt?alt=media&token=b24f5464-c09b-4c99-89e9-d22ac32fa790')
        each_line = str(r.data).replace('b"', "").replace(' ', '')
    else:
        each_line = str(data).replace("b'", "")

    sigtrace_header = ['Channel', 'direction','link','power','ase_noise','nli_noise']
    sig_data = []
    data = each_line.split('\\r\\n')
    device_data = []
    input_data = []
    output_data = []
    for each_data in data:
        if 'signal' in each_data:
            device_data.append(each_data.split('signal:')[1])
        if 'input' in each_data.lower():
            input_data.append(each_data)
        if 'output' in each_data.lower():
            output_data.append(each_data) 
        
        input_len = len(input_data)
        output_len = len(output_data)
        #print('device', device_data, 'input', input_len, 'output', output_len)
        if len(device_data) > 0 & (input_len > 0 or output_len > 0):
            if output_len > 0:    
                sig_data.append([device_data,output_data])
                device_data = []
                input_data = []
                output_data = []
            if input_len > 0:
                sig_data.append([device_data,input_data])
                device_data = []
                input_data = []
                output_data = []

    row_data = [sigtrace_header]
    parse_data = []
    output_data = []
    for sig in sig_data:
        #print('sig', sig)
        for data in sig:
            if '<ch' in str(data):
                if len(parse_data) > 0:
                    print(parse_data[0] , str(data))
                    if parse_data[0] == str(data):
                        parse_data = parse_data[:-5]
                    else:
                        parse_data = []
                parse_data.append(str(data)[2:-2].replace('<', '').replace('>', ''))
            else:
                direction_field = ""
                if 'input' in str(data).lower():
                    direction_field = "Input"
                    parse_data.append(direction_field)
                if 'output' in str(data).lower():
                    direction_field = "Output"
                    parse_data.append(direction_field)

                direction_data = str(data).lower().replace(direction_field.lower() + ':', '')
                each_signal = direction_data[3:-4].split('},')
                for signal in each_signal:
                    each_power = signal.split(':{')
                    for info in each_power:
                        if ('(' in info or '<' in info or (('r' in info or 't' in info) and len(info) == 2)):
                            parse_data.append(info)
                        else:
                            noise = info.split(',')
                            index = 0
                            for each_noise in noise:
                                index += 1
                                if 'power' in each_noise:
                                    dbm_value = 10 * np.log10(float(each_noise.split(":",1)[1])/1e-3)
                                    parse_data.append(dbm_value)
                                else:
                                    parse_data.append(each_noise.split(":",1)[1])
                                if len(parse_data) > 5:
                                    row_data.append(parse_data)
                                    parse_data = parse_data[:-4]
    df = pd.DataFrame(row_data)
    df = df[1:]
    df.columns = sigtrace_header
    #print(df)
    return df.to_json(orient='records')


#print(sigtrace_data_parse(""))