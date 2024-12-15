import cv2
import time

resetted = True
prev = None
prev_time = time.time()
curr_time = time.time()
cap = None
show=False
current = None

def connect():
    global resetted
    global cap
    global current
    global prev
    global prev_time
    global curr_time
    resetted = True
    prev = current
    prev_time = curr_time
    print("Connecting to camera...")
    if(cap is not None):
        cap.release()
    cap = cv2.VideoCapture("rtsp://192.72.1.1:554/liveRTSP/av4")
    if (cap.isOpened()):
        print("Connected to the camera")
    connect = cap

connect()

while(1):
    curr_time = time.time()
    diff_time = curr_time - prev_time
    prev_time = curr_time
    
    if(diff_time > 5):    
        connect()
        
    if(diff_time > 0.2):
        print("slowness detected. " + str(diff_time) + " seconds.")
        continue

    ret, frame = cap.read()
    
    if ((frame is None) or (ret == False)):
        print("Null frame or No return detected.")
        connect()
        continue
    else:
        current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        current = cv2.GaussianBlur(current, (21, 21), 0)
        if(resetted):
            prev = current
            resetted = False
        else:
            deltaframe=cv2.absdiff(prev,current)    
            threshold = cv2.threshold(deltaframe, 2, 255, cv2.THRESH_BINARY)[1]
            threshold2 = cv2.dilate(threshold,None) 
            countour,heirarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if(len(countour)>2):                
                for i in countour:
                    if cv2.contourArea(i) < 1:
                        continue
                    (x, y, w, h) = cv2.boundingRect(i)
                    if((x>10) and (x<230) and (y>320) and (y<350) and (w<220) and (h<30)): #skip the date and time area of camera feed
                        continue                                        
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    show = True
            if(show):
                cv2.imshow('window',frame)
                show=False
                prev = current            
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
print("Exited")


