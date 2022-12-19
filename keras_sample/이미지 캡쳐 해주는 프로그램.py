import os
import macromodule
import pyautogui
import time
import cv2


for a in range(1):
    x, y = pyautogui.locateCenterOnScreen('monster_count.png',confidence = 0.85, region = (0,0,1024,768))
    
    pyautogui.screenshot(r'C:/Users/yoonhong/Desktop/maple_macro/counting_monster/{}.png'.format(int(time.time())),
                         region = (x+99,y-6,28,8))
    time.sleep(1)

