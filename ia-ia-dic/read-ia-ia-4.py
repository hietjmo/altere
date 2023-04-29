
# python read-ia-ia-4.py --debug 1 --out ia-ia-wordlist.txt
# time= 4.245722055435181 s
# n= 502534 words


import re
import time
from sortedcontainers import SortedSet
from collections import defaultdict
from itertools import product
from random import randint
import argparse
import builtins

t0 = time.time ()

def read_args ():
  parser = argparse.ArgumentParser()
  pad = parser.add_argument
  pad('wds',nargs='*')
  pad('-x',type=int,default=0)
  pad('-n',type=int,default=0)
  pad('--debug',type=int,default=0)
  pad('-o','--out')
  pad('-dic','--dicfile',default="ia-ia.dic")
  pad('-aff','--affile',default="ia-ia.aff")
  args = parser.parse_args ()
  return (args)

args = read_args()

def print (level,*args1, **kwargs1):
  if args.debug >= int (level):
    builtins.print (*args1, **kwargs1)

def from_affile ():
  f = open (args.affile)
  content = f.readlines ()
  f.close ()
  
  aff_list = [ s.strip() 
    for s in content if len(s)>1 and not s.startswith ("#")]
  
  pfx = defaultdict (list)
  sfx = defaultdict (list)
  rep = defaultdict (list)
  
  for s in aff_list:
    d = re.split(r"\s+", s)
    if len (d) > 2 and d[2][0] not in ['Y','N']:
      if d[0] == "PFX":
        pfx[d[1]].append (d[2:])
      if d[0] == "SFX":
        sfx[d[1]].append (d[2:])
      if d[0] == "REP":
        rep[d[1]].append (d[2:])

  return pfx,sfx,rep

def from_dicfile ():
  f = open (args.dicfile)
  content = f.readlines ()
  f.close ()
  return [s.strip() for s in content][1:]

def substrs (s):
  return [s[i: j] for i in range(len(s))
          for j in range(i + 1, len(s) + 1)]

def collect_prefixes (d,pfx):
  result = [()]
  for gd in substrs(d[1]):
    if gd in pfx:
      for a,b,c in pfx [gd]:
        m = re.match (F"{c}",d[0])
        if m:
          result.append ((a,b,c))
  return result

def collect_suffixes (d,sfx):
  result = [()]
  for gd in substrs(d[1]):
    if gd in sfx:
      for a,b,c in sfx [gd]:
        m = re.search (F"{c}$",d[0]) 
        if m:
          result.append ((a,b,c))
  return result

def gen_prod (d,cfp,csf):
  result = []
  for pf,sf in product (cfp,csf):
    nw = d[0]
    if pf:
      a,b,c = pf
      if a == '0':
        nw = b + d[0]
      else:
        nw = b + re.sub ("^"+a,"",d[0])
    if sf:
      a,b,c = sf
      if a == '0':
        nw = nw + b
      else:
        nw = re.sub (a+"$","",nw) + b
    if nw not in result:
      result.append (nw)
  return result

def generate_from (s):
  d = s.split (r"/")
  gp=[d[0]]
  if len (d) == 2:
    print (5,"s,d[0],d[1]=",s,d[0],d[1])
    cfp = collect_prefixes (d,pfx)
    print (5,"cfp=",cfp)
    csf = collect_suffixes (d,sfx)
    print (5,"csf=",csf)
    for new in gen_prod (d,cfp,csf):
      if new not in gp:
        gp.append (new)
    print (5,"gp=",gp)
  return gp

pfx,sfx,rep = from_affile ()
wds = from_dicfile ()

print (6,"\npfx=",pfx)
print (6,"\nsfx=",sfx)
print (6,"\nrep=",rep)

def derivates (s):
  rts = generate_from (s)
  rts1 = rts[:]
  rtsz = []
  
  for rt in rts1:
    if "/" in rt:
      for s in generate_from (rt):
        rtsz.append (s)
        d = s.split (r"/")
        if d[0] not in rts:
          rts.append (d[0])
  
  rts2 = []
  for s in rts:
    rtsz.append (s)

    d = s.split (r"/")
    if d[0] not in rts2:
      rts2.append (d[0])
  
  print (3,"rts2=",rts2)
  print (4,"rtsz=",rtsz)

  return rts2

result = SortedSet()

print (3,"args=",args)

if args.n > 0:
  for i in range (0,args.n):
    argsn = randint(0,len(wds)-1)
    s = wds [argsn]
    ds = derivates (s)
    for item in ds:
      result.add (item)

if args.n == 0 and args.x == 0 and args.wds == []:
  for s in wds:
    ds = derivates (s)
    for item in ds:
      result.add (item)

if args.x > 0:
  s = wds[args.x]
  ds = derivates (s)
  for item in ds:
    result.add (item)

for s in args.wds:
  ds = derivates (s)
  for item in ds:
    result.add (item)

if args.out:
  f = open (args.out,"w")
  for item in result:
    f.write (item + "\n")
  f.close ()
else:
  for item in result:
    print (0,item)


t1 = time.time ()
print (1,"time=",t1-t0,"s")
print (1,"n=",len (result),"words")


