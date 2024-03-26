# Facial Recognition System with Firebase Integration

This project implements a facial recognition system using the dlib and face-recognition modules as a baseline. The system includes data processing and a pipeline for storing employee data, face data, and attendance data in Firebase. 

## Features

- Facial recognition using dlib and face-recognition module
- Integration with Firebase for data storage
- Real-time database for storing employee details and attendance data
- Automatic logs creation and reset for attendance tracking
- Ability to handle faces not found in the encoding data

## Getting Started

To use the system, follow these steps:

1. Initialize the real-time database and face `encoding init_rt_database.py` and `init_face_encoder.py`.
2. Start the face recognition system using `main.py`.
2. To capture new user and face data use `add_new_user_cam.py`.

## Baseline Model

The facial recognition system is based on the resnet-34 model, as described in [this blog post](http://blog.dlib.net/2017/02/high-quality-face-recognition-with-deep.html), and implemented in the [face-recognition](https://github.com/ageitgey/face_recognition) module.

## Fine-tuning Model

Additionally, a resnet50 model was fine-tuned on the Indonesian Muslim Student Face Dataset (IMSFD) for a classification problem. After achieving decent metrics, the model was used to extract features and embeddings from faces. A custom dataset (`metadata.csv`) with similarity labels was created and used to compare the accuracy performance with the baseline model. The fine-tuned model achieved better accuracy on the custom similarity dataset and was saved as `resnet_model.pth`.

## Attendance System

The attendance system has the following specifications:

- Logs are created at midnight and reset for the next day.
- If an employee is already marked for the day, it will display "already marked".
- Can handle faces that are not found in the encoding data.

## Data Flow

Encodings and ID data are stored in `employees.p`, which is uploaded, updated, and downloaded as needed. Employee images and encodings are stored in Firebase Storage, while real-time database is used for storing employee details and attendance data simultaneously.

## Takeaways

- The dlib and face-recognition module still prone to misses, might be worth it to try the model fine-tuned from the IMSFD dataset.
- Try other approaches and ways of creating facial similarity prediction models, such as using siamese network, changing model architecture, face detectors, and further fine-tuning.
- The image backgrounds and modes should be improved.
- Code can be cleaned further, especially regarding the application and data flow.

## Reference

This project is inspired by the work of Murtazza Hasan, whose tutorial on facial recognition served as a basis for the implementation. You can find the tutorial [here](https://www.youtube.com/watch?v=iBomaK2ARyI).

