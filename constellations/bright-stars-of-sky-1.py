
# always-look-on-the-bright-stars-of-sky.py

filename = "constellationship.fab"
f = open (filename)
lines = f.readlines ()
f.close ()

s1 = [s.strip().split() for s in lines if len(s)>5]
s2 = {x[0]:[int(a) for a in x[2:]] for x in s1}

brights = set()
for k,v in s2.items():
  for t in v:
    brights.add (t)

brights = sorted (list (brights))

print (brights)
# [677, 746, 765, 1067, 1562, 1599, 1645, 2021, ...]
print (len(brights))
# 692

