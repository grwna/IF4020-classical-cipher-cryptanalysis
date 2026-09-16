import math

import numpy as np


def matrix_mod_inv(mat, mod=26):
    det = round(np.linalg.det(mat)) % mod
    if math.gcd(det, mod) != 1:
        return None
    inv_det = pow(det, -1, mod)
    adj = np.round(np.linalg.inv(mat) * np.linalg.det(mat)).astype(int) % mod
    return (inv_det * adj) % mod


# Convert texts to ordinal values (0-25)
plaintext_start = [ord(c.lower()) - 97 for c in "EXPLOSIVESCOOP"]
with open("h.txt", "r") as f:
    ciphertext = [ord(c.lower()) - 97 for c in f.read() if c.isalpha()]

# Try out different values of m up to max_m
# max_m is the square root of the length of the plaintext because we need max_m^2 of characters to get max_m of linear equations
# I thought of this myself btw ;3
max_m = math.isqrt(len(plaintext_start))

for m in range(1, max_m + 1):
    print(f"=== m = {m} ===")
    c_matrix = np.array([[ciphertext[i * m + j] for j in range(m)] for i in range(m)])
    p_matrix = np.array(
        [[plaintext_start[i * m + j] for j in range(m)] for i in range(m)]
    )

    p_inv = matrix_mod_inv(p_matrix)
    if p_inv is None:
        print("P is not invertible mod 26\n")
        continue

    # Solve K
    k_matrix = (p_inv @ c_matrix) % 26
    print("K:")
    print(k_matrix)

    # Inverse key K
    k_inverse = matrix_mod_inv(k_matrix)
    if k_inverse is None:
        print("K is not invertible mod 26\n")
        continue

    print("K inverse:")
    print(k_inverse)

    # Decrypt ciphertext using K inverse
    decrypted = []
    for i in range(0, len(ciphertext) - len(ciphertext) % m, m):
        block = np.array(ciphertext[i : i + m])
        decrypted.extend((block @ k_inverse) % 26)

    print("Decrypted:")
    print("".join([chr(c + 97) for c in decrypted]))
    print()
