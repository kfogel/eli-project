import tkinter as tk
import tkinter.font as TkFont
import random
import os
import sys
import time
import keyboard
import playsound

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
            s[idxp][idxl] = wrap(l.strip(), 4)
            for idxstring, string in enumerate(s[idxp][idxl]):
                s[idxp][idxl][idxstring] = string.strip()
    return s

# sys.stderr.write(f"DEBUG: whole depo: {textprocess(depo)}\n")

class TextSource:
    """A source of properly broken-up text."""
    def __init__(self, text):
        "See the textprocess() documentation for the format of TEXT."
        self.text = text
        self.cur_section = 0  # current section we're in
        self.cur_para = 0     # current paragraph within current section
        self.cur_fragment = 0 # current word fragment within current para 
        # Was the previous fragment the last one before a paragraph
        # and/or section break?
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
        ret = [self.text[self.cur_section][self.cur_para][self.cur_fragment],
               self.para_break, self.section_break,]
        self.cur_fragment += 1
        # Test if we're at any boundaries and need to cycle around.
        if self.cur_fragment == len(self.text[self.cur_section][self.cur_para]):
            self.cur_fragment = 0
            self.cur_para += 1
            self.para_break = True
            if self.cur_para == len(self.text[self.cur_section]):
                self.cur_para = 0
                self.cur_section += 1
                self.section_break = True
                if self.cur_section == len(self.text):
                    self.cur_section = 0
            else:
                self.section_break = False
        else:
            self.para_break = False
        return ret

depo_text = TextSource(textprocess(open("depo.txt", "r").read().strip()))

root = tk.Tk()
root.configure(bg="black")
# root.attributes('-fullscreen', True)  # make main window full-screen
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

def playclick():
    soundfilenumbers = [1, 4, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,]
    soundfile = f"click{random.choice(soundfilenumbers)}.wav"
    playsound.playsound(soundfile)

def keypressed(ignored_event):
    global x
    global y
    global delay
    global letter
    global battery
    global lastPress
    global timeBetween
    global depo_text

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

    this_fragment = depo_text.next_fragment()
    playclick()

    if this_fragment[2]:
        y += 32  # end of section
    elif this_fragment[1]:
        y += 16  # end of paragraph
    
    # TODO: We need to increment "x" by the appropriate length for the
    # text we write here (this_fragment[0]).  How to do that?  Not
    # sure yet.
    canvas_text = canvas.create_text(x, y,
                                     text=this_fragment[0],
                                     anchor="nw", 
                                     fill="white", 
                                     font=goodFont)

    # I didn't really understand all the delay and battery stuff, so I
    # didn't include it, but I left these lines here from before in
    # case you need to refer to them:
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
