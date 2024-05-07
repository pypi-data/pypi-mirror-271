def ell(p):
  """This function takes a pair p = [p[0], p[1]] and returns the string
  'l[p[0],p[1]]'."""
  return 'l[{},{}]'.format(p[0], p[1])

def ellell(p):
  return '[{},{}]'.format(ell(p[0]),ell(p[1]))

def alldiff(p):
  """Returns a string representing an all_different constraint over the
  variables in the vector v."""
  return 'alldiff({})'.format(ell(p))

def vecneq(p, q):
  """Returns a string representing an vectorised inequality constraint between
  the two vectors p and q."""
  return 'watchvecneq({}, {})'.format(ellell(p), ellell(q))

def sdk_positions_box(i,j,p):
  row_offset = p * (i-1)
  column_offset = p * (j-1)
  return [(row_offset + r, column_offset + c) for r in range(p) for c in range(p)]

def pandiagonal_sum_a(n, w):
  return ",".join([ell([i % n, (i + w) % n]) for i in range(n)])

def pandiagonal_sum_b(n, w):
  return ",".join([ell([i % n, (w - i) % n]) for i in range(n)])

def sumgeq(x, y):
  return 'sumgeq([{}],{})\n'.format(x, y)

def sumleq(x, y):
  return 'sumleq([{}],{})\n'.format(x, y)

def psumg(n, w, f):
  return sumgeq(f(n, w), str(int(n*(n - 1)/2)))

def psuml(n, w, f):
  return sumleq(f(n, w), str(int(n*(n - 1)/2)))
