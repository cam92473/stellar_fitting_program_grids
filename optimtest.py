from scipy.optimize import minimize


xdata = [-3.6,-2.5,-1,0.5,1,1.25]

ydata = [0,-2.5,-2,-4.5,1,4]

erry = [0.02,0.02,0.01,0.03,0.01,0.02]

def testfunc(tup):
    a,b,c,d,f = tup

    model = [a*x**4+b*x**3+c*x**2+d*x+f for x in xdata]

    chisq = sum([([ydata[point]-model[point] for point in range(6)][i])**2/(erry[i])**2 for i in range(6)])

    return chisq

import numpy as np

x0 = np.array([0.4,2.3,3.1,-1.2,-4.6])

result = minimize(testfunc, x0)

print(result)

import matplotlib.pyplot as plt

plt.scatter(xdata,ydata)
plt.scatter(xdata, [result.x[0]*x**4+result.x[1]*x**3+result.x[2]*x**2+result.x[3]*x+result.x[4] for x in xdata])

plt.show()

import math
print(np.sqrt(np.diag(result.hess_inv)))