import os
import cx_Oracle
import pyautogui
import tkinter
############################DB PART##############################
    
LOCATION = r"C:\instantclient_21_3"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

dsn = cx_Oracle.makedsn('localhost', 1521, 'orcl')
db = cx_Oracle.connect('mapledata', 'next0507', dsn)
cursor = db.cursor()

#################################################################
cursor.execute("select * from skilldata")
data = cursor.fetchall()



def asdf():
    shortcut_key = pyautogui.locateCenterOnScreen(
            "shortcut_key.PNG", confidence = 0.85, region = (0,0,1050,800))

    shortcut_x, shortcut_y = shortcut_key

    cursor.execute("select count(*) from skilldata")
    length = cursor.fetchall()
    
    for i in range(length[0][0]):
        imagepath = data[i][1] + data[i][0] + ".PNG"
        try:
            skill_icon = pyautogui.locateCenterOnScreen(
                imagepath, confidence = 0.83, region = (0,0,1050,800))
            skill_icon_x, skill_icon_y = skill_icon
            cood_x = skill_icon_x -shortcut_x
            cood_y = skill_icon_y - shortcut_y
            for arr in keyicon_coordinate.items():
                if cood_x == arr[1][0] and cood_y == arr[1][1]:
                    print(arr[0], data[i][0])
        except TypeError:
            pass

        
        

        
keyicon_coordinate = {'esc': [-28,54], 'f1': [38,54], 'f2': [71,54], 'f3': [104,54],'f4': [137,54],
                      'f5': [187,54], 'f6': [220,54], 'f7': [253,54], 'f8': [286,54],'f9': [336,54],
                      'f10': [369,54], 'f11': [402,54], 'f12': [435,54], '`': [-28,92],'1': [5,92],
                      '2': [38,92], '3': [71,92], '4': [104,92], '5': [137,92],'6': [170,92],
                      '7': [203,92], '8': [236,92], '9': [269,92], '0': [302,92],'-': [335,92],
                      '=': [369,92], 'q': [21,125], 'w': [54,125], 'e': [87,125],'r': [120,125],
                      't': [153,125], 'y': [186,125], 'u': [219,125], 'i': [252,125],'o': [285,125],
                      'p': [318,92], '[': [351,125], ']': [384,125], 'a': [37,158],'s': [70,158],
                      'd': [103,92], 'f': [136,125], 'g': [169,125], 'h': [202,158],'j': [235,158],
                      'k': [268,158], 'l': [301,158], ';': [334,158], "'": [367,158],'shift': [-4,191],
                      'z': [53,191], 'x': [86,191], 'c': [119,191], 'v': [152,191],'b': [185,191],
                      'n': [218,191], 'm': [251,191], ',': [284,191], '.': [317,191],'ctrl': [-20,224],
                      'alt': [78,224], 'space': [202,224], 'insert': [476,92], 'home': [509,92], 'pageup': [542,92],
                      'delete': [476,125], 'end': [509,125], 'pagedown': [542,125],
                      }


#################################tkinter부분
window=tkinter.Tk()
window.title("asdf")
window.geometry("300x200+200+800")
window.resizable(False, False)


frame1 = tkinter.Frame(window)
button = tkinter.Button(frame1, text="START", width=10, command= asdf)

frame1.pack()
button.pack()
window.mainloop()
