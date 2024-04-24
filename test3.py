import keyboard
import time
import os
import glob

path = '/so/path/to/file'
for filename in glob.glob(os.path.join(path, '*.txt')):
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
      # do your stuff



"""
test = open("depo.txt", "r").read().strip().split("~")
textset
for s in textset







print(textset)



tindex = 0

def wrap(s, w):
    return [s[i:i + w] for i in range(0, len(s), w)]


#splitting up the document into the right lines
for text in textlistoflists in set
for w in textlistoflists:
    textlistoflists[tindex] = w.strip()
    textlistoflists[tindex] = wrap(textlistoflists[tindex], 8)
    tindex += 1

print(textlistoflists)
"""




