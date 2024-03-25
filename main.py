# Imports
import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import datetime as dt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendancefacerecognitio-fed56-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "attendancefacerecognitio-fed56.appspot.com"})
print("Success")

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

# Download encoding from storage
bucket = storage.bucket()
firebase_storage_path = "face_encodings/employees.p"
local_file_path = "employees.p"
blob = bucket.blob(firebase_storage_path)
blob.download_to_filename(local_file_path)
print("Face encodings downloaded from Firebase Storage")

# Load Facial Encoding
file = open("employees.p", "rb")
EmployeeList = pickle.load(file)
file.close()
KnownImgsEncoding, Ids = EmployeeList
print("Successfully loaded employees data and Ids")

# Modes Setup
mode = 0
detect_flag = False
match_timer = 0
marked_flag = False
match_not_found = False
attendance_log = {}
threshold = 0.5

# Show the capture 
while True:
    success, img = cap.read()

    # Resize capture to lower load
    resizedImg = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    resizedImg = cv2.cvtColor(resizedImg,cv2.COLOR_BGR2RGB)

    # Show Image
    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = ModeList[mode]

    FaceFrame = face_recognition.face_locations(resizedImg)
    for face_loc in FaceFrame:
        y1, x2, y2, x1 = face_loc
        y1 *= 4
        x2 *= 4
        y2 *= 4
        x1 *= 4
        bbox = (55 + x1, 162 + y1, x2 - x1, y2 - y1)
        imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

    # Matching
    if not detect_flag:
        # Detect Face in Frame and get encodings
        EncodeFrame = face_recognition.face_encodings(resizedImg, FaceFrame)
        for encoding, face in zip(EncodeFrame, FaceFrame):
            matches = face_recognition.compare_faces(KnownImgsEncoding, encoding, tolerance=threshold)
            match_timer = 180 #Around 5 secs
            if True in matches:
                matchIndex = matches.index(True)
                emp_id = Ids[matchIndex]
                detect_flag = True
                if emp_id not in attendance_log or attendance_log[emp_id] != dt.date.today():
                    attendance_log[emp_id] = dt.date.today()
                    print(attendance_log[emp_id])
                    # Download info
                    ref = db.reference(f"Employees/{emp_id}")
                    emp_info = ref.get() 
                    # Update data
                    ref.child("Attendance_Last_TS").set(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    ref.child("Attendance_Count").set(emp_info["Attendance_Count"]+1)
                    emp_info = ref.get()
                    print(emp_info)
                else:
                    marked_flag = True
            else:
                detect_flag = True
                match_not_found = True               

    # Matched - change mode
    elif not match_not_found:
        mode = 1
        cv2.putText(imgBackground, str(emp_info["Attendance_Count"]),(861,125),
                        cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        match_timer -=1
        if match_timer <= 90:
                if marked_flag == True:
                    mode = 3
                else:
                    mode = 2
        if match_timer <=0:
                mode = 0
                detect_flag = False
    else:
        mode = 4
        match_timer -=1  
        if match_timer <= 90:
                mode = 0
                detect_flag = False
        
    cv2.imshow("Background", imgBackground)
    
    if dt.datetime.now().hour == 23 and dt.datetime.now().minute == 59 and dt.datetime.now().second == 0:
                # Export attendance log
                att_file = f"att_log_{dt.datetime.now().strftime('Y%m%d%H%M%S')}.json"
                ref = db.reference("AttendanceLogs")
                ref.child(att_file).set(attendance_log)
                attendance_log = {}  # Reset attendance log for the next day

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the capture
cap.release()
cv2.destroyAllWindows()