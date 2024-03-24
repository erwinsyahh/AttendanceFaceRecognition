import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime as dt

# Initialize firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attendancefacerecognitio-fed56-default-rtdb.asia-southeast1.firebasedatabase.app/"})
print("Success")

# Push data to realtime db
ref = db.reference("Employees")
data = {
    "erwin": {
    "Name": "Erwinsyah",
    "Role": "Data Science",
    "Attendance_Count": 2,
    "Attendance_Last_TS": dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    "ariel": {
    "Name": "Nuzril",
    "Role": "Influencer",
    "Attendance_Count": 0,
    "Attendance_Last_TS": dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
    "heisen": {
    "Name": "Walter White",
    "Role": "Chemist",
    "Attendance_Count": 10,
    "Attendance_Last_TS": dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
}

for key, value in data.items():
    ref.child(key).set(value)
print("Success")