text = open('v.txt', 'r').read()


def duplicate_ngram_finder(n: int):
    seen = {}
    for i in range(len(text) - (n-1)):
        gram = text[i : i + n]
        if gram not in seen:
            seen[gram] = []
        seen[gram].append(i)

    gaps_list = []
    for k in seen:
        if len(seen[k]) > 1:
            gaps = [seen[k][i] - seen[k][i - 1] for i in range(1, len(seen[k]))]
            gaps_list.append(gaps)
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

    top_10_factors = sorted(factors_count, key=factors_count.get, reverse=True)[:10]
    return {fac: factors_count[fac] for fac in top_10_factors}


if __name__ == '__main__':
    gaps = []
    for i in range (3,100):
        gaps.append(merge_list(duplicate_ngram_finder(i)))

    gaps = merge_list(gaps)

    f = []
    for n in gaps:
        f.append(factorize(n))

    top_factors = count_factors(f)
    with open('top_factors.txt', 'w') as f:
        for fac in top_factors:
            f.write(f"{fac}: {top_factors[fac]}\n")
