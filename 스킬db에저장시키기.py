import os
import cx_Oracle
import cv2

LOCATION = r"C:\instantclient_21_3"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]

dsn = cx_Oracle.makedsn('localhost', 1521, 'orcl')
db = cx_Oracle.connect('mapledata', 'next0507', dsn)
cursor = db.cursor()

path = r"C:/Users/yoonhong/Desktop/maple_macro/hoyoung_skill/" # 폴더 경로
os.chdir(path) # 해당 폴더로 이동
files = os.listdir(path) # 해당 폴더에 있는 파일 이름을 리스트 형태로 받음

skilltype = ['mainattack', 'buff', 'cooltimeattack', 'cooltimebuff', 'costattack', 'costbuff', 'etc']
skilltypenum = [1,6,1,0,5,6,2,2,2,2,4,0,3,3,
                0,6,2,3,4,6,5,5,3,2,6,2,3,5,
                3,0]

cooltime = [0,300,0,0,0,0,180,
            8,250,180,0,0,100,200,
            0,0,11,240,0,30,0,
            0,90,6,0,250,200,200,
            100,0]

skilldelay = [0.25,0.25,0.6,0.66,0.63,0,0.72,
              0.54,0.87,0.99,0.72,0.69,0.72,0.9,
              0.69,0,0.42,0.5,0.48,1.56,0.9,
              0.99,0.78,0.66,0.6,0.96,0.9,0.9,
              0.54,0.69]

count = 0
for file in files:
    if '.PNG' in file:
        print(file[:-4])
        cursor.execute("INSERT INTO skilldata VALUES('%s', '%s', '%s', '%d', '%d')"
                       %(file[:-4], path, skilltype[skilltypenum[count]],
                         cooltime[count], skilldelay[count]*1000))
        
    count = count + 1
#cursor.execute("commit")


