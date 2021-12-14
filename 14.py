import fileinput
from collections import defaultdict


def iterate(template, rules, steps):
    pairs = defaultdict(int)
    for a, b in zip(template, template[1:]):
        pairs[a + b] += 1

    for step in range(steps):
        next = defaultdict(int)
        for p, cnt in pairs.items():
            next[p[0] + rules[p]] += cnt
            next[rules[p] + p[1]] += cnt
        pairs = next

    unrolled = defaultdict(int)
    for p, cnt in pairs.items():
        for c in p:
            unrolled[c] += cnt

    unrolled[template[0]] += 1
    unrolled[template[-1]] += 1

    assert all([cnt % 2 == 0 for cnt in unrolled.values()])

    ret = {(c, cnt // 2) for c, cnt in unrolled.items()}
    return ret


def ans(template, rules, steps):
    freq = iterate(template, rules, steps)
    sorting = sorted(map(lambda p: p[1], freq))
    return sorting[-1] - sorting[0]


inp = []
for line in fileinput.input():
    inp.append(line.strip())

template = inp[0]
rules = {}
for line in inp[2:]:
    lhs, rhs = line.split(" -> ")
    rules[lhs] = rhs

for steps in [10, 40]:
    print(
        "After %d steps, the max-min difference is %d"
        % (steps, ans(template, rules, steps))
    )
