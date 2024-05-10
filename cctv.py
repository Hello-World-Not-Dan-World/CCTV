from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import requests
import sys
import base64

url = 'http://localhost:3000/cctv'

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

count = 0

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    _, img_encoded = cv2.imencode('.jpg', image)
    encoded_frame = base64.b64encode(img_encoded).decode('utf-8')


    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    
    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    if prediction[0][0] > 0.1:
        index = 0

    if index == 1:
        count = count + 1

    elif index == 0:
        count = 0

    if count == 1:
        #data = {'img': imgcopy, 'text':str(prediction[0][1])}
        data = {'id': "cctv1",'img': encoded_frame, 'text':str(prediction[0][1])}        
        response = requests.post(url, data)
        if response.status_code == 200:
            print('요청이 성공했습니다.')
            print('응답 데이터:', response.text)
        else:
            print('요청이 실패했습니다. 상태 코드:', response.status_code)
        count = 0
        
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
