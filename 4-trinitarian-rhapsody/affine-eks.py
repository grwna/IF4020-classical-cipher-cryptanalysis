def decrypt_affine(m: int, b: int, ct: str):
    pt = ""
    for c in ct:
        x = pow(m, -1, 26) * ((ord(c) - 65) - b) % 26
        pt += chr(x + 65)
    return pt

text = open('t.txt', 'r').read()
primes = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
for m in primes:
    for b in range (26):
        print(f"======== TEST M: {m}, B: {b} ==============")
        print(decrypt_affine(m, b, text))