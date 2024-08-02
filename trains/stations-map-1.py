
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as crs
import requests
import json
import os
from os import path
from datetime import datetime, timedelta

jsonfile = "stations.json"

days_ago = datetime.now () - timedelta (days=1)
if (not os.path.isfile (jsonfile) or 
    datetime.fromtimestamp(path.getctime(jsonfile)) < days_ago):
  rs1 = (
    "https://rata.digitraffic.fi/api/v1" +
    "/metadata/stations")
  response = requests.get (rs1)
  data = response.json ()
  print (f"Read {rs1}")
  json_string = json.dumps (data)
  f = open (jsonfile,"w")
  f.write (json_string)
  f.close ()
  print (f"Wrote {jsonfile}")

f = open (jsonfile)
data = json.load (f)
f.close()
print (f"Read {jsonfile}")

stations = data
print ("Stations:",len (stations))
print (stations[0].keys())
print (stations[0].values())

lats,lons,names = [],[],[]
for x in stations:
  if x ['countryCode'] == "FI":
    names.append (x ["stationShortCode"])
    lats.append (x ["latitude"])
    lons.append (x ["longitude"])

fig = plt.figure (figsize=(5.8,9.2))
fig.set_layout_engine (layout="tight")
ax = plt.axes (projection=
  crs.Orthographic(
    central_longitude=24.0, 
    central_latitude=62.0, 
    globe=None))

ax.add_feature (cartopy.feature.COASTLINE)
plt.scatter (
  x=lons, y=lats,
  color="indianred",
  s=10,
  alpha=1.0,
  transform=crs.PlateCarree())

for i, (x, y) in enumerate (list (zip(lons, lats))):
  plt.text (
    x, y, 
    "  " + names [i],
    backgroundcolor = (1,1,1,0),
    verticalalignment="center_baseline",
    fontsize=6,
    transform=crs.PlateCarree()
  )
plt.show() ; plt.close()





