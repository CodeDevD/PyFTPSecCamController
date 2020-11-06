import requests
import time
import numpy as np
import cv2
import pygame
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ftplib import FTP

aufnahmen = set([])
def firststep(aufnahmen):
    time.sleep(1)
    doc = BeautifulSoup(r.text, "html.parser")
    htmlaufnahmen = doc.select("a")
    for htmlaufnahme in htmlaufnahmen:
        aufnahmen.add(htmlaufnahme)

    if len(aufnahmen) > 30:
        ftp = FTP("IP_ADRESSE")
        ftp.login("NAME", "PASSWORT")
        ftp.cwd("/www/IPCamera") #example

        listaufnahmen = list(aufnahmen)
        listaufnahmen.reverse()
        for alteaufnahme in listaufnahmen:
            if len(listaufnahmen) > 12:
                try:
                    ftp.delete(alteaufnahme.text)
                    listaufnahmen.remove(alteaufnahme)
                except:
                    print("Error:  " + str(alteaufnahme.text) + "   konnte nicht gelöscht werden")
            else:
                break
        aufnahmen = set(listaufnahmen)

def is_internet_on(r):
    if str(r) == "<Response [200]>":
        return True
    else:
        return False

while True:
    url = "URL"
    r = requests.get(url)
    if is_internet_on(r) == True:
        firststep(aufnahmen)
        break
    else:
        print(r)

while True:
    if is_internet_on == False:
        continue
    r = requests.get(url)
    time.sleep(1)
    doc = BeautifulSoup(r.text, "html.parser")

    htmlaufnahmen = doc.select("a")
    if len(htmlaufnahmen) > len(aufnahmen):
        for htmlaufnahme in htmlaufnahmen:
            if htmlaufnahme in aufnahmen:
                pass
            else:
                aufnahme = htmlaufnahme
                aufnahmen.add(aufnahme)
                print("Neue Aufnahme:         " + str(aufnahme.text))
                gaufnahme = urljoin(url, aufnahme.text)
                video = requests.get(gaufnahme, stream = True)
                open('aufnahme.avi', 'wb').write(video.content)
                cap = cv2.VideoCapture('aufnahme.avi')
                while(cap.isOpened()):
                    ret, frame = cap.read()
                    if ret == True:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        classifier = cv2.CascadeClassifier("./haarcascade_fullbody.xml")
                        bodys = classifier.detectMultiScale(gray, minNeighbors=2)
                        c = frame.copy()
                        if len(bodys) != 0:
                            pygame.init()
                            pygame.mixer.music.load("WARN_SOUND.mp3")
                            pygame.mixer.music.play()
                        for body in bodys:
                            x, y, w, h = body
                            cv2.rectangle(c, (x, y),(x + w, y + h),(0, 0, 255),5)
                        cv2.imshow('c', c)
                        # & 0xFF is required for a 64-bit system
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    else:
                        break
                cap.release()
                cv2.destroyAllWindows()




