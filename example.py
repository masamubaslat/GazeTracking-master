import cv2
import time
from gaze_tracking import GazeTracking
from gpiozero import LED
led1 = LED(14)
led2 = LED(15)
led3 = LED(18)
led4 = LED(23)
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
startTime = time.time()
startCommandTime = time.time()
#total blink number
countblink=0
state = 0    # 
lookingState = 0 # 1=> Basic Command (looking right) 2=> special command (looking left)
#True when eye is close
eyeClose=False
#True when eye is open
eyeOpen=True
#when true increment blinkcounter 
conterFlag=False
blinkStartTime = time.time() 
 
if _name_ == '_main_':      
    try:
        while True: 
            # led1.off()
            # led2.off()
            # led3.on()
            # led4.on()
            #take the current time with every frame
            curentTime = time.time()    
            # We get a new frame from the webcam
            success, frame = webcam.read()
            print(success)
            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            frame = gaze.annotated_frame()
            text = ""

            difference = curentTime - blinkStartTime 

            #ratio = gaze.is_blinking()
            #print(ratio)
            if (gaze.is_blinking()==1): 
                print("close")
                eyeOpen=False
                if not eyeClose:
                    blinkStartTime = time.time() 
                    eyeClose = True
                if(difference>= 2 and difference <= 4 and eyeClose and not eyeOpen):
                    if(not conterFlag):
                        countblink +=1
                        blinkStartTime = time.time()
            
            elif(gaze.is_blinking()==2): 
                print("open")
                eyeOpen=True
                eyeClose =False


            if(countblink==3 and lookingState==0):
                conterFlag=True
                #Basic command => forward left right 
                if(gaze.is_right()):
                    text = "right"
                    if(state != 1):
                        startTime=time.time()
                        state=1
                    if(curentTime - startTime >= 2):
                        text = " Basic command"
                        #time.sleep(0.5)
                        lookingState=1
                        #now we will take the eye movement as command to move the chair
                        #countblink=0

                elif(gaze.is_left()):
                    text = "left"
                    if(state != 2):
                        startTime=time.time()
                        state=2
                    if(curentTime - startTime >= 2):
                        text = "special command"
                        lookingState=2
                        #countblink=0
                        #now we will take the eye movement as command to move the chair

                        
             # Basic Command => Left ,Right ,Forward 
            if(lookingState==1):   
                if(gaze.is_right()):
                    text = "looking right"
                    if(state != 1_1):
                        startTime=time.time()
                        state=1_1
                    if(curentTime - startTime >= 2):
                        text = " we will turn right now"
                        led1.on()
                        #time.sleep(2)
                        led2.off()
                        led3.off()
                        led4.off()
                    
                        lookingState=0
                        countblink=0
                        conterFlag=False

                elif(gaze.is_center()):
                    text = "looking center"
                    if(state != 1_2):
                        startTime=time.time()
                        state=1_2
                    if(curentTime - startTime >= 2):
                        text = " we will go forward"
                        led1.on()
                        #time.sleep(2)
                        led2.off()
                        led3.on()
                        #time.sleep(2)
                        led4.off()
                        
                        lookingState=0
                        countblink=0
                        conterFlag=False
                
                elif(gaze.is_left()):
                    text = "looking left"
                    if(state != 1_3):
                        startTime=time.time()
                        state=1_3
                    if(curentTime - startTime >= 2):
                        text = " we will turn left now"
                        led1.off()
                        led2.off()
                        led3.on()
                        #time.sleep(2)
                        led4.off()
                        lookingState=0
                        countblink=0  
                        conterFlag=False

            elif(lookingState==2):
                if(gaze.is_left()):
                    text = "looking center"
                    if(state != 2_1):
                        startCommandTime=time.time()
                        state=2_1
                    if(curentTime - startCommandTime >= 2):
                        text = " we will go backward"
                        led1.off()
                        led2.on()
                        #time.sleep(2)
                        led3.off()
                        led4.on()
                        #time.sleep(2)
                        countblink=0
                        lookingState=0
                        conterFlag=False

                elif(gaze.is_right()):
                    text = "stop command"
                    led1.off()
                    led2.off()
                    led3.off()
                    led4.off()
                    lookingState=0
                    countblink=0  
                    conterFlag=False

            cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
            cv2.putText(frame ,"blinking number: " +str(countblink),(90,100),cv2.FONT_HERSHEY_DUPLEX,0.9 ,(147,58,31),1)

            cv2.imshow("Demo", frame)

            if cv2.waitKey(1) == 27:
                break
    except KeyboardInterrupt:
        pass

webcam.release()
cv2.destroyAllWindows()