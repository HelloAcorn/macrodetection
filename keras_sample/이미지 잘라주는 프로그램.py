import cv2

src = cv2.imread("1642351439.png", cv2.IMREAD_COLOR)

cv2.imshow("sad",src)
src_y = src.shape[0]
src_x = src.shape[1]

temp = int(src_x / 7)


for a in range(temp):
    print(a)
    dst = src[0:8, a*7:a*7+7].copy()
    cv2.imwrite('{}.png'.format(a),dst)
