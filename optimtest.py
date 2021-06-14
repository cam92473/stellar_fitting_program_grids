from scipy.optimize import minimize
import torch
from torch.autograd.functional import jacobian,hessian
from torch import tensor
import xarray as xr
import numpy as np

'''da = np.array([[1,2,3],[4,5,6],[7,8,9]])
interpolated = da.interp(Ab)'''

xdata = [-3.6,-2.5,-1,0.5,1,1.25]

ydata = [0,-2.5,-2,-4.5,1,4]

erry = [0.02,0.02,0.01,0.03,0.01,0.02]

def testfunc(tup,other1,other2):
    a,b,c,d,f = tup
    suckup = other1
    
    model = [a*x**4+b*x**3+c*x**2+d*x+f for x in xdata]

    chisq = sum([([ydata[point]-model[point] for point in range(6)][i])**2/(erry[i])**2 for i in range(6)])

    print(type(chisq))
    return chisq


x0 = torch.Tensor([0.4,2.3,3.1,-1.2,-4.6])

#print(jacobian(testfunc,x0))

#print(hessian(testfunc,x0))


def jack(x0,other1,other2):
    other1 = torch.Tensor(other1)
    other2 = torch.Tensor(other2)
    t_x0 = torch.from_numpy(x0)
    return jacobian(testfunc,(t_x0,other1,other2,))[0]


def jill(x0,other1,other2):
    other1 = torch.Tensor(other1)
    other2 = torch.Tensor(other2)
    t_x0 = torch.from_numpy(x0)
    return hessian(testfunc,(t_x0,other1,other2,))[0][0]

other1 = [5,6]
other2 = 10

result = minimize(testfunc, x0, method="dogleg", jac = jack, hess = jill, args = (other1,other2,))

print(result)

import matplotlib.pyplot as plt

plt.scatter(xdata,ydata)
plt.scatter(xdata, [result.x[0]*x**4+result.x[1]*x**3+result.x[2]*x**2+result.x[3]*x+result.x[4] for x in xdata])

plt.show()