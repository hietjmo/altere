
from collections import defaultdict


tau_digits = ''.join(c for c in ("""
6.
2831853071 7958647692 5286766559 0057683943 3879875021 
1641949889 1846156328 1257241799 7256069650 6842341359 
6429617302 6564613294 1876892191 0116446345 0718816256 
9622349005 6820540387 7042211119 2892458979 0986076392 
8857621951 3318668922 5695129646 7573566330 5424038182 
9129713384 6920697220 9086532964 2678721452 0498282547 
4491740132 1263117634 9763041841 9256585081 8343072873 
5785180720 0226610610 9764093304 2768293903 8830232188 
6611454073 1519183906 1843722347 6386522358 6210237096 
1489247599 2549913470 3771505449 7824558763 6602389825
""") if c in "1234567890")

abc = (
  "ABCDEFGH"  
  "JKLMNPQR"
  "STUVWXYZ"
  "abcdefgh"
  "jklmnpqr"
  "stuvwxyz"
  "αβγδεζηθ"
  "ικλμνξπρ"
)

def letter (x,y):
  return abc [8*y+x]

def pos (c):
  x = abc.index (c)
  y,x = divmod (x,8)
  return x,y

f = open ("fullabys-2.txt")
content = f.read ()
f.close ()
lines = content.split ("\n")
names = [s for s in lines if len(s) > 2]

dsums = []
for s in names:
  d1 = {}
  rows = defaultdict (list)
  cols = defaultdict (list)
  # print ("\n".join (s [8*y:8*(y+1)] for y in range(8)))
  for i,c in enumerate(s):
    x,y = pos (c)
    t = tau_digits [i]
    d1 [x,y] = int (t)
  for y in range (8):
    for x in range (8):
      rows [y].append (d1 [x,y])
      cols [x].append (d1 [x,y])
  d1 = sum ([sum ([(1 if a==b else 0) for a,b in zip (cols[x][0:],cols[x][1:])]) for x in cols])
  d2 = sum ([sum ([(1 if a==b else 0) for a,b in zip (rows[y][0:],rows[y][1:])]) for y in rows])
  dsum = d1 + d2
  dsums.append (dsum)
  print (F"{s} {dsum}")
  #print (rows,cols,d1+d2)
print (len(dsums),min(dsums),max(dsums))

