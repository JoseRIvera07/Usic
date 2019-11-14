import os
import serial
import urllib.parse as urlparse
from tkinter import *
import winsound
import pygame
from PIL import Image, ImageTk
from threading import Thread

playList = ['track1.mp3', 'track2.mp3', 'track3.mp3']
currentSong = 0
paused = True

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(playList[currentSong])
pygame.mixer.music.play(0)
pygame.mixer.music.pause()


def onPressedBtn1():
    global paused, currentSong, playList
    currentSong = currentSong - 1
    if currentSong < 0:
        currentSong = len(playList) - 1
    pygame.mixer.music.load(playList[currentSong])
    pygame.mixer.music.play(0)
    paused = False
    
def onPressedBtn2():
    global paused
    if paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.play(0)
        fisrtPlay = False
    paused = False

def onPressedBtn3():
    global paused
    pygame.mixer.music.pause()
    paused = True

def onPressedBtn4():
    global paused, currentSong, playList
    currentSong = currentSong + 1
    if currentSong == len(playList):
        currentSong = 0
    pygame.mixer.music.load(playList[currentSong])
    pygame.mixer.music.play(0)
    paused = False

window = Tk()
window.title("Reproductor Inteligente")
window.resizable(width=NO, height=NO)
window.minsize(width=580, height=480)
window.configure(background='#f5f7fa')

load = Image.open("logo.png")
load = load.resize((200, 200), Image.ANTIALIAS)
render = ImageTk.PhotoImage(load)
img = Label(window, image=render)
img.image = render
img.place(x=195, y=40, width=200, height=200)

btn1 = Button(window, text="<<", command=onPressedBtn1, background = '#cf1766', foreground = "#ffffff" )
btn1.place(x=100, y=280, width=80, height=40)

btn2 = Button(window, text=">", command=onPressedBtn2, background = '#cf1766', foreground = "#ffffff" )
btn2.place(x=200, y=280, width=80, height=40)

btn3 = Button(window, text="||", command=onPressedBtn3, background = '#cf1766', foreground = "#ffffff" )
btn3.place(x=300, y=280, width=80, height=40)

btn4 = Button(window, text=">>", command=onPressedBtn4, background = '#cf1766', foreground = "#ffffff" )
btn4.place(x=400, y=280, width=80, height=40)

def sensor():
    global paused
    ser = serial.Serial('com4', baudrate=9600, timeout=1) 
    while True:
        tex = ser.readline()
        print(tex)
        if tex != None:
            if tex== b'p':
                if paused:
                    onPressedBtn2()
                else:
                    onPressedBtn3()
            elif tex== b'a':
                onPressedBtn1()
            elif tex== b'n':
                onPressedBtn4()
            else:
                None
control=Thread(target=sensor,args=())
control.start()
#window.mainloop()

#control=Thread(target=sensor,args=())
#control.start()
