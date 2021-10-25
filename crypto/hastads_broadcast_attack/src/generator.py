import binascii

e = 3


def generate_ciphertexts(flag, ps, qs):
    assert e == len(ps) and e == len(qs)
    m = int(binascii.hexlify(flag.encode()), 16)

    for p, q in zip(ps, qs):
        n = int(p * q)
        ciphertext = pow(m, e, n)
        yield n, ciphertext


def main():
    with open('flag.txt') as file:
        flag = file.read()

    ps, qs = [], []
    with open('ps_and_qs.txt') as file:
        for line in file.readlines():
            p, q = (int(a) for a in line.split(','))
            ps.append(p)
            qs.append(q)

    with open('data.txt', 'w+') as file:
        for n, c, in generate_ciphertexts(flag, ps, qs):
            file.write(f'{n},{c}\n')


if __name__ == '__main__':
    main()
