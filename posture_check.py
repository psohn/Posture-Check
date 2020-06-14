# importing libraries
import cv2
from playsound import playsound

# importing haar cascade for facial recognition
face_cascade = cv2.CascadeClassifier('face.xml')

# using external webcam (set to 0 if computer only has one webcam)
cap = cv2.VideoCapture(1)

# counter for posture
posture_count = 0

# threshold for posture time
posture_time_thresh = 100

# threshold for posture location
posture_loc_thresh = 200

while True:
    # settings for model to read webcam information
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # blue box showing face detection
    for (x,y,w,h) in face:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)
    
    # visualizing if posture is considered good or bad
    if y > posture_loc_thresh:
        cv2.putText(img, "Bad Posture", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))   
    else:
        cv2.putText(img, "Good Posture", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255))
    
    # showing webcam window
    cv2.imshow('Webcam', img)
    
    # escape key set to manually turn off code
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # if slouched, increase posture count
    if y > posture_loc_thresh:
        posture_count += 1
    
    # if not slouched, slowly reset posture count
    if (y < posture_loc_thresh) and (posture_count > 0):
        posture_count -= 1
    
    # if posture count hits threshold, end webcam
    if posture_count == posture_time_thresh:
        break

# destroy webcam view
cap.release()
cv2.destroyAllWindows()

# play music if posture threshold has been reached
if posture_count == posture_time_thresh:
    playsound('condescending_music.mp3')