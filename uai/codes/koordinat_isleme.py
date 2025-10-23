etiketler = {}
etiketler[0] = [1, 0.023958333333333335, 0.3287037037037037, 0.04791666666666667, 0.06481481481481481]
etiketler[1] = [2, 0.6708333333333333, 0.05694444444444444, 0.06666666666666667, 0.09351851851851851]
etiketler[2] = [3, 0.440625, 0.5296296296296297, 0.078125, 0.13148148148148148]
etiketler[3] = [0, 0.4296875, 0.5212962962962963, 0.0125, 0.03148148148148148]
etiketler[4] = [0, 0.6424479166666667, 0.2125, 0.019270833333333334, 0.019444444444444445]

flag = 0
class_box = {}
i = 0
j = 0

for key, value in etiketler.items():
    class_id = value[0]
    left, top, right, bottom = value[1], value[2], value[3], value[4]
    x1 = left * 1920 - (right * 1920) / 2
    x2 = left * 1920 + (right * 1920) / 2
    y1 = top * 1080 - (bottom * 1080) / 2
    y2 = top * 1080 + (bottom * 1080) / 2

    # uap ve uai'nin class_id'leri 2 ve 3 olduğunu kabul ediyoruz
    if class_id == 2:
        class_box[f'uai{i}'] = [x1, x2, y1, y2]
        flag = 1
        i+=1

    if class_id == 3:
        class_box[f'uap{j}'] = [x1, x2, y1, y2]
        flag = 1
        j+=1

flag2=0
if flag == 1:
    print("frame içinde uap veya uai bulunuyor ve şimdi uygunluk kontrol edilecektir")
    for key, value in etiketler.items():
        class_id = value[0]
        if class_id == 0 or class_id == 1:
            left, top, right, bottom = value[1], value[2], value[3], value[4]
            x1 = left * 1920 - (right * 1920) / 2
            x2 = left * 1920 + (right * 1920) / 2
            y1 = top * 1080 - (bottom * 1080) / 2
            y2 = top * 1080 + (bottom * 1080) / 2

            for nesne, koordinatlar in class_box.items():
                #print(nesne, koordinatlar)
                if 'uap' in nesne:
                    print(x1,x2,y1,y2)
                    #print("uap bulunuyor ve kontrol ediliyor")
                    if ((x1 >= koordinatlar[0] and x2 <= koordinatlar[1]) and (y1 >= koordinatlar[2] and y2 <= koordinatlar[3])) or ((
                            (koordinatlar[0] <=x1 <= koordinatlar[1]) or (koordinatlar[0] <= x2 <= koordinatlar[1])) and (
                            (koordinatlar[2] <= y1 <= koordinatlar[3]) or (koordinatlar[2] <= y2 <= koordinatlar[3]))):
                        print("uap iniş alanı uygun değil")
                        print(flag2)
                        flag2 = 1
                elif 'uai' in nesne:
                    print(x1,x2,y1,y2)

                    #print("uai bulunuyor ve kontrol ediliyor")
                    if ((x1 >= koordinatlar[0] and x2 <= koordinatlar[1]) and (y1 >= koordinatlar[2] and y2 <= koordinatlar[3])) or ((
                            (koordinatlar[0] <=x1 <= koordinatlar[1]) or (koordinatlar[0] <= x2 <= koordinatlar[1])) and (
                            (koordinatlar[2] <= y1 <= koordinatlar[3]) or (koordinatlar[2] <= y2 <= koordinatlar[3]))):
                        print("uai iniş alanı uygun değil")
                        print(flag2)
                        flag2 = 1
        else:
            continue


print(flag2)