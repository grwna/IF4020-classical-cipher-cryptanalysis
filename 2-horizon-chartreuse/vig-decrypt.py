def decrypt(c: str, key: str):
    key_len = len(key)
    c_len = len(c)
    
    pt = ""

    for i in range(c_len):
        pt += chr(((ord(c[i]) - ord(key[i % key_len]) - 2 * 65) % 26) + 65)

    return pt
    

if __name__ == "__main__":
    text = open("v.txt", "r").read()
    open('plaintext.txt', 'w').write(decrypt(text, "UNDERNIGHT"))