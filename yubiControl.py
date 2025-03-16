import cv2
import mediapipe
import pyautogui

view = False

mouseFlag = False


pyautogui.FAILSAFE = False
wh = pyautogui.size()

screenWidth = wh.width
screenHeight = wh.height

mpHands = mediapipe.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.9)

camera = cv2.VideoCapture(0)

print("アプリケーション起動")

while True:
    ret,frame = camera.read()
    frame = cv2.flip(frame,1)
    h,w = frame.shape[:2]
    image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            x8 = (int)(handLandmarks.landmark[8].x*w)
            y8 = (int)(handLandmarks.landmark[8].y*h)
            if view:
                cv2.circle(frame,(x8,y8),15,(0,0,255),thickness=3)
            x4 = (int)(handLandmarks.landmark[4].x*w)
            y4 = (int)(handLandmarks.landmark[4].y*h)
            if view:
                cv2.circle(frame,(x4,y4),15,(0,255,0),thickness=3)
            mouseX = (int)(handLandmarks.landmark[8].x*screenWidth)
            mouseY = (int)(handLandmarks.landmark[8].y*screenHeight)
            rateW = w/(w-100)
            rateH = h/(h-100)
            mouseX = (int)(((int)((handLandmarks.landmark[8].x*w)-50)/w)*rateW*(screenWidth))
            mouseY = (int)(((int)((handLandmarks.landmark[8].y*h)-50)/h)*rateH*(screenHeight))
            pyautogui.moveTo(mouseX,mouseY)
            if(abs(x4-x8)<25 and abs(y4-y8)<25):
                if(mouseFlag==False):
                    pyautogui.mouseDown()
                mouseFlag = True
                if view:
                    cv2.rectangle(frame,(0+50,0+50),(w-50,h-50),(255,0,0),thickness=3)
            else:
                if(mouseFlag==True):
                    pyautogui.mouseUp()
                mouseFlag = False
                if view:
                    cv2.rectangle(frame,(0+50,0+50),(w-50,h-50),(0,0,255),thickness=3)
    if view:
        cv2.imshow('yubiCam',frame)
        key = cv2.waitKey(10)
        if key == 27:
            break
                
camera.release()
cv2.destroyAllWindows()