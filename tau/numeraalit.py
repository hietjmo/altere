
unes = [ '', 'yksi', 'kaksi', 'kolme', 'neljä', 'viisi', 
 'kuusi', 'seitsemän', 'kahdeksan', 'yhdeksän' ]

def milliardos (n):
  m = n % 1_000_000_000_000 // 1_000_000_000
  result = ''
  if m == 1:
    result = 'miljardi'
  if m > 1:
    result = from1to999 (m) + 'miljardia'
  return result

def milliones (n):
  m = n % 1_000_000_000 // 1_000_000
  result = ''
  if m == 1:
    result = 'miljoona'
  if m > 1:
    result = from1to999 (m) + 'miljoonaa'
  return result

def milles (n):
  m = n % 1_000_000 // 1_000
  result = ''
  if m == 1:
    result = 'tuhat'
  if m > 1:
    result = from1to999 (m) + 'tuhatta'
  return result

def centos (n):
  c = n % 1000 // 100
  result = ''
  if c == 1:
    result = 'sata'
  if c > 1:
    result = unes [c] + 'sataa'
  return result

def deces (n):
  d = n % 100 // 10
  i = n % 10
  result = ''
  if d == 1 and i == 0:
    result = 'kymmenen'
  if d == 1 and i > 0:
    result = unes [i] + "toista"
  if d > 1:
    result = unes [d] + 'kymmentä'
  return result

def unes1 (n):
  i = n % 10
  d = n % 100 // 10
  result = ''
  if n == 0: 
    result = 'nolla'
  elif i > 0 and d != 1:
    result = unes [i]
  return result

def join_numwds (a,b,sep=" "):
  result = ''
  if a and b:
    result = a + sep + b
  elif a:
    result = a
  elif b:
    result = b
  return result

def from1to999 (n):
  c = centos (n)
  d = deces (n)
  u = unes1 (n)
  w1 = join_numwds (d,u,"")
  w2 = join_numwds (c,w1,"")
  return w2

def numeraali (n):
  mmm = milliardos (n)
  mm = milliones (n)
  m = milles (n)
  c = from1to999 (n)
  w1 = join_numwds (m,c)
  w2 = join_numwds (mm,w1)
  w3 = join_numwds (mmm,w2)

  return w3
