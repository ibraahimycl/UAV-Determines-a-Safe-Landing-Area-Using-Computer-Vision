import numpy as np
import cv2
import json

img = cv2.imread("resim5.jpg")
b,g,r= cv2.split(img)
red_img = r
print(red_img.shape)


kordinata_gore = red_img[470:620,744:896]
kordinata_gore = cv2.resize(kordinata_gore, (640,680))
cv2.imshow("black and white", kordinata_gore)
cv2.waitKey(0)


print(kordinata_gore.shape) 

x1 = 0
x2 = kordinata_gore.shape[1]
y1 = 0
y2 = kordinata_gore.shape[0]
piksel_sayisi = (x2 - x1) * (y2 - y1)
p = 0

dictionary = {}



for y in range(y1,y2):
    for x in range(x1,x2):
        if kordinata_gore[y,x] < 140:
            kordinata_gore[y,x] = 0
        else:
            kordinata_gore[y,x] = 255

for y in range(y1,y2):
    for x in range(x1,x2):
        dictionary[f"{p}.piksel"] = kordinata_gore[y,x].tolist()
        p += 1

kordinata_gore = cv2.resize(kordinata_gore, (640,680))
cv2.imshow("0-255",kordinata_gore)
cv2.waitKey(0)
cv2.destroyAllWindows()


ortalama = sum(dictionary.values()) / len(dictionary)
print(f"ortalama: {ortalama}")


with open("output3kırmızıkanalinsanvar.json", "w") as dosya:
    json.dump(dictionary, dosya, indent=4)
    
siyahl = []
beyazl = []
threshold = 80
for value in dictionary.values():
    if value == 0:
        siyahl.append(value)
    else:
        beyazl.append(value)

total = len(siyahl) + len(beyazl)
ratio_s = (len(siyahl) / total) * 100
ratio_b = (len(beyazl) / total) * 100
print(f"ratio_siyah: {ratio_s} ----- ratio_beyaz: {ratio_b}")

#döngü başlat sözlük içinde değerleri al aldıkça herbirini ortalamadan çıkar mutlak al len(dictionary.values())
toplam_std = 0
for i in dictionary.values():
    sapma = ortalama - i
    toplam_std += abs(sapma)
    
std = toplam_std / len(dictionary)
print("standart sapma: ", std)

cv2.imwrite("kırmızıkanal.jpg", kordinata_gore)