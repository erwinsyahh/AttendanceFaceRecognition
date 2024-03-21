# Imports
import cv2
import os
import face_recognition
import pickle

# Initial image setup
ImageFolderPath = "Resources/Images"
ImagesPath = os.listdir(ImageFolderPath)
ImageList = []
Ids = []
for path in ImagesPath:
    ImageList.append(cv2.imread(os.path.join(ImageFolderPath, path)))
    Ids.append(os.path.splitext(path)[0])
print(Ids)

def get_encoding(Images):
    encodingList = []
    for img in ImageList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(img)[0]
        encodingList.append(encoding)
    return encodingList

KnownImgsEncoding = get_encoding(ImageList)
AttendantList = [KnownImgsEncoding, Ids]
print("Successfully get features from Images")

file = open("attendants.p", "wb")
pickle.dump(AttendantList, file)
file.close()
print("Successfully saved attendants data and Ids")