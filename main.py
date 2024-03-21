# Imports
import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone

# Webcam Capture
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread("Resources/bg.png")

# Modes setup
ModeFolderPath = "Resources/Modes"
ModesPath = os.listdir(ModeFolderPath)
ModeList = []
for path in ModesPath:
    ModeList.append(cv2.imread(os.path.join(ModeFolderPath, path)))

# Load Attendants Data
file = open("attendants.p", "rb")
AttendantList = pickle.load(file)
file.close()
KnownImgsEncoding, Ids = AttendantList
print("Successfully loaded attendants data and Ids")

# Show the capture 
while True:
    success, img = cap.read()

    # Resize capture to lower load
    resizedImg = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    resizedImg = cv2.cvtColor(resizedImg,cv2.COLOR_BGR2RGB)

    # Detect Face in Frame and get encodings
    FaceFrame = face_recognition.face_locations(resizedImg)
    EncodeFrame = face_recognition.face_encodings(resizedImg, FaceFrame)

    # Show Image
    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = ModeList[2]

    # Matching
    for encoding, face in zip(EncodeFrame, FaceFrame):
         matches = face_recognition.compare_faces(KnownImgsEncoding, encoding)
         distance = face_recognition.face_distance(KnownImgsEncoding, encoding)
         matchIndex = np.argmin(distance)
         if matches[matchIndex]:
              print(Ids[matchIndex])
              y1, x2, y2, x1 = face
              y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
              bbox = 55+x1, 162+y1, x2-x1, y2-y1
              imgBackground = cvzone.cornerRect(imgBackground, bbox, rt= 0)

    cv2.imshow("Background", imgBackground)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture
cap.release()
cv2.destroyAllWindows()