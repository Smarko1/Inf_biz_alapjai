import random

def ext_euclid(a,b):
    if a == 0 :
        return b,0,1
             
    gcd,x1,y1 = ext_euclid(b%a, a)
     
    x = y1 - (b//a) * x1
    y = x1
     
    return gcd,x,y

def modular_exp(x, y, m):
    res = 1
    x = x % m
    while (y > 0):
        if ((y & 1) != 0):
            res = (res * x) % m
        y = y >> 1  
        x = (x * x) % m
    return res

def is_prime(n, num_of_tests=5):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d = d // 2

    def try_composite(a):
        if modular_exp(a, d, n) == 1:
            return False
        for i in range(s):
            if modular_exp(a, 2 ** i * d, n) == n - 1:
                return False
        return True  

    for _ in range(num_of_tests):
        a = random.randrange(2, n)
        if try_composite(a):
            return False

    return True

def chinese_rem(c, m1, m2, d):
    m = m1 * m2
    c1 = modular_exp(c, d % (m2 - 1), m2)
    c2 = modular_exp(c, d % (m1 - 1), m1)

    _, y1, y2 = ext_euclid(m1, m2)

    return ((c1 * y1 * m1) + (c2 * y2 * m2)) % m

def rsa():
    min = 10
    max= 10000
    p = random.randint(min, max)
    while not is_prime(p):
        p = random.randint(min, max)
    
    q = random.randint(min, max)
    while not is_prime(q):
        q = random.randint(min, max)
    n = p*q
    phi_n=(p-1) * (q-1)

    while True:
        e = random.randint(1,phi_n)
        if ext_euclid(e, phi_n)[0] == 1:
            break
    
    d= ext_euclid(e, phi_n)[1]
    return q, e, d, p, n



if __name__ == '__main__':
    q, e, d, p, n = rsa()
    message = 11
    print("d=", d)
    print(f'Public key: {e,n}')
    print(f'Private key: {d,n}')

    print('Original message:', message)
    C= chinese_rem(message, q, p, d)
    print(f'Encrypted message: {C}')
    M = modular_exp(C, e, n)
    print(f'Decrypted message: {M}')

