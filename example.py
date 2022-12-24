"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""


import cv2
import time
#from scipy.spatial import distance
#from imutils import face_utils
from gaze_tracking import GazeTracking
from gpiozero import LED
led = LED(14)
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
startTime = time.time()
countblink=0
counter=0
state = 0    #  0 => S   1 => L  2=> R 3=> F   4=>B

    

while True: 
    curentTime = time.time()    
    # We get a new frame from the webcam
    _, frame = webcam.read()


    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    difference = curentTime - startTime

    #if gaze.is_blinking():
    #    print("in is_blinking ==1 before checking the state")
    #    print (state)
    #    print (startTime)
    #    print (curentTime)
    #    print (countblink)
    #    if(state != 4):
    #        startTime=time.time()
    #        state=4
    #        print("in is_blinking ==1 after checking the state")
    #        print (state)
    #        print (startTime)
    #        print (curentTime)
    #        print (countblink)
    #       # counter+=1
    #       # print(counter)
    #       # text = "Blinking"
    #        #led.off()
    #elif(not gaze.is_blinking()):
    #    print("in is_blinking ==0 before checking the time different")
    #    print (state)
    #    print (startTime)
    #    print (curentTime)
    #    if(difference >= 1 ):
    #        if(state==4):
    #            countblink+=1
    #            state=0
    #            print("in is_blinking==0 after checking the time different")
    #            print (state)
    #            print(startTime)
    #            print(curentTime)
    #            print (countblink)
    #                #startTime=curentTime
    #    # counter=0
    

    #if gaze.is_blinking():
    #    #if(state != 4):
    #        #startTime=time.time()
    #        #state=4
    #    counter+=1
    #    print(counter)
    #    text = "Blinking"
    #       #led.off()
    #else:
    #    if(counter >3):
    #        #if(curentTime - startTime >= 3 ):
    #            #print(curentTime , startTime)
    #        countblink+=1
    #            #state=0
    #            #startTime = curentTime
    #        counter=0
                

    
    if gaze.is_right():
        if(state != 2):
            startTime = time.time()
            state = 2
        text = "Looking right"
        if(curentTime - startTime > 3):
            text = "looking right"
            #led.on()
    elif gaze.is_left():
        state = 1
        text = "Looking left"
        #led.off()
    elif gaze.is_center():
        state = 3
        text = "Looking center"
        #led.off()
    
    #if(countblink == 3):
    #    if(gaze.is_right()):
    #        text = "looking right"
    #        if(state != 2):
    #            startTime=time.time()
    #            state=2
    #        if(curentTime - startTime >= 2):
    #            text = " we will turn right now"
    #            #counterblink=0
#
    #    elif(gaze.is_center()):
    #        text = "looking center"
    #        if(state != 3):
    #            startTime=time.time()
    #            state=3
    #        if(curentTime - startTime >= 2):
    #            text = " we will go forward"
    #            #counterblink=0
    #            
    #    elif(gaze.is_left()):
    #        text = "looking left"
    #        if(state != 1):
    #            startTime=time.time()
    #            state=1
    #        if(curentTime - startTime >= 2):
    #            text = " we will turn left now"
    #            #counterblink=0
#
    #elif(countblink == 4):
    #    text = "stop the chair"
    #    #countblink=0
    #
    #elif(countblink == 5):
    #    if(gaze.is_center()):
    #        text = "looking center"
    #        if(state != 5):
    #            startTime=time.time()
    #            state=5
    #        if(curentTime - startTime >= 2):
    #            text = " we will go backward"
    #            #counterblink=0

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame ,"blinking number: " +str(countblink),(90,200),cv2.FONT_HERSHEY_DUPLEX,0.9 ,(147,58,31),1)
   
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break

     # Update the previous frame and frame difference
    prev_frame = frame
    frame_diff = None
   
webcam.release()
cv2.destroyAllWindows()
