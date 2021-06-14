from scipy import optimize
def f(x,a):
    b = a
    return (x**3 - 1)  # only one real root at x = 1

def fprime(x):
    return 3*x**2

a = 2
sol = optimize.root_scalar(f, args=(a,),bracket=[0, 3], method='brentq')

print(sol.root)