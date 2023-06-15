import mediapipe as mp
import numpy as np


import cv2

counter=0
stage=None





mp_drawing=mp.solutions.drawing_utils
mp_holistic=mp.solutions.holistic

mp_pose=mp.solutions.pose


def calculateangle(a,b,c):
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)


    rad=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])

    angle=np.abs(rad*180/np.pi)

    if angle>180:
        angle=360-angle

        
    return angle

    



cap=cv2.VideoCapture(0);


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()



        img= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        

        img.flags.writeable=False

        result = pose.process(img)

        try:
            landmarks=result.pose_landmarks.landmark


            sh=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elb=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            lwrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            #print(sh)
            #print(elb)
            #print(lwrist)


            angle=calculateangle(sh,elb,lwrist)

            #print(angle)

            
            #cv2.putText(img,str(angle), tuple(np.multiply(elbow,[640,480]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255),2, cv2.LINE_AA)

            #print(landmarks)


            if angle>160:
                stage='down'
            if angle<30 and stage=='down':
                stage='up'
                counter=counter+1
                print(counter)
            
        except:
            pass


    
        cv2.rectangle(img,(0,0),(255,80),(255,255,0),-1)

        cv2.putText(img,'REPS',(20,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2,cv2.LINE_AA)

        cv2.putText(img,str(counter),(15,60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,255),2,cv2.LINE_AA)

        
        
          
        img.flags.writeable=False
        img= cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


        mp_drawing.draw_landmarks(img,result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        
        cv2.imshow("Panel",img)


        if cv2.waitKey(10) & 0xFF== ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




        
