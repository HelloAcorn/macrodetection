import keyboard
import pyautogui
import pynput
import math
import time
import random

mouse_control = pynput.mouse.Controller()
mouse_button = pynput.mouse.Button


def prv_dly(num):   #매크로 탐지 방해 지연함수
    n = random.uniform(0.0,num)#매크로 미연에방지
    nn = round(n,3)
    return nn;

def mouse_move(x,y,delay):   #마우스를 원하는 좌표로 이동
    mouse_control.position=(x,y)
    time.sleep(float(delay)*prv_dly(0.05))

def mouse_drag(x,y):   #원하는 좌표를 좌클릭 드래그
    mouse_control.position=(x,y)
    mouse_control.press(mouse_button.left)

def mouse_drop(x,y,delay):        #원하는 좌표를 좌클릭 드랍
    mouse_move(x,y,delay)
    mouse_control.release(mouse_button.left)
    time.sleep(float(delay)*prv_dly(0.05))
    
def mouse_click(x,y,delay):#말그대로 마우스 클릭 함수 (x좌표,y좌표,종료후 딜레이)
    mouse_control.position=(x,y)
    mouse_control.press(mouse_button.left)
    mouse_control.release(mouse_button.left) 
    time.sleep(float(delay)*prv_dly(0.05))

    
def key_down(key,delay):#키 꾹 누르길 원할때 쓰는 함수  (키, 종료후 딜레이)
    keyboard.press(key)
    time.sleep(float(delay)*prv_dly(0.02))
    keyboard.release(key)
    
def key_click(key,delay):#키 눌럿다뗏다 원할때 쓰는 함수 (키, 종료후 딜레이)
    keyboard.press(key)
    keyboard.release(key)
    time.sleep(float(delay)*prv_dly(0.05))

def image_click(img_name,con,delay): #이미지를 찾아 가운데로 마우스 이동 함수  (이미지이름,정확도, 종료후 딜레이)
    center = pyautogui.locateCenterOnScreen(img_name, confidence = con)
    x, y = center
    mouse_control.position=(x,y)
    time.sleep(float(delay)*prv_dly(0.05))
    return x, y

def find_my_mouse():
    print("현재 위치:" ,pyautogui.position())

def find_image(img_name,con):
    center = pyautogui.locateCenterOnScreen(img_name, confidence = con)
    x, y = center
    return x, y
