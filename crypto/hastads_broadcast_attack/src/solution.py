# make sure joe didn't mess up
#
# Citation:
# https://github.com/aaossa/Computer-Security-Algorithms/blob/master/11%20-%20H%C3%A5stad's%20Broadcast%20Attack/hastads-broadcast-attack.py
from binascii import unhexlify
from functools import reduce
import gmpy

def gcd(a, b):
    x, y = 0, 1
    last_x, last_y = 1, 0

    while b:
        a, (q, b) = b, divmod(a, b)
        x, last_x = last_x - q * x, x
        y, last_y = last_y - q * y, y

    return last_x, last_y, a


def crt(cs, ns):
    product = reduce(lambda x, y: x * y, ns)

    result = 0
    for c, n in zip(cs, ns):
        m = product // n
        r, s, d = gcd(n, m)
        result += c * s * m

    return result % product


def main():
    ns, cs = [], []
    with open('data.txt') as file:
        for line in file.readlines():
            n, c = (int(a) for a in line.split(','))
            ns.append(n)
            cs.append(c)

    c = gmpy.mpz(crt(cs, ns)).root(3)[0]
    m = hex(int(c))[2:]
    print(unhexlify(m).decode('utf-8'))

if __name__ == '__main__':
    main()
