from sympy import randprime
from math import gcd
from random import choice

def keys_generator():
    p, q = randprime(100, 999), randprime(100, 999)
    n = p*q
    fn = (p-1)*(q-1)
    e = []
    for i in range(fn, 2, -1):
        if gcd(i, fn) == 1:
            e.append(i)
    e = choice(e)
    d = pow(e, -1, fn)
    return [(n, e), (n, d)]
           
