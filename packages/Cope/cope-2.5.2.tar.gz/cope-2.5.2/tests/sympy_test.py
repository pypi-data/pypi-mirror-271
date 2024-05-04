from Cope.sympy import *
from sympy import Symbol, sqrt

def test_catagorize():
    x = Symbol('x')
    assert categorize(x**2) == ['polynomial', 'rational', 'quadratic', 'power'], categorize(x**2)
    assert categorize(sqrt(x)) == ['root', 'power'], categorize(sqrt(x))
    assert categorize(x**3) == ['polynomial', 'rational', 'power'], categorize(x**3)
    assert categorize(sqrt(3*x + 1)) == [], categorize(sqrt(3*x + 1))
    assert categorize(x**3 - 3*x + 2) == ['polynomial', 'rational'], categorize(x**3 - 3*x + 2)
    assert categorize((x - 1)**2) == ['polynomial', 'rational', 'quadratic'], categorize((x - 1)**2)
    assert categorize((2*x + 3)/(x**2 + 1)) == ['rational'], categorize((2*x + 3)/(x**2 + 1))
    assert categorize(5**x) == ['exponential'], categorize(5**x)
