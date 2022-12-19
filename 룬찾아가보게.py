import os
import cx_Oracle
import time
import random
import pyautogui
import keyboard

#########################매크로 모듈################################
def prv_dly(num):   #매크로 탐지 방해 지연함수
    n = random.uniform(0.0,num)#매크로 미연에방지
    nn = round(n,3)
    return nn;

def mouse_click(x,y,delay):#말그대로 마우스 클릭 함수
    mouse_control.position=(x,y)
    mouse_control.press(mouse_button.left)
    mouse_control.release(mouse_button.left)
    time.sleep(float(delay)+prv_dly(0.05))
    
def mouse_move(x,y,delay):   #마우스를 원하는 좌표로 이동
    mouse_control.position=(x,y)
    time.sleep(float(delay)*prv_dly(0.05))
    
def mouse_drag(x,y):   #원하는 좌표를 좌클릭 드래그
    mouse_control.position=(x,y)
    mouse_control.press(mouse_button.left)

def mouse_drop(x,y,delay): #원하는 좌표를 좌클릭 드랍
    mouse_move(x,y,delay)
    mouse_control.release(mouse_button.left)
    time.sleep(float(delay)*prv_dly(0.05))
    
def key_down(key,delay):#키 꾹 누르길 원할때 쓰는 함수
    keyboard.press(key)
    time.sleep(float(delay)+prv_dly(0.05))
    keyboard.release(key)
    
def key_click(key,delay):#키 눌럿다뗏다 원할때 쓰는 함수
    keyboard.press(key)
    keyboard.release(key)
    time.sleep(float(delay)+prv_dly(0.05))

def strong_key_click(key,delay):
    rand_num = round(random.uniform(0.15,0.3), 3)
    keyboard.press(key)
    keyboard.release(key)
    time.sleep(float(delay*rand_num)+prv_dly(0.02))
    keyboard.press(key)
    keyboard.release(key)
    time.sleep(float(delay*(1-rand_num))+prv_dly(0.02))



def move_dicy():  #점프만 하게함.
    key_click("alt",0.16)
    keyboard.press("x")
    time.sleep(0.03+prv_dly(0.01))
    keyboard.press("up")
    time.sleep(0.03+prv_dly(0.01))
    keyboard.press("left")
    time.sleep(0.6+prv_dly(0.01))
    keyboard.release("x")
    keyboard.release("up")
    keyboard.release("left")

rune = pyautogui.locateCenterOnScreen('rune.PNG', confidence = 0.72, region = (0,0,400,300))
rune_x, rune_y = rune
time.sleep(1)

char = pyautogui.locateCenterOnScreen('char.PNG', confidence = 0.72, region = (0,0,400,300))
char_x, char_y = char


key_click("alt",0.16)
keyboard.press("x")
time.sleep(0.03+prv_dly(0.01))
if rune_x < char_x:
    keyboard.press("left")
elif rune_x > char_x:
    keyboard.press("right")
elif rune_x == char_x:
    pass
    
time.sleep(0.02+prv_dly(0.01))

if rune_y == char_y:
    pass
elif rune_y < char_y:
    keyboard.press("up")
elif rune_y > char_y:
    keyboard.press("down")
time.sleep(0.6+prv_dly(0.01))
keyboard.release("x")
keyboard.release("up")
keyboard.release("left")
keyboard.release("down")
keyboard.release("right")


time.sleep(1)
char = pyautogui.locateCenterOnScreen('char.PNG', confidence = 0.72, region = (0,0,400,300))

print(char)

