import tkinter as tk
import tkinter.font as TkFont
import random
import os
import sys
import time
import threading
import keyboard
import playsound

text = open("depo.txt", "r")
text = text.read()
text = text.strip()
textlistoflists = text.split("~")
tindex = 0

root = tk.Tk()
root.configure(bg="black")
root.attributes('-fullscreen', True)  # make main window full-screen
canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.pack(fill=tk.BOTH, expand=True)
delay = 0
lastPress = float(0)
timeBetween = float(0)
battery = 0
goodFont = TkFont.Font(family="Courier", size=12, weight="bold")
x = 10
y = 10
letter = 0
write = True
###################
soundfilenumbers = [1, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,]

def playclick():
    soundfile = f"click{random.choice(soundfilenumbers)}.wav"
    playsound.playsound(soundfile)

def keypressed():
    global battery
    global lastPress
    global timeBetween
    timeBetween = round(time.time() - lastPress, 2)
    lastPress = round(time.time(), 2)
    battery += 4


def onKeyPress(event):
    keypressed()
    #print(f"battery level: {battery}")


def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]


#splitting up the document into the right lines
for w in textlistoflists:
    textlistoflists[tindex] = w.strip()
    textlistoflists[tindex] = wrap(textlistoflists[tindex], 91)
    tindex += 1


def mainloop():
    global x
    global y
    global root
    global delay
    global battery
    global letter
    for paragraph in textlistoflists:
        for line in paragraph:
            canvas_text = canvas.create_text(x, y, text="", anchor="nw", fill="white", font=goodFont)
            for l in range(len(line) + 1):
                while battery < 1:
                    event1 = keyboard.read_event()
                    if event1.event_type == keyboard.KEY_DOWN:
                        keypressed()
                canvas.after(delay, lambda c=canvas_text, s=line[0:l]: canvas.itemconfigure(c, text=s))
                #playclick()
                delay += random.randint(20, 60)
                battery -= 1
            y += 16
        #end of paragraph
        y += 32



t1 = threading.Thread(target=mainloop).start()

root.bind('<KeyPress>', onKeyPress)
root.mainloop()
