# Install the following packages:

# pip install google-cloud-storage
# pip install firebase
# pip install firebase_admin

print("Uploading files to Google Cloud Storage...")
import os
import urllib.request  # the lib that handles the url stuff

filePath = 'C:\\Users\\Gaming PC\\OneDrive\\UCC\\Project\\upload-files-python\\'
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

    #####################################################
    # Put your local file path for nodes.txt
    fileName = "nodes.txt"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(filePath + fileName)
    blob.make_public()
    print(filePath, blob.public_url)

    #####################################################
    # Put your local file path for links.txt
    fileName = "links.txt"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(filePath + fileName)
    blob.make_public()
    print(filePath, blob.public_url)
    #####################################################