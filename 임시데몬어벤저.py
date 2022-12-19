import keyboard
import pyautogui
import pynput
import math
import time
import random
import tkinter
import queue
import threading
from pynput import keyboard as PYNPUT
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

mouse_control = pynput.mouse.Controller()
mouse_button = pynput.mouse.Button
THREAD_QUEUE = queue.Queue()  #큐생성


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
    
#########################전역 변수################################
#캐릭터의 좌표
CHAR_XY = [0,0]
#좌하단X, 좌하단Y, 우상단X, 우상단Y
MAPDATA = []
#프로그램 전체의 루프를 담당하는 변수
WORKS_PROGRAM = False


############################DB PART##############################
 
#judge 0=랜덤 1=왼쪽 2=오른쪽
def jump_char():  #점프만 하게함.
    jump = random.randint(3,4)  #점프 2~3번뛸지 정하기
    key_click("alt",0.08)
    for _ in range(jump):
        key_click("alt",0.1)



def used_mainskill():#사용하는 기본 사냥스킬(중복되는건 스킬빈도)
    random = random.randint(2,3)
    for i in range(random):
        key_click('d', 0.13)
    key_click('shift', 0.45)


    
#사냥터의 미니맵 크기 리턴
def mapsize(size_x):
    global MAPDATA
    try:
        MAPDATA = [0 for i in range(4)]     
        arcane = pyautogui.locateAllOnScreen('arcaneforce.PNG', confidence = 0.8, region = (0,0,400,300))
        authentic = pyautogui.locateAllOnScreen('authenticforce.PNG', confidence = 0.8, region = (0,0,400,300))
        
        arcane = list(arcane)
        authentic = list(authentic)
        if len(list(arcane)) != 0:
            arcane = list(arcane).pop()
            MAPDATA[0],MAPDATA[1],dummy1,dummy2 = arcane
        elif len(list(authentic)) != 0:
            authentic = list(authentic).pop()
            MAPDATA[0],MAPDATA[1],dummy1,dummy2 = authentic
        
        world = pyautogui.locateOnScreen('world.PNG', confidence = 0.85, region = (0,0,400,800))
        MAPDATA[2],MAPDATA[3],wid,hei = world
        MAPDATA[2] = MAPDATA[2] + wid - size_x
        MAPDATA[0] = MAPDATA[0] + size_x
        
    except UnboundLocalError:
        time.sleep(0.5)
        print("force 재탐색")
        mapsize(size_x)
        
    except TypeError:
        time.sleep(0.5)
        print("world 재탐색")
        mapsize(size_x)
        

#캐릭터의 위치를 계속 갱신시키는 함수
def update_character():
    global CHAR_XY
    while WORKS_PROGRAM == True:
        try:
            char = pyautogui.locateCenterOnScreen('char.PNG', confidence = 0.78, region = (0,0,MAPDATA[2]+50,MAPDATA[1]+50))
            CHAR_XY[0], CHAR_XY[1] = char
            time.sleep(0.15)
        except TypeError:   #char를 못찾았을때
            pass

def turn_character():
    while WORKS_PROGRAM == True:
        if CHAR_XY[0] < MAPDATA[0]:
            key_down("right", 0.42)
        if CHAR_XY[0] > MAPDATA[2]:
            key_down("left", 0.42)
        time.sleep(0.2)

        




#각종 버프들 모음
def manegement_buff():   
    for key, delay, cooltime in SUBATTACK_SKILL:
        tmp_thread=threading.Thread(target = give_buff, args=(key,delay,cooltime), daemon=True)
        tmp_thread.start()    



#버프 및 쿨탐 스킬 사용 함수
def give_buff(key,delay,cooltime):
    if cooltime == 0:
        cooltime = 35
    time.sleep(prv_dly(cooltime))
    while WORKS_PROGRAM == True:
        t1 = threading.Thread(target = key_click, args=(key,delay), daemon=True)
        THREAD_QUEUE.put(t1)
        print(key)
        time.sleep(prv_dly(cooltime / 10) + cooltime)
        




#게임화면을 좌상단에 고정시켜준다.
def set_game():
    try:
        center = pyautogui.locateCenterOnScreen("mapleicon.png", confidence = 0.9)
        x, y = center
        x = x+30
        if (x>50 and y>50):
            pyautogui.moveTo(x,y)
            mouse_control.press(mouse_button.left)
            time.sleep(0.15)
            pyautogui.moveTo(42,12)
            mouse_control.release(mouse_button.left)
    except:
        pass
    run()
    

#메인 사냥 함수
def run():
    global WORKS_PROGRAM
    WORKS_PROGRAM = True
    mouse_click(500,50,0.5)
    mapsize(26)   #미니맵 사이즈
    char_thread = threading.Thread(target = update_character)
    char_thread.start()
    turn_thread = threading.Thread(target = turn_character)
    turn_thread.start()


    
    while WORKS_PROGRAM == True:
        if THREAD_QUEUE.empty() == True:
            t1 = threading.Thread(target = jump_char, daemon=True)
            t2 = threading.Thread(target = used_mainskill, daemon = True)
            THREAD_QUEUE.put(t1)
            THREAD_QUEUE.put(t2)
            
        while THREAD_QUEUE.empty() != True:
            temp = THREAD_QUEUE.get()
            temp.start()
            temp.join()
            
        if keyboard.is_pressed('f12'):
            button.configure(state = tkinter.NORMAL)  
            WORKS_PROGRAM = False
        

#################################tkinter부분

    
window=tkinter.Tk()
window.title("asdf")
window.geometry("300x200+200+800")
window.resizable(False, False)


frame1 = tkinter.Frame(window)
label = tkinter.Label(frame1, text="시작시 전투분석을 꼭 켜주세요")
label2 = tkinter.Label(frame1, text="")
button = tkinter.Button(frame1, text="START", width=10, command= set_game)


label.pack()
label2.pack()
button.pack()
frame1.pack()
window.mainloop()
################################################


