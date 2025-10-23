import numpy as np
import cv2
import sys

file = open("frame_001444_jpg.rf.09dca83cce9c56019653154b1e4403e3.txt", "r")
content = file.readlines()
satir = content[0]
bilgiler = satir.strip().split()
print(bilgiler)
print(content)


file = open("frame_013712_jpg.rf.7979fb5b2d945d3483bffd0dafef89f2.txt", "r")
content = file.readlines()

x_min, x_max, y_min, y_max = 0,0,0,0

left, top, right, bottom = 0,0,0,0

def yolo_to_pixel(bbox, image_width=1920, image_height=1080):
    for bilgi in content:
        print(bilgi)
        bilgi = bilgi.strip().split()
        print(bilgi)
        left, top, right, bottom = float(bilgi[1]), float(bilgi[2]), float(bilgi[3]), float(bilgi[4])
        cx *= image_width
        cy *= image_height
        w *= image_width
        h *= image_height

        x1 = int(cx - w / 2)
        y1 = int(cy - h / 2)
        x2 = int(cx + w / 2)
        y2 = int(cy + h / 2)

        return x_min, y_min, x_max, y_max



np.set_printoptions(threshold=sys.maxsize,linewidth=sys.maxsize)
img = cv2.imread("1.jpg")
x_min, y_min, x_max, y_max=yolo_to_pixel()
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kordinata_gore = gray_img[y_max:y_min, x_max:x_min]
(thresh,blackandwhite) = cv2.threshold(kordinata_gore,127,255,cv2.THRESH_BINARY)

print(blackandwhite.shape[0])

top_index_list=[]
for i in range(0,blackandwhite.shape[1]):
    row_i = 0
    #print(i)
    for out_value in blackandwhite[:,i]:
        #print(out_value)
        total_in_values = 0
        if out_value == 255:

            for in_value in blackandwhite[row_i:row_i+5,i]:
                if in_value==255:
                    total_in_values+=1

        if total_in_values > 4:
            top_index_list.append([row_i, i])
            break

        row_i+=1

down_index_list = []
for i in range(0, blackandwhite.shape[1]):
    row_i = 143
    # print(i)
    for out_value in blackandwhite[::-1, i]:
        # print(out_value)
        total_in_values = 0
        if out_value == 255:
            for in_value in blackandwhite[row_i-5:row_i, i]:
                if in_value == 255:
                    total_in_values += 1

        if total_in_values > 4:
            down_index_list.append([row_i, i])
            break

        row_i -= 1

zipped_indexes=zip(top_index_list,down_index_list)

total_white=0
total_black=0
total_pixels=0
for top,down in zipped_indexes:
    for value in blackandwhite[top[0]:down[0],top[1]]:
        if value == 255:
            total_white+=1
        if value == 0:
            total_black+=1

        total_pixels+=1

print("Normalde toplam pixel sayısı",blackandwhite.shape[0]*blackandwhite.shape[1])
print("Gerekli index işlemlerinden sonra pixel sayısı",total_pixels)
print(total_pixels,total_white,total_black)
print("Toplam siyah pixelin toplam pixele oranı",total_black/total_pixels)

#cv2.imwrite("1_jpg_siyah_beyaz.jpg",blackandwhite)

window_name = "image"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

cv2.imshow("image", blackandwhite)
cv2.waitKey(0)
cv2.destroyAllWindows()
