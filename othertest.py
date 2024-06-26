import tkinter as tk
import tkinter.font as TkFont
from tkinter import ttk
import random
import os
import sys
import time
import playsound
import threading
import PIL
from PIL import Image, ImageTk


def wrap(s, w):
   return [s[i:i + w] for i in range(0, len(s), w)]

def textprocess(f):
    """Return the contents of file handle F in nested-list form:

    [ [['Sect', 'ion', '1 pa', 'ragr', 'aph', '1'], 
       ['Sect', 'ion', '1 pa', 'ragr', 'aph', '2'], ... ],
      [['Sect', 'ion', '2 pa', 'ragr', 'aph', '1'],
       ['Sect', 'ion', '2 pa', 'ragr', 'aph', '2'], ... ],
      ... 
    ]
    """
    s = f.split("#")
    for idxp, p in enumerate(s):
        s[idxp] = p.strip().split("~")
        for idxl, l in enumerate(s[idxp]):
            s[idxp][idxl] = wrap(l.strip(), 59)
            for idxf, f in enumerate(s[idxp][idxl]):
                s[idxp][idxl][idxf] = wrap(f.strip(), random.randint(2, 4))
                for idxi, i in enumerate(s[idxp][idxl][idxf]):
                    s[idxp][idxl][idxf][idxi] = i.strip("\n")
    return s

# sys.stderr.write(f"DEBUG: whole depo: {textprocess(depo)}\n")

class TextSource:
    """A source of properly broken-up text."""
    def __init__(self, text):
        "See the textprocess() documentation for the format of TEXT."
        self.text = text
        self.cur_section = 0  # current section we're in
        self.cur_para = 0   # current paragraph within current section
        self.cur_line = 0
        self.cur_fragment = 0 # current word fragment within current para 
        # Was the previous fragment the last one before a paragraph
        # and/or section break?
        self.line_break = False
        self.para_break = False
        self.section_break = False
    def next_fragment(self):
        """Yield the next text fragment, plus line break or paragraph break.
        Wrap around to the beginning of self.text as needed.

        The return value is a list of three elements:

          [text_fragment, paragraph_break, section_break]

        The first element (text_fragment) is always a string.

        The second element (paragraph_break) is always either False or
        True.  If it's True, the consumer should print a paragraph
        break before printing the text_fragment.

        The third element (section_break) is always either False or
        True.  If it's True, the consumer should print a section break
        before printing the text_fragment (the consumer may, at its
        discretion, not print a paragraph break when there's a section
        break to print anyway -- that's about how the consumer wants
        to display things).
        """
        ret = [self.text[self.cur_section][self.cur_para][self.cur_line][self.cur_fragment],
               self.line_break,
               self.para_break,
               self.section_break,]
        self.cur_fragment += 1
        # Test if we're at any boundaries and need to cycle around.
        if self.cur_fragment == len(self.text[self.cur_section][self.cur_para][self.cur_line]):
            self.cur_fragment = 0
            self.cur_line += 1
            self.line_break = True
            if self.cur_line == len(self.text[self.cur_section][self.cur_para]):
                self.cur_line = 0
                self.cur_para += 1
                self.para_break = True
                if self.cur_para == len(self.text[self.cur_section]):
                    self.cur_para = 0
                    self.cur_section += 1
                    self.section_break = True
                    if self.cur_section == len(self.text):
                        self.cur_section = 0
                        print("sequence done")
                else:
                    self.section_break = False
            else:
                self.para_break = False
                self.section_break = False
        else:
            self.line_break = False
            self.para_break = False
            self.section_break = False
        #print(f"Current section: {self.cur_section}")
        #print(f"CurrentPara: {self.cur_para}")
        #print(f"CurrentFragment: {self.cur_fragment}")
        return ret

depo_text = TextSource(textprocess(open("depo.txt", "r", encoding="utf8").read().strip()))
root = tk.Tk()
root.configure(bg="black")
root.attributes('-fullscreen', True)  # make main window full-screen
canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.pack(fill=tk.BOTH, expand=True)
delay = 0
lastPress = float(0)
timeBetween = float(0)
battery = 0
goodFont = TkFont.Font(family="Courier", size=16) #weight="bold"
orig_x = 12
x = orig_x
orig_y = 12
y = orig_y
letter = 0
write = True
carryFragment = str("")
pictureTime = True
###################


def playenter():
    playsound.playsound("entersound.wav")
def playpicture():
    threading.Thread(target=playsound.playsound, args=("picturesound.wav",), daemon=True).start()
def playclick():
    soundfilenumbers = [1, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38,]
    soundfile = f"click{random.choice(soundfilenumbers)}.wav"
    # We used to just call playsound.playsound() directly, like this:
    # 
    # playsound.playsound(soundfile)
    # 
    # But that meant it was called synchronously: the whole program
    # had to wait until the sounds finishes playing.  This meant that
    # the user experienced delay, as the program couldn't keep up with
    # their typing.  So instead we play the sound in its own separate
    # thread.  Now the playing happens in the background -- in other
    # words, this playclick() function actually exits before the sound
    # has played, and control returns to the caller, so we can go back
    # to the regular event loop and handle the next keypress while
    # this sound is in the process of playing in a separate thread.
    threading.Thread(target=playsound.playsound, args=(soundfile,), daemon=True).start()

def keypressed(event):
    global orig_x
    global orig_y
    global x
    global y
    global delay
    global letter
    global battery
    global lastPress
    global timeBetween
    global depo_text
    global write
    global carryFragment
    global pictureTime

    # Uncomment these to get console debugging prints:
    # 
    # sys.stdout.write(f"{this_fragment[0]}")
    # sys.stdout.flush()
    # if this_fragment[1]: # paragraph break
    #     sys.stdout.write("\n\n")
    #     sys.stdout.flush()
    # if this_fragment[2]: # section break
    #     sys.stdout.write("\n-----------------\n\n")
    #     sys.stdout.flush()

    # TODO: You could put the code below in a loop that iterates a
    # random numbetr (N) of times, and thus fetches N text fragments in
    # turn and displays each one, putting paragraph breaks and section
    # breathteaks as necessary.
    this_fragment = depo_text.next_fragment()

    if write is False and event.keysym == "Return":
        playenter()
        write = True
        this_fragment[0] = carryFragment
        depo_text.cur_para = 0
        depo_text.cur_line = 0
        depo_text.cur_fragment = 1
        canvas.delete("all")
        x = orig_x
        y = orig_y

    if write:
        if this_fragment[3]:
            y += 70  # start a new section
            x = orig_x
            enter_text = canvas.create_text(x, y, text="Press ENTER To Continue>", anchor="nw", fill="white", font=goodFont)
            write = False
            carryFragment = this_fragment[0]
        elif this_fragment[2]:
            y += 46  # start a new paragraph
            x = orig_x
        elif this_fragment[1]:
            y += 21  # start a new line
            x = orig_x

    if write:
        canvas_text = canvas.create_text(x, y,
                                         text=this_fragment[0],
                                         anchor="nw",
                                         fill="white",
                                         font=goodFont)
        playclick()
        text_bbox = canvas.bbox(canvas_text)
        x += (text_bbox[2] - text_bbox[0])
    if pictureTime:
        if "0" in this_fragment[0]:
            canvas.p0 = ImageTk.PhotoImage(Image.open("intropic.png").resize((420, 750)))
            canvas.create_image(850, 10, image=canvas.p0, anchor='nw')
            playpicture()
        elif "1" in this_fragment[0]:
            canvas.p1 = ImageTk.PhotoImage(Image.open("cathedral.png").resize((420, 450)))
            canvas.create_image(850, 10, image=canvas.p1, anchor='nw')
            playpicture()
        elif "2" in this_fragment[0]:
            canvas.p2 = ImageTk.PhotoImage(Image.open("longyou.png").resize((420, 300)))
            canvas.create_image(850, 490, image=canvas.p2, anchor='nw')
            playpicture()
        elif "3" in this_fragment[0]:
            canvas.p3 = ImageTk.PhotoImage(Image.open("mosque.png").resize((420, 460)))
            canvas.create_image(850, 10, image=canvas.p3, anchor='nw')
            playpicture()
        elif "4" in this_fragment[0]:
            canvas.p4 = ImageTk.PhotoImage(Image.open("amphitheater.png").resize((420, 280)))
            canvas.create_image(850, 480, image=canvas.p4, anchor='nw')
            playpicture()
        elif "5" in this_fragment[0]:
            canvas.p5 = ImageTk.PhotoImage(Image.open("resonancepic.PNG").resize((800, 410)))
            canvas.create_image(240, 375, image=canvas.p5, anchor='nw')
            playpicture()
        elif "9" in this_fragment[0]:
            pictureTime = False





    #elif event.keysym == "Return":
    #    canvas.delete("all")
    #    x = orig_x
    #    y = orig_y
    #    write = True



# I didn't know how you want all the delay and battery stuff to
    # work, so I didn't use it, but I left these lines here from
    # before in case you need to refer to them:
    # 
    # canvas.after(delay, lambda c=canvas_text, s=line[0:l]: canvas.itemconfigure(c, text=s))
    # delay += random.randint(20, 60)
    # y += 16
    # end of paragraph
    # y += 32
    # timeBetween = round(time.time() - lastPress, 2)
    # lastPress = round(time.time(), 2)
    # battery += 4
root.bind('<KeyPress>', keypressed)
root.mainloop()


