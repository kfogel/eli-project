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
os.getcwd()
"""
click1 = AudioSegment.from_mp3("click1.mp3")
click2 = AudioSegment.from_mp3("click2.mp3")
click3 = AudioSegment.from_mp3("click3.mp3")
click4 = AudioSegment.from_mp3("click4.mp3")
click5 = AudioSegment.from_mp3("click5.mp3")
click6 = AudioSegment.from_mp3("click6.mp3")
click7 = AudioSegment.from_mp3("click7.mp3")
click8 = AudioSegment.from_mp3("click8.mp3")
click9 = AudioSegment.from_mp3("click9.mp3")
click10 = AudioSegment.from_mp3("click10.mp3")
click11 = AudioSegment.from_mp3("click11.mp3")
click12 = AudioSegment.from_mp3("click12.mp3")
click13 = AudioSegment.from_mp3("click13.mp3")
click14 = AudioSegment.from_mp3("click14.mp3")
click15 = AudioSegment.from_mp3("click15.mp3")
click16 = AudioSegment.from_mp3("click16.mp3")
click17 = AudioSegment.from_mp3("click17.mp3")
click18 = AudioSegment.from_mp3("click18.mp3")
click19 = AudioSegment.from_mp3("click19.mp3")
click20 = AudioSegment.from_mp3("click20.mp3")
click21 = AudioSegment.from_mp3("click21.mp3")
"""

def playclick(i):
    #if i == 1:
    #   playsound.playsound("click1", False)
    """
    elif i == 2:
        play(click2)
    elif i == 3:
        play(click3)
    elif i == 4:
        play(click4)
    elif i == 5:
        play(click5)
    elif i == 6:
        play(click6)
    elif i == 7:
        play(click7)
    elif i == 8:
        play(click8)
    elif i == 9:
        play(click9)
    elif i == 10:
        play(click10)
    elif i == 11:
        play(click11)
    elif i == 12:
        play(click12)
    elif i == 13:
        play(click13)
    elif i == 14:
        play(click14)
    elif i == 15:
        play(click15)
    elif i == 16:
        play(click16)
    elif i == 17:
        play(click17)
    elif i == 18:
        play(click18)
    elif i == 19:
        play(click19)
    elif i == 20:
        play(click20)
    else:
        play(click21)
        """

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
                #playclick(random.randint(1, 21))
                delay += random.randint(20, 60)
                battery -= 1
            y += 16
        y += 32


t1 = threading.Thread(target=mainloop).start()

root.bind('<KeyPress>', onKeyPress)
root.mainloop()
