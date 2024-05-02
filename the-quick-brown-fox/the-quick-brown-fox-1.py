
import random
import time

# print_all = True
print_all = False
litteras = "eaionstlrucdmpvbghfqxjykzw"
litlist = list (litteras)
litlist.reverse ()

f = open ("par-total-1.txt")
content = f.read ()
f.close ()

wds = content.split ("\n")

d = {c: [] for c in litlist}

for w in wds:
  s = set (w)
  for c in s:
    if c in d:
      d [c].append (w)

print ("".join (litlist))

def rrand (samp):
  wts = [x+1 for x in list (range (len(samp)))]
  wts.reverse ()
  i = 0
  fnd = None
  r = random.random ()
  cum = 0.0
  while not fnd:
    p = wts [i] / sum (wts)
    cum = cum + p
    if cum > r:
      fnd = samp[i]
    i = i + 1
    if i >= len (samp):
      i = 0
  return fnd

def newwds ():
  notdone = litlist.copy ()
  wd1 = []
  done = []
  while notdone:
    samp = d [notdone[0]]
    s1 = rrand (samp)
    wd1.append (s1)
    notdone = [c for c in notdone if c not in s1]
  return wd1

foxfile = "the-quick-brown-fox-ia.txt"
f = open (foxfile)
content = f.read ()
f.close ()
rs = content.split ("\n")

time1 = time.time ()
i = 0

while True:
  newds = " ".join (newwds ())
  if print_all:
    print (newds)
  rs.append (newds)
  rs.sort (key=len)
  rs = rs[:500]
  i = i + 1
  if i % 50 == 0:
    time2 = time.time ()
    dt1 = time2-time1
    time1 = time.time ()
    print (f"{i} {dt1:.4f}")
  if i % 10000 == 0:
    f = open (foxfile,"w")
    f.write ("\n".join(rs))
    f.close ()
    print (f"Wrote {foxfile}.")

