import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

#케라스 모델 데이터를 훈련모델/테스트모델로 불러옴
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

#파라미터의 영향을 보기 위해 랜덤값 고정
tf.random.set_seed(1234)

#데이터 정규화
x_train, x_test = x_train / 255.0, x_test / 255.0

#데이터 reshape
x_train = x_train.reshape(-1,28,28,1)
x_test = x_test.reshape(-1,28,28,1)

#one-hot 인코딩
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)


#모델 생성
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(kernel_size=(3,3), filters=64,
                           input_shape=(28,28,1), padding = 'same', activation='relu'),
    tf.keras.layers.Conv2D(kernel_size=(3,3), filters=64,
                           padding = 'same', activation='relu'),
    tf.keras.layers.MaxPool2D(pool_size=(2,2)),
    
    tf.keras.layers.Conv2D(kernel_size=(3,3), filters=128,
                           padding = 'same', activation='relu'),
    tf.keras.layers.Conv2D(kernel_size=(3,3), filters=256,
                           padding = 'valid', activation='relu'),
    tf.keras.layers.MaxPool2D(pool_size=(2,2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(units=512, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(units=256, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(units=10, activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer=tf.optimizers.Adam(lr=0.001), metrics=['accuracy'])
model.summary()
model.fit(x_train, y_train, batch_size=100, epochs=10, validation_data=(x_test, y_test))

result = model.evaluate(x_test, y_test)
print("result: ",result)

image = cv.imread('2.png', cv.IMREAD_GRAYSCALE)
image = cv.resize(image, (28, 28))
image = image.astype('float32')
image = image.reshape(1, 784)
image = 255-image
image /= 255.0

pred = model.predict(image.reshape(1, 784), batch_size=1)
print("추정된 숫자=", pred.argmax())


plt.show()
