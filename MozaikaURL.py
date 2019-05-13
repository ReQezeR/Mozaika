from bottle import route, run, template, request, static_file
from urllib.request import urlopen
import numpy as np
import random
import math
import cv2
import re


#  w podlistach mozliwosc ustalenia rozkładu mozaiki dla max 8 obrazów
def rozmieszczenie(): return [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2], [3, 2], [3, 3], [4, 3], [4, 4]]

def newSize(img, r1, nr_wiersza, flagaY):  # (obraz, obrazow_w_wierszu, nr_wiersza,flagaY)
    wynik = [int(math.floor(img.shape[0] / nr_wiersza)), int(math.floor(img.shape[1] / r1))]  # [Y, X]
    if flagaY is True and img.shape[0] % wynik[0] is 1:  # Y
        wynik[0] = wynik[0] + 1
    return wynik  # [Y, X]

'''Funkcja pobierajaca obraz'''
def url_to_image(url):  # download the image, convert it to a NumPy array, and then read it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

'''Funkcja losująca kolejność'''
def losuj(ileURL):
    result_list = []
    while(1):
        los = random.sample(range(1, ileURL+1), 1)
        x = los[0]
        if x not in result_list: result_list.append(los[0])
        if len(result_list) >= ileURL: break
    return result_list

'''Funkcja zwracajaca gotowy obraz'''
@route('/mozaika')
def send_image1():
    Z = int(request.query.losowo)
    resolution = request.query.rozdzielczosc or '2048x2048'
    resolution = re.split("x", resolution)
    X = int(resolution[0])
    Y = int(resolution[1])
    URL = request.query.zdjecia

    if len(URL) > 0:
        URL = re.split(",", URL)
        ileURL = int(request.query.ile or len(URL))

        if 0 < ileURL <= 8:
            r = rozmieszczenie()
            img = np.zeros((Y, X, 3), np.uint8)
            img[:] = 0

            if r[ileURL][0] is not 0 or r[ileURL][1] is not 0:
                lista = losuj(len(URL))
                r1 = r[ileURL][0]  # liczba zdjec w wierszu 1
                r2 = r[ileURL][1]  # liczba zdjec w wierszu 2

                '''Petla scalajaca obrazy'''
                for x in range(ileURL):
                    if Z == 1:
                        temp_url = URL[lista[x] - 1]  # losowe pobranie URL
                    else:
                        temp_url = URL[x]  # pobranie URL
                    temp_img = url_to_image(temp_url)  # pobranie obrazu
                    '''Obsluga pierwszego wiersza'''
                    if r[ileURL][0] >= x+1:
                        pX = int(math.floor(X / r1) * x)
                        kX = int(math.floor(X / r1) * (x+1))
                        pY = 0
                        if r[ileURL][1] is 0:
                            kY = Y
                            w = 1
                        else:
                            kY = int(math.floor(Y / 2))
                            w = 2
                        nXY = newSize(img, r1, w, False)  # kalkulacja wymiarow obrazu
                        temp_img = cv2.resize(temp_img, (0, 0), fx=nXY[1]/temp_img.shape[1], fy=nXY[0]/temp_img.shape[0], interpolation=cv2.INTER_LANCZOS4)
                        img[pY:kY, pX:kX] = temp_img[:]  # wstawienie obrazu
                    '''Obsluga drugiego wiersza'''
                    if r[ileURL][0] < x+1:
                        nXY = newSize(img, r2, 2, True)  # kalkulacja wymiarow obrazu
                        temp_img = cv2.resize(temp_img, (0, 0), fx=nXY[1] / temp_img.shape[1],fy=nXY[0] / temp_img.shape[0], interpolation=cv2.INTER_LANCZOS4)
                        pX = int((nXY[1] * (x-r1)))
                        kX = int((nXY[1] * (x-r1 + 1)))
                        pY = int(nXY[0]-1)
                        kY = Y
                        img[pY:kY, pX:kX] = temp_img[:]  # wstawienie obrazu
            cv2.imwrite('kolaz.jpg', img)
            cv2.imwrite('D:\\localhost\\kolaz.jpg', img)
            return static_file('kolaz.jpg', root='//Awionetka/localhost')  # odeslanie gotowego obrazu
        else: return template("Zła liczba obrazów")
    else: print("BRAK ZDJEC")


if __name__ == "__main__":
    run(host='localhost', port=8080)