text = open('v.txt', 'r').read()
english_top_10 = [ 'E', 'T','A','O','I','N','S','H','R', 'D']

def split_on_key_len(kl: int):
    splitted = ["" for _ in range(kl)]
    for i in range(len(text)):
        splitted[i % kl] += text[i]
    return splitted

def most_frequent_letters(s: str):
    freq = {}
    for c in s:
        if c not in freq:
            freq[c] = 1
        else: freq[c] +=1

    top_10 = sorted(freq, key=freq.get, reverse=True)[:10]

    for k in top_10:
        print(f"{k}: {freq[k]}")

    return top_10

# p + k = c --> k = c - p (mod 26)
def shift_to_key(c: chr, p: chr):
    return chr(((ord(c) - ord(p) - 2 * 65) % 26) + 65)

if __name__ == '__main__':
    kl = 10
    splitted = split_on_key_len(kl)
    top_10s = [] # will be 10x10
    for i, s in enumerate(splitted):
        print("Line ", i+1)
        top_10s.append(most_frequent_letters(s))
    
    with open('outputs/keys.txt', 'w')as f:
        for i in range(10):
            key_cand = ""
            for j in range(kl):
                key_cand += shift_to_key(top_10s[j][i], english_top_10[i])
            f.write(key_cand + '\n')


    