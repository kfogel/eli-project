# Goal of the program

* A simple black and white GUI that progressively types out
  predetermined words according to random keyboard input, as well as
  plays preloaded audio samples

* Key presses are cumulative (up to a point) and a large "battery" of
  key presses makes the letters typed out very fast.  when another
  letter is printed to the canvas.

* Paragraphs will be separated by keys "#" and "~" or any other
  identifier, with the # symbol representing a new paragraph, and "~"
  meaning a pause and need to hold enter to continue.

# Main issues

* Can't figure out how to pause and keep everything on screen with a
  "hold enter" prompt.

* I either want the screen to scroll downward, or reset after every
  set of paragraphs (between the hold enter prompts)

* I tried two audio libraries but I can't figure out how to load the
  files into the program.

* The program sometimes slows down after a lot of words are on screen,
  don't know why

# Low priority

* Blinking cursor at the typehead

* Ability to put images on the canvas on the right side at a given
  point in the text

* More dynamic typing where the time between keypresses determines the
  speed of the words being displayed
