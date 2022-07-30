import numpy as np

gbound1lo = 3.5
gbound1hi = 5
g1num = 5
Tbound1lo = .35
Tbound1hi = 3.1
T1num = 5
Zbound1lo = -2.5
Zbound1hi = .5
Z1num = 5
ebvbound1lo = .07
ebvbound1hi = 1
ebv1num = 5

a = np.linspace(gbound1lo,gbound1hi,g1num)
b = np.linspace(Tbound1lo,Tbound1hi,T1num)
c = np.linspace(Zbound1lo,Zbound1hi,Z1num)
d = np.linspace(ebvbound1lo,ebvbound1hi,ebv1num)

e,f,g,h = np.meshgrid(a,b,c,d)


print(a)
print(b)
print(c)
print(d)

print("######################")
print(e)
print("######################")
print(f)
print("######################")
print(g)
print("######################")
print(h)
print("######################")

print(e[1,4,2,0])
print(f[1,4,2,0])
print(g[1,4,2,0])
print(h[1,4,2,0])