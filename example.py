import cv2
import time
from gaze_tracking import GazeTracking
#from gpiozero import LED
#led = LED(14)
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
#time to start detect if the command is basic or special
startTime = time.time()
#time to detect if this command to move the wheelchair 
startCommandTime = time.time()
#total blink
countblink=0
#detect if he want Basic command or special command
state = 0    #1=>Basic  2=>special  1_1=>right  1_2=>forward    1_3=>left   2_1=>backward
#detect if he want Basic command or special command
lookingState = 0   #=>0 => none     1=>Basic    2=>special
# true if i close
eyeClose=False
#true if eye open
eyeOpen=True
# detect the blinking time
blinkStartTime = time.time()
    
while True: 
    curentTime = time.time()    
    # We get a new frame from the webcam
    _, frame = webcam.read()


    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    #ratio = gaze.is_blinking()
    #print(ratio)

    if (gaze.is_blinking()==1): 
        print("close")
        eyeOpen=False
        if not eyeClose:
            blinkStartTime = time.time() 
            eyeClose = True
        if(curentTime - blinkStartTime >= 2 and curentTime - blinkStartTime <= 4 and eyeClose and not eyeOpen):
            countblink +=1
            blinkStartTime = time.time()
    
    elif(gaze.is_blinking()==2): 
        print("open")
        eyeOpen=True
        eyeClose =False


    if(countblink==3 and lookingState==0):
        #Basic command => forward left right 
        if(gaze.is_right()):
            text = "right"
            if(state != 1):
                startTime=time.time()
                state=1
            if(curentTime - startTime >= 2):
                text = " Basic command"
                #now we will take the eye movement as command to move the chair
                lookingState=1
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

                
    if(lookingState==1):   
        if(gaze.is_right()):
            text = "looking right"
            if(state != 1_1):
                startTime=time.time()
                state=1_1
            if(curentTime - startTime >= 2):
                text = " we will turn right now"
                lookingState=0
                counterblink=0

        elif(gaze.is_center()):
            text = "looking center"
            if(state != 1_2):
                startTime=time.time()
                state=1_2
            if(curentTime - startTime >= 2):
                text = " we will go forward"
                lookingState=0
                counterblink=0
        
        elif(gaze.is_left()):
            text = "looking left"
            if(state != 1_3):
                startTime=time.time()
                state=1_3
            if(curentTime - startTime >= 2):
                text = " we will turn left now"
                lookingState=0
                counterblink=0  

    elif(lookingState==2):
        if(gaze.is_center()):
                    text = "looking center"
                    if(state != 2_1):
                        startCommandTime=time.time()
                        state=2_1
                    if(curentTime - startCommandTime >= 2):
                        text = " we will go backward"
                        lookingState=0
                        counterblink=0
    
    ###################################################################################3
    # TO check the basic and special command
        # For now, we'll use the states
        # State_0  --> Initial state
        # State_1  --> Basic Command
        # State_11 --> Turn_Left
        # State_12 --> Turn_Right
        # State_2  --> Special Command
        # State_21 --> Forward
        # State_22 --> Backward
        # State_3  --> Controlling by a Friend

        # S_C_Flag     --> Stop/Cancel Command
        # accept_flag  --> Accepting the Command.
        # forget_flag  --> Forget_to_Blink
        # con_flag     --> check continuously
        # c_a_flag     --> check_accept_flag
        # c_c_flag     --> check_command_flag            

    # if (state ==0): #Initial State - Do NOTHING
    #     # The user should blink 3 times:
    #     # The screen will show if the user wanna chose the Basic or Special commands
    #     # if (c_c_flag ==1)
    #         # Look left for Basic Command --> state = 1
    #         # Look right for special command --> state =2
    #     time.sleep(2)
    #     state =1

    # #######################################################################################

    # if ( state ==1 or pre_state == 1): #Basic Command
    #     # Show the user if he/she wanna move left/right on the screan
    #     text = "LEFT OR RIGHT !"
    #     # Check if we need to turn left OR right
    #     c_c_flag =1
    #     # If the user look left  --> state = 11
    #     # If the user look Right --> state = 12
    #     pre_state =1
    #     time.sleep(2)
    #     state =11
    #     if (state ==11): # Turn Left
    #         # Show the command on the screan
    #         text = "LEFT COMMAND"
    #         c_a_flag =1
    #         time.sleep(2)
    #         c_a_flag =0
    #         accept_flag=1
    #         if ( accept_flag and not c_a_flag): #Accepting the Command.
    #             #The wheelchair will move in a 30 or 45 degree to the wanted angle.
    #             text = "MOVING LEFT"
    #             time.sleep(2)                
    #             state = 0
    #         elif (forget_flag and not c_a_flag):
    #             S_C_Flag=1
        
    #     elif (state ==12): # Turn Right
    #         # Show the command on the screan
    #         c_a_flag =1
    #         if ( accept_flag and not c_a_flag): #Accepting the Command.
    #             #The wheelchair will move in a 30 or 45 degree to the wanted angle.
    #             text = "The wheelchair will move in a 30 or 45 degree to the wanted angle"
    #         elif (forget_flag and not c_a_flag):
    #             S_C_Flag=1
                
    #     elif (S_C_Flag): #Stop/Cancel Command OR Forget_to_Blink
    #             state = 0 # To return to the initial state
    #             accept_flag =0
                
    #######################################################################################
    
    # if gaze.is_right():
    #     #blink_state=False
    #     if(state != 2):
    #         startTime = time.time()
    #         state = 2
    #     text = "Looking right"
    #     if(curentTime - startTime > 2):
    #         text = "looking right now"
    #         #led.on()
    # elif gaze.is_left():
    #     blink_state=False
    #     state = 11
    #     text = "Looking left"
    #     #led.off()
    # elif gaze.is_center():
    #     if(state != 3):
    #         startTime = time.time()
    #         state = 3
    #     text = "Looking center"
    #     if(curentTime - startTime > 2):
    #         text = "Looking center now"
    #     blink_state=False
    #     # state = 3
        
    #     #led.off()
    
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