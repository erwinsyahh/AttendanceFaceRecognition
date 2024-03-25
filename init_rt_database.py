import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime as dt

# Initialize firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendancefacerecognitio-fed56-default-rtdb.asia-southeast1.firebasedatabase.app/"})

# Push data to realtime db
ref = db.reference("Employees")
data = {
    "XXX1": {
    "Name": "Nuzril",
    "Role": "Influencer",
    "Attendance_Count": 2,
    "Attendance_Last_TS": dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    "XXX3": {
    "Name": "Walter White",
    "Role": "Chemist",
    "Attendance_Count": 10,
    "Attendance_Last_TS": dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
}

for key, value in data.items():
    ref.child(key).set(value)
print("Success")