# Imports
import cv2
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# Initialize firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'storageBucket': "attendancefacerecognitio-fed56.appspot.com"})
print("Success")

# Initial image setup
ImageFolderPath = "Resources\Images"
ImagesPath = os.listdir(ImageFolderPath)
bucket = storage.bucket()
ImageList = []
Ids = []
for path in ImagesPath:
    # Append Employee List
    ImageList.append(cv2.imread(os.path.join(ImageFolderPath, path)))
    Ids.append(os.path.splitext(path)[0])
    # Upload Employee Image to Bucket
    fileName = os.path.join(ImageFolderPath, path)
    print(fileName)
    with open(fileName, "rb") as file:
        blob = bucket.blob(f"{os.path.splitext(path)[0]}.jpeg")
        blob.upload_from_file(file)

print(Ids)

def get_encoding(Images):
    encodingList = []
    for img in ImageList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(img)[0]
        encodingList.append(encoding)
    return encodingList

KnownImgsEncoding = get_encoding(ImageList)
EmployeeList = [KnownImgsEncoding, Ids]
print("Successfully get features from Images")

# Save encodings as a file
file = open("employees.p", "wb")
pickle.dump(EmployeeList, file)
file.close()
print("Successfully saved employees data and Ids")

# Upload face encodings if you want to get from cloud
firebase_storage_path = "face_encodings/employees.p"

# Upload the file to Firebase Storage
blob = bucket.blob(firebase_storage_path)
blob.upload_from_filename("employees.p")
print("Face encodings uploaded to Firebase Storage")