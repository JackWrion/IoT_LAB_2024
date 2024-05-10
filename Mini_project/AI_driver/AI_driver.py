from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import base64
import threading


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
# Load the model
model = load_model("AI_driver/keras_model.h5", compile=False)
# Load the labels
class_names = open("AI_driver/labels.txt", "r").readlines()
# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)


r_class = "NONE"
r_data = 0

def AI_Execute():
    # Grab the webcamera's image. Free buffer after time.sleep()
    # for i in range(5):
    #     camera.grab()

    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    
    # Backup data for post-processing
    data = image
    

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)      # (batch size, x, y , RGB channels)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    
    confidence_score = prediction[0][index]
    
    class_name = class_names[index]
    class_name =  class_name.split(" ")[1]

    # Print prediction and confidence score
    # print("Class:", class_name)
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")


    # #Listen to the keyboard for presses.
    # keyboard_input = cv2.waitKey(1)

    # # 27 is the ASCII for the esc key on your keyboard.
    # if keyboard_input == 27:
    #     break



    # Show the image in a window
    cv2.putText(data, class_name, (90, 40), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow("Webcam Image", data)
    # base64 encoded data for uploading to platform
    r,data = cv2.imencode(".jpg", data, [cv2.IMWRITE_JPEG_QUALITY, 40])
    data = base64.b64encode(data)



    cv2.waitKey(10)
    return data, class_name

def AI_Stop():
    camera.release()
    cv2.destroyAllWindows()

def AI_Get():
    global r_data, r_class
    return r_data, r_class

def AI_Start():
    global r_class, r_data
    while True:
        r_data, r_class = AI_Execute()

AI_thread = threading.Thread(target=AI_Start)
AI_thread.start()


# For TESTING
# while True:
#     mydata, classname = AI_Execute()
#     print (classname)
     
# AI_Stop()


    
