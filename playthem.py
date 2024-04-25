import time
import os
import playsound

for i in range(1, 22):
    soundfile = f"click{i}.wav"
    if os.path.exists(soundfile):
        print(f"Playing {soundfile}...")
        playsound.playsound(soundfile)
        print("Done.")
        print("")
    time.sleep(1)
