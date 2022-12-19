from PIL import Image
 
image1 = Image.open('C:/Users/yoonhong/Desktop/maple_macro/keras_sample/1642360165.png')


iz, ix = image1.size

image1.crop((0,0,7,8))
print("asd")
