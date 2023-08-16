
import numeraalit as num
import shutil
import os

def crear (path):
  if os.path.exists (path) and os.path.isdir (path):
    shutil.rmtree (path)
  os.mkdir (path)

path = "osat"
crear (path)

lenny = 0
osa = 0
f = None
for i in range (1,1_000_001):
  text = f"{num.numeraali (i)}, \n"
  if i % 50000 == 0:
    text = text.replace (",",".")
  if i % 50000 == 1:
    text = text.capitalize ()
    osa = osa + 1
    if i != 1_000_000:
      if f: 
        f.close ()
      f = open (f"{path}/osa-{osa:02}.txt","w")
  f.write (text)
  lenny = lenny + len (text) - 1
f.close()
print (lenny,"merkkiä.")

"""
64225009 merkkiä.

real	0m3,900s
user	0m3,735s
sys	0m0,085s
"""


