from numpy.lib.function_base import interp
from scipy.optimize import minimize
import torch
from torch.autograd.functional import jacobian,hessian
from torch import tensor
import numpy as np
import xarray as xr

def interpolate(gra):
    print("gra",gra)
    da = xr.DataArray(np.array([[1,2,3],[4,5,6],[7,8,9]]),[("g",[1.0,1.5,2.0]),("T",[5000,5250,5500])])
    print("interpolated ", da.interp(g=gra,T=5376).data.item())
    return da.interp(g=gra,T=5376).data.item()


def simp(x,t_a,t_b):
    print("a ", t_a)
    print("b ",t_b)
    if not isinstance(t_b,int):
        print("b long ",t_b.long())
        print(print("b long item",t_b.long().item()))
    print("a[1]", t_a[1])
    aint = [int(i) for i in t_a]
    print("aint ",aint)
    alist = [4,5,6]
    print(alist[aint[1]])

    ecks = x[0]
    print(ecks)
    wie = x[1]
    print(wie)

    interped = interpolate(ecks.item())
    print("interped",interped)
    print(type(interped))

    sumlist = []
    
    for i in range(1):
        sumlist.append(ecks**2+wie*interped)

    return sum(sumlist)

x0 = torch.tensor([1.8,3])
a = [1,2,3]
b = 2

#print(simp(x0,a))

#print(jacobian(simp,(x0,a,)))

def jack(x0,a,b):

    t_x0 = torch.from_numpy(x0)
    t_a = torch.tensor([float(i) for i in a])
    t_b = torch.tensor(float(b))
    print("##JACKSTART##")
    print(t_a[2])
    print(t_b.item())
    print("##JACKEND##")
    return jacobian(simp,(t_x0,t_a,t_b,))[0]

def jill(x0,a,b):

    print("##HESSSTART##")
    t_x0 = torch.from_numpy(x0)
    t_a = torch.tensor([float(i) for i in a])
    t_b = torch.tensor(float(b))
    print("##HESSEND##")
    return hessian(simp,(t_x0,t_a,t_b,))[0][0]

result = minimize(simp, x0, method="dogleg", jac = jack, hess = jill, args = (a,b,))

print(result)