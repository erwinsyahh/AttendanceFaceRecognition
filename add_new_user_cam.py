# Imports
import cv2
import time
import datetime as dt
import os
import pickle
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage, db
import threading

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

# Function to register a new face
def register_new_face():
    
    def add_user_info(user_id, name, role):
        user_info = {
            user_id: {
                "Name": name,
                "Role": role,
                "Attendance_Count": 0,
                "Attendance_Last_TS": ""
            }}

        # Push the user information to the database under the user_id
        ref = db.reference(f"Employees")
        ref.update(user_info)

    print("Registering a new face...")
    new_face_encodings = []
    new_ids = []
    employee_id = input("Enter the employee ID: ")
    employee_name = input("Enter the employee Name: ")
    employee_role = input("Enter the employee Role: ")

    # Create a directory to save the images if it doesn't exist
    images_dir = f"Resources\Images\{employee_id}\\"
    os.makedirs(images_dir, exist_ok=True)

    for i, angle in enumerate(["straight forward", "slightly tilted left", "slightly tilted right"], start=1):
        while True:
            print(f"Capture face image {i}/3: {angle}. Please adjust.")
            time.sleep(1)
            print("3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)
            success, img = cap.read()
            if not success:
                print("Failed to capture image.")
                continue

            # Resize image to lower load
            resized_img = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

            # Detect face locations
            face_locations = face_recognition.face_locations(resized_img)

            if len(face_locations) == 1:

                # Save the image to the directory
                datestamp = dt.datetime.now().strftime("%Y%m%d")
                image_path = os.path.join(images_dir, f"{datestamp}_{i}.jpg")
                cv2.imwrite(image_path, img)
                print(f"Image {i}/3 saved to {image_path}")

                # Encode face
                image = cv2.imread(image_path)
                face_encoding = face_recognition.face_encodings(image)[0]
                new_face_encodings.append(face_encoding)
                new_ids.append(employee_id)
                print(f"Image {i}/3 captured successfully.")

                break  # Exit the loop if a face is successfully captured
            else:
                print("Failed to detect a face. Please try again.")

    # Initialize and update real time employee data
    add_user_info(employee_id, employee_name, employee_role)

    # Download encoding from storage
    bucket = storage.bucket()
    firebase_storage_path = "face_encodings/employees.p"
    local_file_path = "employees.p"
    blob = bucket.blob(firebase_storage_path)
    blob.download_to_filename(local_file_path)
    print("Face encodings downloaded from Firebase Storage")

    # Append new face encoding to employees.p
    try:
        with open("employees.p", "rb") as file:
            existing_employee_data = pickle.load(file)
            existing_face_encodings, employee_ids = existing_employee_data
            existing_face_encodings.extend(new_face_encodings)
            employee_ids.extend(new_ids)

        with open("employees.p", "wb") as file:
            pickle.dump([existing_face_encodings, employee_ids], file)
        print("New face encoding appended to 'employees.p'.")
    except FileNotFoundError:
        print("File 'employees.p' not found. Creating a new file.")

        # Create a new employees.p file with new data
        new_data = [new_face_encodings, new_ids]

        with open("employees.p", "wb") as file:
            pickle.dump(new_data, file)
        print("New file 'employees.p' created with the first employee data.")
    
    # Upload updated encodings to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob("face_encodings/employees.p")
    blob.upload_from_filename("employees.p")
    print("Updated encoding data uploaded to Firebase Storage.")

# Main loop
while True:
    success, img = cap.read()

    # Display the captured image
    cv2.imshow("Capture", img)
    key = cv2.waitKey(1)

    # If 'r' is pressed, register a new face
    if key & 0xFF == ord('r'):
        threading.Thread(target=register_new_face).start()
    # If 'q' is pressed, quit the program
    if key & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
