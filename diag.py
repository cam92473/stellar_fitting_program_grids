import numpy as np

a = np.array([[ 8.60939347e+01, -4.05579491e+03, -6.06923567e+02, -1.97391925e+02,
1.87814823e+03, -5.14950468e+03, -5.41462710e+01,  9.44780234e+02],
 [-4.05579491e+03,  1.93269919e+05,  2.89218947e+04,  9.40751376e+03,
  -8.95642941e+04,  2.45443398e+05,  2.58061077e+03, -4.50362617e+04,],
 [-6.06923567e+02,  2.89218947e+04,  4.32904819e+03,  1.40778614e+03,
  -1.34037091e+04,  3.67298911e+04,  3.86166462e+02, -6.73962838e+03],
 [-1.97391925e+02,  9.40751376e+03,  1.40778614e+03,  4.58290030e+02,
  -4.36169551e+03,  1.19486253e+04,  1.25144382e+02, -2.19264347e+03],
 [ 1.87814823e+03, -8.95642941e+04, -1.34037091e+04, -4.36169551e+03,
   4.15997100e+04, -1.13818461e+05, -1.19488175e+03,  2.08928455e+04],
 [-5.14950468e+03,  2.45443398e+05,  3.67298911e+04,  1.19486253e+04,
  -1.13818461e+05,  3.11766039e+05,  3.27696000e+03, -5.72122541e+04],
 [-5.41462710e+01,  2.58061077e+03,  3.86166462e+02,  1.25144382e+02,
  -1.19488175e+03,  3.27696000e+03,  3.51174652e+01, -6.01171754e+02],
 [ 9.44780234e+02, -4.50362617e+04, -6.73962838e+03, -2.19264347e+03,
   2.08928455e+04, -5.72122541e+04, -6.01171754e+02,  1.05008132e+04]])

print(a)

print(np.diag(a))