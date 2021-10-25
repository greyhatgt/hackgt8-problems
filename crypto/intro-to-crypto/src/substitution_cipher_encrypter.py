import random

letters = "abcdefghijklmnopqrstuvwxyz"
letters = list(letters)
result_letters = list(letters)
random.shuffle(result_letters)
key = dict(zip(letters, result_letters))
plaintext = "this is not a very secure cipher. it can easily be solved online."

print(''.join([c if c not in key else key[c] for c in plaintext]))
# zmon on nzovv xwz q pjhy njtlhj tofmjh.

print(key)
# {
#   'a': 'q', 'b': 'k', 'c': 't', 'd': 'c', 'e': 'j', 'f': 's', 'g': 'b',
#   'h': 'm', 'i': 'o', 'j': 'd', 'k': 'i', 'l': 'v', 'm': 'r', 'n': 'x',
#   'o': 'w', 'p': 'f', 'q': 'u', 'r': 'h', 's': 'n', 't': 'z', 'u': 'l',
#   'v': 'p', 'w': 'g', 'x': 'a', 'y': 'y', 'z': 'e'
# }
