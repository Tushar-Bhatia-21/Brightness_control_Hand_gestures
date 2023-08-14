import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict
import subprocess
import time

# Constants for display brightness
BRIGHTNESS_INCREASE = 20
BRIGHTNESS_DECREASE = -10
vol_flag=0
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)

def set_brightness_inc():
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "Absolute Path of Increase.ps1"])

def set_brightness_dec():
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "Absolute Path of Decrease.ps1"])

def set_vol_inc():
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "Absolute Path of Volume Increase.ps1"])

def set_vol_dec():
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "Absolute Path of Volume Decrease.ps1"])

def set_mute():
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "Absolute path of Mute.ps1"])


cap = cv2.VideoCapture(0)
ctr=0
while True:
    time.sleep(1)
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        # Both Hands are present in image(frame)
        if len(results.multi_handedness) == 2:
            vol_flag=1
            if vol_flag==1:
                cv2.putText(img, 'Volume Control', (250, 50),cv2.FONT_HERSHEY_COMPLEX,0.9, (0, 255, 0), 2)
                time.sleep(2)
                ctr+=1
            if ctr==6:
                set_mute()
                ctr=0
                # Display 'Both Hands' on the image
            #cv2.putText(img, 'Both Hands', (250, 50),
             #           cv2.FONT_HERSHEY_COMPLEX,
              #          0.9, (0, 255, 0), 2)
        else:    
            for i in results.multi_handedness:
                label = MessageToDict(i)['classification'][0]['label']
                if vol_flag==0:
                    if label == 'Left':
                        set_brightness_dec()
                        label = label + ' Hand'
                        cv2.putText(img, label, (20, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                    elif label == 'Right':
                        set_brightness_inc()
                        label = label + ' Hand'
                        cv2.putText(img, label, (460, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                
                elif ctr==2:
                    ctr=0
                    vol_flag=0
                # VOLUME CONTROL
                elif vol_flag==1:
                    if label == 'Left':
                        set_vol_dec()
                        label = label + ' Hand'
                        cv2.putText(img, label, (20, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
                elif label == 'Right':
                    label = label + ' Hand'
                    set_vol_inc()
                    cv2.putText(img, label, (460, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
