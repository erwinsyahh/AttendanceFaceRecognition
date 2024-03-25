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
bucket = storage.bucket()
ImageList = []
Ids = []
# Iterate over each folder (representing IDs) in the ImageFolderPath
for id_folder in os.listdir(ImageFolderPath):
    id_folder_path = os.path.join(ImageFolderPath, id_folder)
    if os.path.isdir(id_folder_path):
        for image_filename in os.listdir(id_folder_path):
            image_path = os.path.join(id_folder_path, image_filename)
            image = cv2.imread(image_path)
            if image is not None:
                ImageList.append(image)
                Ids.append(id_folder)
            else:
                print("Error: Unable to read image at path", image_path)
        # Upload Employee Image to Bucket
        fileName = os.path.join(id_folder_path, image_filename)
        print(fileName)
        with open(fileName, "rb") as file:
            blob = bucket.blob(f"image_storage/{id_folder}/{image_filename}")
            blob.upload_from_file(file)

print(Ids)
print("Successfully get employees list and uploaded images")

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

# Upload face encodings file
firebase_storage_path = "face_encodings/employees.p"
blob = bucket.blob(firebase_storage_path)
blob.upload_from_filename("employees.p")
print("Face encodings uploaded to Firebase Storage")