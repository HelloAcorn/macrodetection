import os 
import cv2

path = r"C:/Users/yoonhong/Desktop/maple_macro/counting_monster/" # 폴더 경로
os.chdir(path) # 해당 폴더로 이동
files = os.listdir(path) # 해당 폴더에 있는 파일 이름을 리스트 형태로 받음

count = 0

for file in files:
    if '.png' in file:
        src = cv2.imread(file)
        src_y = src.shape[0]
        src_x = src.shape[1]
        temp = int(src_x / 7)
        for a in range(temp):
            count = count+1
            dst = src[0:8, a*7:a*7+7].copy()
            cv2.imwrite('{}.png'.format(count),dst)




