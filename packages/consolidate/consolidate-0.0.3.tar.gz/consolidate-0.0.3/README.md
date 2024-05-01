# consolidate-py
A Python library for generating a list of strings with every possible combination of placements of a given character (or a zero-width non joiner by default) within another given string, up to a given maximum length of characters.
## What you could use this for
This module was built to allow for the generation of inputs when duplicate inputs aren't allowed. <br><br>
I used this in my Kahoot spam bot to allow for me to (for educational purposes, obviously) generate the same username for my bots, because Kahoot doesn't allow duplicate names, and 20 "SpanishInquisition"s are a lot cooler than than "SpanishInquisition7923", "SpanishInquisition8213", etc.
## Syntax:
Import module by typing ```from consolidate.consolidatemodule import generate``` in your Python program file<br><br>
Run the generate function with ```generate(string baseString, int maxCharacterLength (default 6, can't be less than baseString's length), string fillerString (default is a zero width non-joiner U+200C ) )```
## Example usage:
print(generate("python", 8, "X")) <br><br>
&#62; ["python", "Xpython", "XXpython", "pXython", "XpXython", "pyXthon", "XpyXthon", ... ]
## Supporting consolidate.py:
Please feel free to modify the code to add functionalities you want to!
<br> Something I'm missing is the ability to use strings to fill instead of a single character... it compl