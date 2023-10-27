
# always-look-on-the-bright-stars-of-sky.py
# python bright-stars-of-sky-2.py > hip_cons_692.txt

from math import tau
import re

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

"""
print (brights)
# [677, 746, 765, 1067, 1562, 1599, 1645, 2021, ...]
print (len(brights))
# 692
"""

filename = "hip_main.dat"
d = {}
with open (filename) as f:
  for line in f:
    xs = re.split (r" *\| *",line.strip())
    hipnum = int (xs[1])
    if hipnum in brights:
      ra  = float (xs[8])
      dec = float (xs[9])
      mag = float (xs[5].strip())
      d[hipnum] = ra,dec,mag

for k,v in d.items():
  print (k,v[0],v[1],v[2])


"""
Hipparcos   CDS Name    HEASARC Name       Description
Cat. Field

--          * New *    Name               /Catalog Designation
H0          Catalog    * Not Displayed *  /Catalogue (H=Hipparcos)
H1          HIP        HIP_Number         /Identifier (HIP number)
H2          Proxy      Prox_10asec        /Proximity flag
H3          RAhms      RA                 /RA in h m s, ICRS (J1991.25)
H4          DEdms      Dec                /Dec in deg ' ", ICRS (J1991.25)
H5          Vmag       Vmag               /Magnitude in Johnson V
H6          VarFlag    Var_Flag           /Coarse variability flag
H7          r_Vmag     Vmag_Source        /Source of magnitude
H8          RAdeg      RA_Deg             /RA in degrees (ICRS, Epoch-J1991.25)
H9          DEdeg      Dec_Deg            /Dec in degrees (ICRS, Epoch-J1991.25)

H|           1| |00 00 00.22|+01 05 20.4| 9.10| |H|000.00091185|+01.08901332| 

RA is the abbreviation for Right Ascension and dec is the abbreviation for declination. They are similar to latitude and longitude, but they relate to coordinates in the sky.
Mag stands for magnitude, which is the brightness of the star. The limiting brightness of stars seen with the naked eye is about magnitude 6.5. With binoculars, you can see to magnitudes of about 10. For magnitudes beyond that, using an amateur telescope is recommended.
"""

