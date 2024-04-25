import keyboard
import time
import os
import glob

depo = open("depo.txt", "r").read().strip()

def wrap(s, w):
   return [s[i:i + w] for i in range(0, len(s), w)]

def textprocess(d):
    s = d.split("#")
    for idxp, p in enumerate(s):
        s[idxp] = p.strip().split("~")
        for idxl, l in enumerate(s[idxp]):
            s[idxp][idxl] = wrap(l.strip(), 4)
            for idxstring, string in enumerate(s[idxp][idxl]):
                s[idxp][idxl][idxstring] = string.strip()
    return s

print(f"whole depo: {textprocess(depo)}")



