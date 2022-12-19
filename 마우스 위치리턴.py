from macromodule import *
import keyboard
import tkinter


#테스트
def test():
    global temp
    if temp == True:
        button.config(text = "START")
        temp = False
    elif temp == False:
        button.config(text = "STOP")
        temp = True


#################################tkinter부분
temp = False
window=tkinter.Tk()
window.title("lifegod")
window.geometry("300x200+200+800")
window.resizable(False, False)


frame1 = tkinter.Frame(window)
label = tkinter.Label(frame1, text="마우스 위치 리턴")
label2 = tkinter.Label(frame1, text=" ")
entry1 = tkinter.Entry(frame1)
button = tkinter.Button(frame1, text="START", width=10, command=test)

label.pack()
label2.pack()
button.pack()
entry1.pack()
frame1.pack()
while True:
    if temp == True:
        find_my_mouse()
        time.sleep(0.5)
    window.update()

################################################
    

