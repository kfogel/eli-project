import keyboard
import time
import os
import glob

set = open("depo.txt", "r").read().strip().split("#")
tindex = 0


def wrap(s, w):
   return [s[i:i + w] for i in range(0, len(s), w)]


# splitting up the document into the right lines


for paragraphs in set:
   paragraphs = paragraphs.split("~")

"""

for w in set:
   set[tindex] = w.strip()
   set[tindex] = wrap(set[tindex], 91)
   tindex += 1

"""
print(paragraphs)






