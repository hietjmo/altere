
# python clipboard.py

import tkinter

win = tkinter.Tk ()
selection = "CLIPBOARD"
# selection = "PRIMARY"

class S ():
  def __init__ (self):
    self.clipboard = win.selection_get (selection=selection)
    self.old_clipboard = self.clipboard 
  def check_clipboard (self):
    self.clipboard = win.selection_get (selection=selection)
    if self.clipboard != self.old_clipboard:
      print (self.clipboard)
      self.old_clipboard = self.clipboard
    win.after (100, self.check_clipboard)

self = S ()
win.title (selection)
win.after (100, self.check_clipboard)
win.mainloop ()

# Just use
# :!chmod +x %

