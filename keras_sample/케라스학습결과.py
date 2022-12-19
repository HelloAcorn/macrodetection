from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import os
import time


path = r"C:/Users/yoonhong/Desktop/maple_macro/keras_sample/" # 폴더 경로
#os.chdir(path) # 해당 폴더로 이동
files = os.listdir(path) # 해당 폴더에 있는 파일 이름을 리스트 형태로 받음


model = load_model('keras_model.h5',compile = False)


for file in files:
    start = time.time()
    if '.png' in file:
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        size = (224, 224)
        image = Image.open('C:/Users/yoonhong/Desktop/maple_macro/keras_sample/{}'.format(file))
        
        img_x, img_y = image.size
        image_size = int(img_x / 7)
        kill_num = 0
        for length in range(image_size):
            cut_image = image.crop((7*(image_size-1-length),0,7*(image_size-length),8))
            cut_image = ImageOps.fit(cut_image, size, Image.BILINEAR)


            image_array = np.asarray(cut_image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array

            # run the inference
            prediction = model.predict(data)

            temp_list = []
            for i in range(11):
                temp_list.append(prediction[0][i])
                
            tmp = max(temp_list)
            index = temp_list.index(tmp)
            if index != 10:
                kill_num = kill_num + (index*10**length)
        print(kill_num)
    end = time.time()
    print(end-start)
