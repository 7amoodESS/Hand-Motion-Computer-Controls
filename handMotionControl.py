import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx
import pyautogui
mouse = Controller()

# gets size of screen monitor
app = wx.App(False)
# screen resolution, width and height
(x_screen, y_screen) = wx.GetDisplaySize()
# camera resolution, width and height
(x_cam, y_cam) = (320, 200)

# HSV
lowerHSV = np.array([33,80,40])
upperHSV = np.array([102,255,255])

cam = cv2.VideoCapture(0)

kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))
closeFlag = 0

while True:
    ret, img = cam.read()
    img = cv2.resize(img,(340, 220))

    # convert RGB to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the mask
    mask = cv2.inRange(imgHSV, lowerHSV, upperHSV)
    # morphology
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    h,contour,_ = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # 2 objects, move mouse cursor
    if(len(contour) == 2):
        if(closeFlag == 1):
            closeFlag = 0
            mouse.release(Button.left)
        x1, y1, w1, h1 = cv2.boundingRect(contour[0])
        x2, y2, w2, h2 = cv2.boundingRect(contour[1])
        
        # calculates center width and height of each object
        # object 1
        x1_center = x1 + w1 / 2
        y1_center = y1 + h1 / 2
        # object 2
        x2_center = x2 + w2 / 2
        y2_center = y2 + h2 / 2
        
        # calculates center between two objects
        x_center = (x1_center + x2_center) / 2
        y_center = (y1_center + y2_center) / 2
        
        # mouse movement
        # convert camera/image resolution to screen resolution
        mouseLocation = (x_screen - (x_center * x_screen / x_cam), y_center * y_screen / y_cam)
        mouse.position = mouseLocation 
        while mouse.position != mouseLocation:
            pass
    
    # 1 object, closed gesture to left click mouse
    elif(len(contour) == 1):
        x, y, w, h = cv2.boundingRect(contour[0])
        if(closeFlag == 0):
            closeFlag = 1
            mouse.press(Button.left)
        
        # calculates center width and height object
        x_center = x + w / 2
        y_center = y + h / 2
        
        # mouse movement
        mouseLocation = (x_screen - (x_center * x_screen / x_cam), y_center * y_screen / y_cam)
        mouse.position = mouseLocation 
        while mouse.position != mouseLocation:
            pass
    
    # 3 objects, left arrow key
    elif(len(contour) == 3):
        pyautogui.press('left')
        while mouse.position != mouseLocation:
            pass
    
    # 4 objects, right arrow key
    elif(len(contour) == 4):
        pyautogui.press('right')
        while mouse.position != mouseLocation:
            pass
    cv2.imshow("video",img)
    cv2.waitKey(5)
