
import numerales as num

parte = 0
f = open (f"parte-{parte:02}.txt","w")
for i in range (1,1_000_001):
  texto = f"{num.numeral (i)}, \n"
  if i % 50000 == 0:
    texto = f"{num.numeral (i)}. \n"
  if i == 1_000_000:
    texto = f"million. \n"
  if i % 50000 == 1:
    texto = f"{num.numeral (i)}, \n".capitalize ()
    # f.write (f"Fin del parte {parte:02}.\n")
    parte = parte + 1
    if i != 1_000_000:
      f.close ()
      f = open (f"partes/parte-{parte:02}.txt","w")
  f.write (texto)
f.close()

