
import random
import time
import argparse

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('files', nargs='*')
  pad ("-n1", "--num1", type=int, default=100_000)
  pad ("-n2", "--num2", type=int, default=2_000_000)
  pad ("-n3", "--num3", type=int, default=500)
  pad ("-all","--print_all", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

litteras = "eaionstlrucdmpvbghfqxjykzw"
litlist = list (litteras)
litlist.reverse ()

f = open ("parolas-total.txt")
content = f.read ()
f.close ()

pars1 = content.split ("\n")
pars2 = []
for p2 in pars1:
  p = p2.split ("\t")
  if len (p) == 2:
    a,b = p
    pars2.append ((a,int(b)))
pars3 = {a:b for a,b in pars2}

d = {c: [] for c in litlist}
sumd = {c: 0 for c in litlist}

for w in pars2:
  s = set (w[0])
  for c in s:
    if c in d:
      d [c].append (w)
      sumd [c] += w[1]

ps = {}
for c in litlist:
  lst = []
  for w in d[c]:
    lst.append ((w[0],w[1]/sumd [c]))
  ps [c] = lst

print ("".join (litlist))

def rrand (samp):
  i = 0
  fnd = None
  r = random.random ()
  cum = 0.0
  while not fnd:
    p = samp [i][1]
    cum = cum + p
    if cum > r:
      fnd = samp [i]
    i = i + 1
    if i >= len (samp):
      i = 0
  return fnd [0]

def newwds ():
  notdone = litlist.copy ()
  wd1 = []
  done = []
  while notdone:
    samp1 = ps [notdone[0]]
    s1 = rrand (samp1)
    wd1.append (s1)
    notdone = [c for c in notdone if c not in s1]
  return wd1

def sum_pars3 (phrase):
  wds = phrase.split (" ")
  return -sum ([pars3[w] for w in wds])

foxfile = "le-rapide-brun-vulpe-ia.txt"
try:
  f = open (foxfile)
  content = f.read ()
  f.close ()
  rs = content.split ("\n")
  rs = rs[1:]
except:
  rs = []

time1 = time.time ()
i = 0

while True:
  newds1 = newwds ()
  if args.print_all:
    print (newds1)
  newds2 = " ".join (newds1)
  rs.append (newds2)
  i = i + 1
  if i % args.num3 == 0:
    rs = list (set (rs))
    rs.sort (key=lambda x: (len (x), sum_pars3(x)))
    rs = rs[:args.num3]
  if i % args.num1 == 0:
    time2 = time.time ()
    dt1 = time2-time1
    time1 = time.time ()
    print (f"{i} {dt1:.4f}")
  if i % args.num2 == 0:
    f = open (foxfile,"w")
    f.write ("".join (litlist)+"\n")
    f.write ("\n".join(rs))
    f.close ()
    print (f"Wrote {foxfile}.")

# :cd %:h
# wzkyjxqfhgbvpmdcurltsnoiae
