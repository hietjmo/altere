
ykkoset = ["", "yksi", "kaksi", "kolme", "neljä",
  "viisi", "kuusi", "seitsemän", "kahdeksan", "yhdeksän" ]

def from1to19 (n):
  d = n % 100
  i = n % 10
  result = ''
  if n == 0:
    result = 'nolla'
  if 1 <= i <= 9:
    result = ykkoset [i] 
  if d == 10:
    result = 'kymmenen'
  if 11 <= d <= 19:
    result = ykkoset [i] + 'toista'
  return result

def kymmenet1 (n):
  d = n % 100 // 10
  result = ''
  if 2 <= d <= 9:
    result = ykkoset [d] + 'kymmentä'
  return result

def sadat1 (n):
  c = n % 1000 // 100
  result = ''
  if c == 1:
    result = 'sata'
  if c > 1:
    result = ykkoset [c] + 'sataa'
  return result

def from1to999 (n):
  i = from1to19 (n)
  d = kymmenet1 (n)
  c = sadat1 (n)
  return c + d + i

def tuhatta (n):
  result = ''
  m = n % 1_000_000 // 1_000
  i = from1to19 (m)
  d = kymmenet1 (m)
  c = sadat1 (m)
  if m == 1:
    result = 'tuhat '
  if m >= 2:
    result = c + d + i + 'tuhatta '
  return result

def miljoonaa (n):
  result = ''
  m = n % 1_000_000_000 // 1_000_000
  i = from1to19 (m)
  d = kymmenet1 (m)
  c = sadat1 (m)
  if m == 1:
    result = 'miljoona '
  if m >= 2:
    result = c + d + i + 'miljoonaa '
  return result

def numeraali (n):
  result = ''
  if 0 <= n <= 999_999_999:
    result = miljoonaa (n) + tuhatta (n) + from1to999 (n)
  return result.strip ()



