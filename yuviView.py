import cv2
import mediapipe
import pyautogui

print("アプリケーション起動")
pyautogui.FAILSAFE = False
wh = pyautogui.size()

screenWidth = wh.width
screenHeight = wh.height
#print(f"{wh.width} {wh.height}")

#mpDrawing = mediapipe.solutions.drawing_utils

mpHands = mediapipe.solutions.hands

camera = cv2.VideoCapture(0)

hands = mpHands.Hands(min_detection_confidence=0.9)

while True:
    ret,frame = camera.read()
    frame = cv2.flip(frame,1)
    h,w = frame.shape[:2]
    #print(f"{w} {h}")
    image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            #print(f"{handLandmarks.landmark[8].x} {handLandmarks.landmark[8].y}")
            x8 = (int)(handLandmarks.landmark[8].x*w)
            y8 = (int)(handLandmarks.landmark[8].y*h)
            cv2.circle(frame,(x8,y8),15,(0,0,255),thickness=3)
            x4 = (int)(handLandmarks.landmark[4].x*w)
            y4 = (int)(handLandmarks.landmark[4].y*h)
            cv2.circle(frame,(x4,y4),15,(0,255,0),thickness=3)
            #print(f"({x4},{y4}) ({x8},{y8})")
            rateW = w/(w-100)
            rateH = h/(h-100)
            mouseX = (int)(((int)((handLandmarks.landmark[8].x*w)-50)/w)*rateW*(screenWidth))
            mouseY = (int)(((int)((handLandmarks.landmark[8].y*h)-50)/h)*rateH*(screenHeight))
            print(f"{mouseX} {mouseY}")
            #mouseX = (int)(handLandmarks.landmark[8].x*screenWidth)
            #mouseY = (int)(handLandmarks.landmark[8].y*screenHeight)
            pyautogui.moveTo(mouseX,mouseY)
            if(abs(x4-x8)<25 and abs(y4-y8)<25):
                #print("ok")
                cv2.rectangle(frame,(0+50,0+50),(w-50,h-50),(255,0,0),thickness=3)
                #pyautogui.mouseDown()
            else:
                #pyautogui.mouseUp()
                cv2.rectangle(frame,(0+50,0+50),(w-50,h-50),(0,0,255),thickness=3)
            #mpDrawing.draw_landmarks(frame,handLandmarks)
    cv2.imshow('cam',frame)
    key = cv2.waitKey(10)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()