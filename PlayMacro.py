import os
print(os.getcwd()+r'\images\hunt_count.png')

import cv2
import keyboard
import pyautogui
import pynput
import math
import time
import random
import tkinter
import queue
import threading
import cx_Oracle
from pynput import keyboard as PYNPUT
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps, ImageGrab
import numpy as np
import warnings

warnings.filterwarnings('ignore')
mouse_control = pynput.mouse.Controller()
mouse_button = pynput.mouse.Button
THREAD_QUEUE = queue.Queue()  #큐생성

NUMBER_MODEL = load_model('keras_number_model.h5',compile = False)
RUNE_MODEL = load_model('keras_rune_model.h5',compile = False)


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
    
LOCATION = r"C:\instantclient_21_3"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

dsn = cx_Oracle.makedsn('localhost', 1521, 'orcl')
db = cx_Oracle.connect('C##mapledata', 'next0507', dsn)
cursor = db.cursor()

UPLOAD_DB_LISTED = []
SMALL_DBDATA = []
HUNT_COUNT = 0

def mold_string(text):  ##db에서 이름 가져올때 어긋나는거 수정.
    text = str(text)
    text = text.replace("'","")
    temp = 'Key.' in text
    if temp:
        text = text[4:]

    if text == 'ctrl_l':
        text = 'ctrl'

    if text == 'alt_l':
        text = 'alt'

    if text == 'shift_l':
        text = 'shift'
        
    return text

start_time = time.time()
end_time = time.time()
def on_press(key):
    global start_time
    global end_time
    if WORKS_PROGRAM == True:
        start_time = time.time()
        SMALL_DBDATA = []
        key = mold_string(key)
        for i in range(len(KEYSETDATA)):
            if KEYSETDATA[i][1] == key:
                SMALL_DBDATA.append(KEYSETDATA[i][0])
        if len(SMALL_DBDATA) != 0:
            SMALL_DBDATA.append(CHAR_XY[0])
            SMALL_DBDATA.append(CHAR_XY[1])
            SMALL_DBDATA.append(HUNT_COUNT)##몬스터수
            SMALL_DBDATA.append(round(start_time - end_time,3))
            UPLOAD_DB_LISTED.append(SMALL_DBDATA)
        end_time = time.time()



def on_release(key):
    pass

def record_DB():
    global WORKS_PROGRAM
    WORKS_PROGRAM = True
    UPLOAD_DB_LISTED.clear()
    listener = PYNPUT.Listener(on_press = on_press, on_release = on_release)
    listener.start()
    th1 = threading.Thread(target = update_DB)
    th1.start()


def update_DB():
    while WORKS_PROGRAM == True:
        keyblock = 0
        time.sleep(30)
        cursor.execute("select * from key_block")
        data = cursor.fetchall()
        keyblock = data[0][0]
        cursor.execute("update key_block set count = count+1")
        
        
        for i in range(len(UPLOAD_DB_LISTED)):
            #스킬키, x좌표, y좌표, 몬스터 처치수
            cursor.execute("INSERT INTO east_wall VALUES ('%s','%d','%d','%d','%f', '%d')"
                           %(UPLOAD_DB_LISTED[i][0], UPLOAD_DB_LISTED[i][1],
                             UPLOAD_DB_LISTED[i][2], UPLOAD_DB_LISTED[i][3],
                             UPLOAD_DB_LISTED[i][4], keyblock))
            
        UPLOAD_DB_LISTED.clear()
        cursor.execute("commit")

    
#마리수 가져오는 함수
def get_huntcount():
    global HUNT_COUNT
    try:
        x, y = pyautogui.locateCenterOnScreen(os.getcwd()+r'\images\monster_count.png',confidence = 0.85, region = (0,0,1024,768))
    except TypeError:
        pass

    while WORKS_PROGRAM == True:
        pyautogui.screenshot(os.getcwd()+r'/images/hunt_count.png',
                    region = (x+99,y-6,28,8))
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        size = (224, 224)
        image = Image.open(os.getcwd()+r'\images\hunt_count.png')
        
        img_x, img_y = image.size
        image_size = int(img_x / 7)
        kill_num = 0
        for length in range(image_size):
            cut_image = image.crop((7*(image_size-1-length),0,7*(image_size-length),8))
            cut_image = ImageOps.fit(cut_image, size, Image.BILINEAR)
            image_array = np.asarray(cut_image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            # run thte inference
            prediction = NUMBER_MODEL.predict(data)
            guess_number = []
            for i in range(11):
                guess_number.append(prediction[0][i])            
            tmp = max(guess_number)
            index = guess_number.index(tmp)
            if index != 10:
                kill_num = kill_num + (index*10**length)
        HUNT_COUNT = kill_num
        time.sleep(0.05)


def get_keysetting():
    global KEYSETDATA
    cursor.execute("select trim(key), trim(skillname) from hoyoung_keyset")
    KEYSETDATA = cursor.fetchall()
    match_skillname_to_keyset()
    
        
###################단축기 가져오기###############
Keyicon_Coordinate = {'esc': [-28,54], 'f1': [38,54], 'f2': [71,54], 'f3': [104,54],'f4': [137,54],
                      'f5': [187,54], 'f6': [220,54], 'f7': [253,54], 'f8': [286,54],'f9': [336,54],
                      'f10': [369,54], 'f11': [402,54], 'f12': [435,54], '`': [-28,92],'1': [5,92],
                      '2': [38,92], '3': [71,92], '4': [104,92], '5': [137,92],'6': [170,92],
                      '7': [203,92], '8': [236,92], '9': [269,92], '0': [302,92],'-': [335,92],
                      '=': [369,92], 'q': [21,125], 'w': [54,125], 'e': [87,125],'r': [120,125],
                      't': [153,125], 'y': [186,125], 'u': [219,125], 'i': [252,125],'o': [285,125],
                      'p': [318,125], '[': [351,125], ']': [384,125], 'a': [37,158],'s': [70,158],
                      'd': [103,158], 'f': [136,158], 'g': [169,158], 'h': [202,158],'j': [235,158],
                      'k': [268,158], 'l': [301,158], ';': [334,158], "'": [367,158],'shift': [-4,191],
                      'z': [53,191], 'x': [86,191], 'c': [119,191], 'v': [152,191],'b': [185,191],
                      'n': [218,191], 'm': [251,191], ',': [284,191], '.': [317,191],'ctrl': [-20,224],
                      'alt': [78,224], 'space': [202,224], 'insert': [476,92], 'home': [509,92], 'pageup': [542,92],
                      'delete': [476,125], 'end': [509,125], 'pagedown': [542,125],
                      }


KEYSETDATA = [] ##스킬이름-키 해싱과 같은 리스트
def Match_Keysetting():
    global KEYSETDATA
    cursor.execute("delete from hoyoung_keyset")    #키셋 갈아엎으면 초기화
    shortcut_x, shortcut_y = pyautogui.locateCenterOnScreen(
            os.getcwd()+r"\images\shortcut_key.PNG", confidence = 0.85, region = (0,0,1920,1080))
    cursor.execute("select count(*) from skilldata")
    length = cursor.fetchall()

    cursor.execute("select * from skilldata")
    data = cursor.fetchall()
    
    for i in range(length[0][0]):   #호영 스킬 전수조사
        imagepath = data[i][1] + data[i][0] + ".PNG"
        temp = []
        try:
            skill_icon_x, skill_icon_y = pyautogui.locateCenterOnScreen(
                imagepath, confidence = 0.77, region = (shortcut_x-40,shortcut_y,shortcut_x+570,shortcut_y+250))
            
            cood_x = skill_icon_x -shortcut_x
            cood_y = skill_icon_y - shortcut_y
            for arr in Keyicon_Coordinate.items():
                if cood_x >= arr[1][0]-3 and cood_x <= arr[1][0]+3 and cood_y >= arr[1][1]-3 and cood_y <= arr[1][1]+3 :
                    temp.append(arr[0])
                    temp.append(data[i][0])
                    KEYSETDATA.append(temp)
        except TypeError:
            pass
    
    try:
        x, y = pyautogui.locateCenterOnScreen('exit1.PNG',confidence = 0.8, region = (0,0,1920,1080))
        mouse_click(x, y,0.3)
    except TypeError:
        KEYSETDATA = []
        label.configure(text = "실패: 설정 아이콘이 보이게 해주세요.")
        cursor.execute("delete from hoyoung_keyset")


    print(KEYSETDATA)
    for i in range(len(KEYSETDATA)):
        cursor.execute("insert into hoyoung_keyset values('%s', '%s')"
                       %(KEYSETDATA[i][1], KEYSETDATA[i][0]))
    cursor.execute("insert into hoyoung_keyset values('up', 'up')");
    cursor.execute("insert into hoyoung_keyset values('down', 'down')");
    cursor.execute("insert into hoyoung_keyset values('left', 'left')");
    cursor.execute("insert into hoyoung_keyset values('right', 'right')");
    cursor.execute("commit")
    
    label.configure(text = "키세팅 확인 완료!!")



def play_keyset():
    label.configure(text = "키세팅을 불러오는중...")
    try:
        x, y = pyautogui.locateCenterOnScreen(os.getcwd()+r'\images\setting.PNG',confidence = 0.8, region = (0,0,1920,1080))
        mouse_click(x, y,0.05)
        mouse_click(x, y,0.2)
        x, y = pyautogui.locateCenterOnScreen(os.getcwd()+r'\images\shortkey_setting.PNG',confidence = 0.8, region = (0,0,1920,1080))
        mouse_click(x, y,0.3)
        Match_Keysetting()
    except TypeError:
        try:
            x, y = pyautogui.locateCenterOnScreen(os.getcwd()+r'\images\shortcut_key.PNG',confidence = 0.8, region = (0,0,1920,1080))
            if x !=0 and y != 0:
                Match_Keysetting()
                return
        except TypeError:
            label.configure(text = "실패: 설정 아이콘이 보이게 해주세요.")            
        label.configure(text = "실패: 설정 아이콘이 보이게 해주세요.")



#######################룬 해제 관련 함수####################################
#######################룬 해제 관련 함수####################################
#######################룬 해제 관련 함수####################################
#######################룬 해제 관련 함수####################################
#######################룬 해제 관련 함수####################################
#꼭지점 찾는 함수
def findLocalMaxima(src):
    kernel = cv2.getStructuringElement(shape=cv2.MORPH_CROSS,ksize=(9,9))
    dilate = cv2.dilate(src,kernel) #팽창
    localMax = (src==dilate)
    erode = cv2.erode(src,kernel)   #침식
    localMax2 = src>erode
    localMax &= localMax2
    points = np.argwhere(localMax == True)
    points[:,[0,1]] = points[:,[1,0]]
    return points


#꼭지점이 어디어디 몰려있는지 확인하는 함수
def get_center_rect(array):
    point_array = []
    arrow_box = []
    for i in range(len(array)):
        temp = []
        temp.append(int(array[i][0]))
        temp.append(int(array[i][1]))
        point_array.append(temp)
    
    
    random.shuffle(point_array)
    while len(point_array) >= 1:
        target_box = []
        while_num = len(point_array)-1
        temp = 0
        target_x, target_y = point_array[0]
        target_box.append(point_array[0])
        point_array.pop(temp)   
        while len(point_array)-2 >= temp:
            temp = temp +1
            temp_x, temp_y = point_array[temp]
            if target_x-30 <= temp_x and temp_x <= target_x+30 and target_y-25 <= temp_y and temp_y <= target_y+25:
                target_box.append(point_array[temp])
                point_array.pop(temp)
            while_num = while_num -1

        if len(target_box) >= 6:
            arrow_box.append(target_box)

    return arrow_box



#중복되는 꼭지점을 삭제하고 오름차순으로 정렬해주는 함수
def get_arranged_box(array):
    box_array = []
    for a in range(len(array)):
        count = len(array[a])
        sum_x = 0
        sum_y = 0
        for b in range(count):
            temp_x, temp_y = array[a][b]
            sum_x = sum_x + temp_x
            sum_y = sum_y + temp_y
        temp = []
        sum_x = int(sum_x / count)
        sum_y = int(sum_y / count)
        temp.append(sum_x)
        temp.append(sum_y)
        box_array.append(temp)

    box_array.sort()
    
    if len(box_array) > 4:
        index = 0
        while index < len(box_array)-1:
            if abs(box_array[index][0] - box_array[index+1][0]) <=32 and abs(box_array[index][1] - box_array[index+1][1]) <=32:
                box_array.pop(index)
            index = index+1

    return box_array



#자른 이미지를 머신러닝 모델에 넣어서 확인하는 함수
def get_cropped_img(final_box, cut_img):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    size = (224, 224)
    for i in range(len(final_box)):
        cropped = cut_img[final_box[i][1]-16 : final_box[i][1]+16 , final_box[i][0]-16: final_box[i][0]+16]
        rune_img_name = time.time()
        cv2.imwrite("{0}.png".format(rune_img_name), cropped)
        cropimg = Image.open("{0}.png".format(rune_img_name))
        image = ImageOps.fit(cropimg, size, Image.BILINEAR)
        #turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array
        prediction = RUNE_MODEL.predict(data)
        if prediction[0,0] > prediction[0,1] and prediction[0,0] > prediction[0,2] and prediction[0,0] > prediction[0,3] and prediction[0,0] > prediction[0,4]:
            key_click("up", 0.2)
        elif prediction[0,1] > prediction[0,0] and prediction[0,1] > prediction[0,2] and prediction[0,1] > prediction[0,3] and prediction[0,1] > prediction[0,4]:
            key_click("down", 0.2)
        elif prediction[0,2] > prediction[0,0] and prediction[0,2] > prediction[0,1] and prediction[0,2] > prediction[0,3] and prediction[0,2] > prediction[0,4]:
            key_click("left", 0.2)
        elif prediction[0,3] > prediction[0,0] and prediction[0,3] > prediction[0,1] and prediction[0,3] > prediction[0,2] and prediction[0,3] > prediction[0,4]:
            key_click("right", 0.2)
        elif prediction[0,4] > prediction[0,0] and prediction[0,4] > prediction[0,1] and prediction[0,4] > prediction[0,2] and prediction[0,4] > prediction[0,3]:
            pass

def decoring_rune():
    image = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(280, 190, 720, 310))), cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.getcwd()+r"\images\wholerune.png", image)
    img = cv2.imread(os.getcwd()+r"\images\wholerune.png", cv2.IMREAD_COLOR)
    print(img)
     
    #NI 이미지 블러
    captured_img = cv2.fastNlMeansDenoisingColored(img, None, 15, 15, 5, 10)
    cut_img = captured_img.copy()
    rectangle = (10, 5, 410, 90)
    mask = np.zeros(captured_img.shape[:2], np.uint8)
    # grabCut에 사용할 임시 배열 생성
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    # grabCut 실행
    cv2.grabCut(captured_img, # 원본 이미지
               mask,       # 마스크
               rectangle,  # 사각형
               bgdModel,   # 배경을 위한 임시 배열
               fgdModel,   # 전경을 위한 임시 배열 
               5,          # 반복 횟수
               cv2.GC_INIT_WITH_RECT) # 사각형을 위한 초기화
    mask_2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')
    # 이미지에 새로운 마스크를 곱해 배경을 제외
    captured_img = captured_img * mask_2[:, :, np.newaxis]
    captured_img = cv2.cvtColor(captured_img, cv2.COLOR_BGR2GRAY)
    _, captured_img = cv2.threshold(captured_img, 168, 255, cv2.THRESH_BINARY)
    captured_img = cv2.cvtColor(captured_img, cv2.COLOR_BGR2RGB)
    captured_img = cv2.medianBlur(captured_img, 3)
    captured_img = cv2.GaussianBlur(captured_img, (5,5), 0)
    captured_img = cv2.fastNlMeansDenoisingColored(captured_img, None, 3, 3, 5, 10)
    captured_img = cv2.cvtColor(captured_img, cv2.COLOR_BGR2GRAY)
    _, captured_img = cv2.threshold(captured_img, 170, 255, cv2.THRESH_BINARY)
    res = cv2.preCornerDetect(captured_img,ksize=3)
    ret,res2 = cv2.threshold(np.abs(res),0.1,0,cv2.THRESH_TOZERO)

    corners = findLocalMaxima(res2)
    boxed = get_center_rect(corners)
    final_box = get_arranged_box(boxed)
    get_cropped_img(final_box, cut_img)
#######################룬 해제 관련 함수####################################
#######################룬 해제 관련 함수####################################
#######################룬 해제 관련 함수####################################
#######################룬 해제 관련 함수####################################
#######################룬 해제 관련 함수####################################
#######################룬 해제 관련 함수####################################
        
def find_rune():#사용하는 기본 사냥스킬(중복되는건 스킬빈도)
    global WORKS_PROGRAM
    while WORKS_PROGRAM == True:
        rune_cor = pyautogui.locateCenterOnScreen(os.getcwd()+r'\images\rune.png', confidence = 0.68, region = (0,0,MAPDATA[2]+50,MAPDATA[1]+50))
        if rune_cor != None:
            WORKS_PROGRAM = False
            time.sleep(1)
            x, y = rune_cor
            move_char_to_target(x, y)
            
            WORKS_PROGRAM = True
            record_DB()
            run() #재시작
            
            

def move_char_to_target(rune_x, rune_y):
    while True:
        char = pyautogui.locateCenterOnScreen(os.getcwd()+r'\images\char.PNG', confidence = 0.72, region = (0,0,MAPDATA[2]+50,MAPDATA[1]+50))
        char_x, char_y = char
        if rune_x-5 <= char_x and char_x <= rune_x+5 and rune_y-1 <= char_y and char_y <= rune_y+1 :
            break
        key_click("alt",0.15)
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
        time.sleep(0.2+prv_dly(0.5))
        keyboard.release("x")
        keyboard.release("up")
        keyboard.release("left")
        keyboard.release("down")
        keyboard.release("right")
    key_click("space", 0.2)
    decoring_rune()
    

    
#####################사냥 스레드에 관련되는 함수들##########################    
#judge 0=랜덤 1=왼쪽 2=오른쪽
def jump_char():  #점프만 하게함.
    jump = random.randint(3,4)  #점프 2~3번뛸지 정하기
    key_click("alt",0.09)
    for _ in range(jump):
        key_click("alt",0.11)


def used_kill():#사용하는 기본 사냥스킬(중복되는건 스킬빈도)
    key_click = ['c', 'f', 'ctrl', 'r', 'shift']
    key_delay = [0.6,0.5,0.7,0.3,0.5]
    random = random.randint(0,5)
    key_click(key_click[random],key_delay[random])


def used_mainskill():#사용하는 기본 사냥스킬(중복되는건 스킬빈도)
    key_click(MAINATTACK_SKILL[0][0],MAINATTACK_SKILL[0][1])



##키사용세팅에서 사용자 키셋 확인
MAINATTACK_SKILL = []
SUBATTACK_SKILL = []
def match_skillname_to_keyset():
    global MAINATTACK_SKILL
    global SUBATTACK_SKILL
    #주력 사냥기
    cursor.execute("select skillname, skilldelay, cooltime from skilldata where skilltype = 'mainattack'")
    data = cursor.fetchall()   
    MAINATTACK_SKILL = load_skilldata(data)

    #보조 사냥기
    cursor.execute("""select skillname, skilldelay, cooltime from skilldata
                        where (skillname = 'chasingghost' or skillname = 'clonesage' or skillname = 'goldcudgel' or skillname = 'crestofthesollar' or 
		skillname = 'energyillusion' or skillname = 'extremeclone' or skillname = 'phantasmalclone' or skillname = 'rainbowbutterfiles' or 
		skillname = 'grandisgoddess' or skillname = 'taeuldivine' or skillname = 'summontiger' or skillname = 'strangegods' or 
		skillname = 'spyderinmirror' or skillname = 'ropeconnect' or skillname = 'comflagrationchain')""")
    data = cursor.fetchall()   
    SUBATTACK_SKILL = load_skilldata(data)

    
def load_skilldata(data):
    skillarray = []
    
    for a in range(len(KEYSETDATA)):
        temp = []
        for b in range(len(data)):
            if KEYSETDATA[a][0] == data[b][0]:  #이름이 같으면
                temp.append(KEYSETDATA[a][1])
                temp.append(data[b][1]/1000.0)
                temp.append(data[b][2]/1000.0)
                skillarray.append(temp)
                
    return skillarray

    
#사냥터의 미니맵 크기 리턴
def mapsize(size_x):
    global MAPDATA
    try:
        MAPDATA = [0 for i in range(4)]     
        arcane = pyautogui.locateAllOnScreen(os.getcwd()+r'\images\arcaneforce.PNG', confidence = 0.8, region = (0,0,400,300))
        authentic = pyautogui.locateAllOnScreen(os.getcwd()+r'\images\authenticforce.PNG', confidence = 0.8, region = (0,0,400,300))
        
        arcane = list(arcane)
        authentic = list(authentic)
        if len(list(arcane)) != 0:
            arcane = list(arcane).pop()
            MAPDATA[0],MAPDATA[1],dummy1,dummy2 = arcane
        elif len(list(authentic)) != 0:
            authentic = list(authentic).pop()
            MAPDATA[0],MAPDATA[1],dummy1,dummy2 = authentic
        
        world = pyautogui.locateOnScreen(os.getcwd()+r'\images\world.PNG', confidence = 0.85, region = (0,0,400,800))
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
            char = pyautogui.locateCenterOnScreen(os.getcwd()+r'\images\char.PNG', confidence = 0.72, region = (0,0,MAPDATA[2]+50,MAPDATA[1]+50))
            CHAR_XY[0], CHAR_XY[1] = char
            time.sleep(0.15)
        except TypeError:   #char를 못찾았을때
            pass
        
#캐릭터가 좌우로 돌아보게 해주는 함수
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
        time.sleep(prv_dly(cooltime / 10) + cooltime)
        




#게임화면을 좌상단에 고정시켜준다.
def set_game():
    center = pyautogui.locateCenterOnScreen(os.getcwd()+r"\images\mapleicon.png", confidence = 0.9)
    x, y = center
    x = x+30
    if (x>50 and y>50):
        pyautogui.moveTo(x,y)
        mouse_control.press(mouse_button.left)
        time.sleep(0.15)
        pyautogui.moveTo(42,12)
        mouse_control.release(mouse_button.left)

    get_keysetting()
    record_DB()
    #db 레코드를 시작합니다.
    run()
    

#메인 사냥 함수
def run():
    global WORKS_PROGRAM
    WORKS_PROGRAM = True
    mouse_click(500,50,0.5)
    #미니맵 사이즈는 맵에따라 다르니까 손으로 수정
    mapsize(30)
    
    char_thread = threading.Thread(target = update_character)       #캐릭터 위치 업데이트 스레드
    char_thread.start()
    turn_thread = threading.Thread(target = turn_character)         #캐릭터 좌우 방향 바꿔주는 스레드
    turn_thread.start()
    rune_thread = threading.Thread(target = find_rune)              #룬을 찾는 스레드
    rune_thread.start()
    huntcount_thread = threading.Thread(target = get_huntcount)     #마리수 알려주는 스레드
    huntcount_thread.start()
    manegement_buff()

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
            THREAD_QUEUE.clear()
            WORKS_PROGRAM = False
        

#################################tkinter부분

WORKS_PROGRAM = True
window=tkinter.Tk()
window.title("asdf")
window.geometry("300x200+200+800")
window.resizable(False, False)


frame1 = tkinter.Frame(window)
label = tkinter.Label(frame1, text="시작시 전투분석을 꼭 켜주세요")
label2 = tkinter.Label(frame1, text="")
button = tkinter.Button(frame1, text="START", width=10, command= set_game)
button2 = tkinter.Button(frame1, text="키사용세팅", width=10, command= lambda: play_keyset())


label.pack()
label2.pack()
button.pack()
button2.pack()
frame1.pack()
window.mainloop()
################################################


