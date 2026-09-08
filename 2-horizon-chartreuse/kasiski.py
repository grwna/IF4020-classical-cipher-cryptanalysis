text = open('v.txt', 'r').read()


def duplicate_ngram_finder(n: int):
    seen = {}
    for i in range(len(text) - (n-1)):
        gram = text[i : i + n]
        if gram not in seen:
            seen[gram] = []
        seen[gram].append(i)

    gaps_list = []
    for pat, pos in seen.items():
        if len(pos) > 1:
            gaps = [pos[i] - pos[i - 1] for i in range(1, len(pos))]
            gaps_list.append(gaps)
            print(f"pattern: {pat} | distances: {gaps}")

    return gaps_list


def merge_list(list: list[list]):
    merged = []
    for l in list:
        if l:
            merged += l
    return merged

# x -> [list of factors]
def factorize(x: int):
    f = []
    for i in range(2, (x // 2) + 1):
        if x % i == 0:
            f.append(i)
    f.append(x)
    return f

def count_factors(f: list[list]):
    factors_count = {}
    for fac in f:
        for n in fac:
            if n not in factors_count:
                factors_count[n] = 1
            else: factors_count[n] += 1

    for k in sorted(factors_count, key=factors_count.get, reverse=True)[:10]:
        print(f"{k}: {factors_count[k]}")

if __name__ == '__main__':
    gaps = []
    for i in range (3,100):
        gaps.append(merge_list(duplicate_ngram_finder(i)))

    gaps = merge_list(gaps)

    f = []
    for n in gaps:
        f.append(factorize(n))

    print(count_factors(f))
