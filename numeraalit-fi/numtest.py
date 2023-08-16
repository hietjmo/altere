
import numeraalit as num
import readline

while True:
  n = input ("Numero: ")
  n = n.replace (" ","")
  try:
    n = int (n)
  except:
    break
  print (f"{n:_}".replace("_", " "), f'"{num.numeraali (n)}"')

