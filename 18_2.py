import ast
import fileinput
import pytest 


def sparse(line):
    return ast.literal_eval(line)


def size(h):
    if isinstance(h, int):
        return 1
    else:
        return size(h[0]) + size(h[1])


def smap_leafs(h, fn, offset=0, depth=1):
    if isinstance(h, list):
        l = smap_leafs(h[0], fn, offset, depth + 1)
        r = smap_leafs(h[1], fn, offset + size(l), depth + 1)
        return [l, r]
    else:
        return fn(offset, depth, h)


def smap_int_pairs(h, fn, offset=0, depth=1):
    if isinstance(h, list):
        if is_int_pair(h):
            return fn(offset, depth, h)
        else:
            l = smap_int_pairs(h[0], fn, offset, depth + 1)
            r = smap_int_pairs(h[1], fn, offset + size(l), depth + 1)
            return [l, r]
    else:
        return h


def is_int_pair(h):
    return isinstance(h[0], int) and isinstance(h[1], int)


def sreduce_explode(h):
    class Step1:
        def __init__(self):
            self.found = None

        def __call__(self, idx, depth, h):
            if self.found is None and depth == 5:
                self.found = (idx, h)
                return 0
            else:
                return h

    class Step2:
        def __init__(self, updates):
            self.updates = updates

        def __call__(self, idx, depth, h):
            if idx in self.updates and isinstance(h, int):
                return self.updates[idx](h)
            else:
                return h

    step1 = Step1()
    h = smap_int_pairs(h, step1)
    if step1.found is not None:
        #print("explode found ", step1.found)
        idx, (l, r) = step1.found
        step2 = Step2({
            idx-1: lambda x: x + l,
            idx+1: lambda x: x + r,
        })
        h = smap_leafs(h, step2)
    return step1.found is not None, h


def sreduce_split(h):
    class Splitter:
        def __init__(self):
            self.done = False
        def __call__(self, idx, depth, h):
            if not self.done and  h >= 10:
                self.done = True
                return [h // 2, h // 2 + (h % 2)]
            else:
                return h

    splitter = Splitter()
    h = smap_leafs(h, splitter)
    return splitter.done, h


def sreduce(h):
    while True:
        acted, h = sreduce_explode(h)
        if acted:
            continue
        acted, h = sreduce_split(h)
        if not acted:
            break
    return h
    


def ssum(parsed):
    res = sreduce(parsed[0:2])
    for p in parsed[2:]:
        res = sreduce([res, p])
    return res


def smagnitude(h):
    if isinstance(h, int):
        return h
    else:
        return 3 * smagnitude(h[0]) + 2 * smagnitude(h[1])


def part1(inp):
    parsed = [sparse(line) for line in inp]
    summed = ssum(parsed)
    return smagnitude(summed)


def part2(inp):
    best = 0
    for i in range(len(inp)):
        for j in range(i + 1, len(inp)):
            best = max(best, part1([inp[i], inp[j]]))
            best = max(best, part1([inp[j], inp[i]]))
    return best


def test_sparse():
    assert [1, [2, 3]] == sparse("[1,[2,3]]")


def test_ssum():
    assert [[[[1,1],[2,2]],[3,3]],[4,4]] == ssum([[1,1], [2,2], [3,3], [4,4]])
    assert [[[[5,0],[7,4]],[5,5]],[6,6]] == ssum([[1,1], [2,2], [3,3], [4,4], [5,5], [6,6]])
    assert [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]] == ssum([
        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
    ])


def test_smagnitude():
    assert 29 == smagnitude([9, 1])
    assert 129 == smagnitude([[9, 1], [1, 9]])
    assert 3488 == smagnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])


def test_part1():
    assert 129 == part1(["[9, 1]", "[1, 9]"])


if __name__ == '__main__':
    inp = []
    for line in fileinput.input():
        line = line.strip()
        inp.append(line)

    print("The magnitude of the sum is %d" % part1(inp))
    print("Largest magnitude of sum of any 2 numbers is %d" % part2(inp))
