"""
Python package `psssodls` generates Minion 3 input files
for pandiagonal strongly symmetric self-orthogonal diagonal
latin squares (PSSSODLS).
"""

import sys

from math import sqrt

from psssodls.constraints import alldiff, sdk_positions_box
from psssodls.constraints import psumg, pandiagonal_sum_a, psuml, pandiagonal_sum_b
from psssodls.constraints import ell, ellell

def begin(n):
  return """\
MINION 3

**VARIABLES**
DISCRETE l[{},{}] {{0..{}}}

**SEARCH**
PRINT ALL

**CONSTRAINTS**

""".format(n, n, n - 1)

def end():
  return "**EOF**"

def latin_constraints_str(n):
  """Returns a string containing the latin constraints for a square of size
  n."""
  s = '# Latin constraints. \n\n'
  s += "".join([alldiff([i,'_']) + '\n' + alldiff(['_',i]) + '\n' for i in range(n)])
  return s + '\n'

def box_constraints_str(n):
  p = int(sqrt(n))
  F = [sdk_positions_box(i,j,p) for i in range(1, p + 1) for j in range(1, p + 1)]
  s = '# Box constraints. \n\n'
  for p in F:
    s += 'alldiff([' + ",".join(ell(q) for q in p) + '])' + '\n'
  return s + '\n'

def pandiagonality_constraints_str(n):
  """Returns a string containing the pandiagonality constraints for a square
  of size n."""
  s = '# Pandiagonality constraints. \n\n'
  for w in range(n):
    s += psumg(n, w, pandiagonal_sum_a)
    s += psuml(n, w, pandiagonal_sum_a)
    s += psumg(n, w, pandiagonal_sum_b)
    s += psuml(n, w, pandiagonal_sum_b)
    s += '\n'
  return s

def strongly_symmetric_constraints_str(n):
  s = '# Strongly symmetric constraints. \n\n'
  for i in range(n):
    for j in range(n):
      s += 'sumgeq({}, {})\n'.format(ellell([[i,j],[n - 1 - i, n - 1 - j]]), n - 1)
      s += 'sumleq({}, {})\n'.format(ellell([[i,j],[n - 1 - i, n - 1 - j]]), n - 1)
    s += '\n'
  return s

def orthogonality_constraints_str(n):
  """Returns a string containing the orthogonality constraints for a square
  of size n."""
  F = [[(i,j), (j,i)] for i in range(n) for j in range(n)]
  s = '# Orthogonality constraints. \n\n'
  s += "".join([vecneq(p, q) + '\n' for p in F for q in F if p > q])
  return s + '\n'

def psssodls_string(n, boxes):
  """Returns a string which is the entire Minion 3 format constraint program
  for PSSSODLS(n)."""
  s = begin(n)
  s += latin_constraints_str(n)
  if boxes:
    s += box_constraints_str(n)
  s += pandiagonality_constraints_str(n)
  s += strongly_symmetric_constraints_str(n)
  s += orthogonality_constraints_str(n)
  s += end()
  return s