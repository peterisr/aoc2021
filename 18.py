import ast
import fileinput
import pytest


def sparse(line):
    return ast.literal_eval(line)


def sflat(h):
    ret = []

    def rec(h, depth):
        assert len(h) == 2
        for i in range(0, 2):
            if isinstance(h[i], int):
                ret.append([h[i], depth])
            else:
                rec(h[i], depth + 1)

    rec(h, 1)
    return ret


def shier(f):
    def rec2(pos, depth):
        num, d = f[pos]
        if d == depth:
            return pos + 1, num
        else:
            next_pos, l = rec2(pos, depth + 1)
            next_next_pos, r = rec2(next_pos, depth + 1)
            return next_next_pos, [l, r]

    next_left, ret = rec2(0, 0)
    assert next_left == len(f)
    return ret


def sreduce(f):
    return sflat(sreduce_hier(shier(f)))

    while True:
        explosion = None
        split = None
        for idx, (num, depth) in enumerate(f):
            assert depth <= 5
            if depth == 5 and explosion is None:
                assert f[idx + 1][1] == 5
                explosion = idx

            if num >= 10 and split is None:
                split = idx

        if explosion is None and split is None:
            break
        elif explosion is not None:
            (a, da), (b, db) = f[explosion : explosion + 2]
            assert da == db

            f = f[0 : explosion + 1] + f[explosion + 2 :]
            if explosion >= 1:
                f[explosion - 1][0] += a
            f[explosion] = [0, da - 1]
            if explosion + 1 < len(f):
                f[explosion + 1][0] += b
        elif split is not None:
            num, depth = f[split]
            f = (
                f[0:split]
                + [[num // 2, depth + 1], [num // 2 + (num % 2), depth + 1]]
                + f[split + 1 :]
            )
    return f


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


def sreduce_hier_explode(h):
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
        # print("explode found ", step1.found)
        idx, (l, r) = step1.found
        step2 = Step2(
            {
                idx - 1: lambda x: x + l,
                idx + 1: lambda x: x + r,
            }
        )
        h = smap_leafs(h, step2)
    return step1.found is not None, h


def sreduce_hier_split(h):
    class Splitter:
        def __init__(self):
            self.done = False

        def __call__(self, idx, depth, h):
            if not self.done and h >= 10:
                self.done = True
                return [h // 2, h // 2 + (h % 2)]
            else:
                return h

    splitter = Splitter()
    h = smap_leafs(h, splitter)
    return splitter.done, h


def sreduce_hier(h):
    if False:
        return shier(sreduce(sflat(h)))
    else:
        while True:
            acted, h = sreduce_hier_explode(h)
            if acted:
                continue
            acted, h = sreduce_hier_split(h)
            if not acted:
                break
        return h


def ssum(parsed):
    res = sreduce_hier(parsed[0:2])
    for p in parsed[2:]:
        res = sreduce_hier([res, p])
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


def test_sflat():
    assert [[1, 1], [2, 1]] == sflat([1, 2])
    assert [[1, 1], [2, 2], [3, 2]] == sflat([1, [2, 3]])
    assert [[1, 1], [2, 3], [3, 3], [4, 2]] == sflat([1, [[2, 3], 4]])


def test_shier():
    assert [1, 2] == shier([[1, 1], [2, 1]])
    assert [1, [2, 3]] == shier([[1, 1], [2, 2], [3, 2]])
    assert [1, [[2, 3], 4]] == shier([[1, 1], [2, 3], [3, 3], [4, 2]])
    assert [[1, 1], [2, 2]] == shier([[1, 2], [1, 2], [2, 2], [2, 2]])

    h = [1, [[2, [3, [4, 4]]], 5]]
    assert h == shier(sflat(h))

    h = [
        [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
        [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
    ]
    assert h == shier(sflat(h))
    # assert [[[[4, 0], [5, 4], [7, 7], [6, 0], [6, 6], [5, 6], [6, 0], [7, 7]]]] == shier([[4, 4], [0, 4], [5, 4], [4, 4], [7, 4], [7, 4], [6, 4], [0, 4], [6, 4], [6, 4], [5, 4], [6, 4], [6, 4], [0, 4], [7, 4], [7, 4]])


def test_sreduce():
    # no reduce
    assert [[1, 1], [2, 1]] == sreduce([[1, 1], [2, 1]])

    # splits
    assert [[5, 2], [6, 2], [2, 1]] == sreduce([[11, 1], [2, 1]])
    assert [[1, 1], [6, 2], [6, 2]] == sreduce([[1, 1], [12, 1]])
    assert [[1, 1], [6, 3], [6, 3], [3, 2]] == sreduce([[1, 1], [12, 2], [3, 2]])

    # explodes
    assert sflat([[[[0, 3], 3], 4], 5]) == sreduce(sflat([[[[[1, 1], 2], 3], 4], 5]))
    assert sflat([1, [2, [3, [9, 0]]]]) == sreduce(sflat([1, [2, [3, [4, [5, 5]]]]]))
    assert sflat([1, [[2, [7, 0]], 9]]) == sreduce(sflat([1, [[2, [3, [4, 4]]], 5]]))

    # test cases from task
    assert sflat([[[[0, 9], 2], 3], 4]) == sreduce(sflat([[[[[9, 8], 1], 2], 3], 4]))
    assert sflat([7, [6, [5, [7, 0]]]]) == sreduce(sflat([7, [6, [5, [4, [3, 2]]]]]))
    assert sflat([[6, [5, [7, 0]]], 3]) == sreduce(sflat([[6, [5, [4, [3, 2]]]], 1]))
    # assert sflat([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == sreduce(sflat([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]))
    assert sflat([[3, [2, [8, 0]]], [9, [5, [7, 0]]]]) == sreduce(
        sflat([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]])
    )

    # several reductions
    assert sflat([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == sreduce(
        sflat([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
    )


def test_iso():
    assert sflat([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]) == sreduce(
        sflat([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
    )


def test_ssum():
    assert [[[[1, 1], [2, 2]], [3, 3]], [4, 4]] == ssum(
        [[1, 1], [2, 2], [3, 3], [4, 4]]
    )
    assert [[[[5, 0], [7, 4]], [5, 5]], [6, 6]] == ssum(
        [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
    )
    assert [
        [[[4, 0], [5, 4]], [[7, 7], [6, 0]]],
        [[8, [7, 7]], [[7, 9], [5, 0]]],
    ] == ssum(
        [
            [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
            [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
        ]
    )


def test_smagnitude():
    assert 29 == smagnitude([9, 1])
    assert 129 == smagnitude([[9, 1], [1, 9]])
    assert 3488 == smagnitude(
        [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
    )


def test_part1():
    129 == part1(["[9, 1]", "[1, 9]"])


if __name__ == "__main__":
    inp = []
    for line in fileinput.input():
        line = line.strip()
        inp.append(line)

    print("The magnitude of the sum is %d" % part1(inp))
    print("Largest magnitude of sum of any 2 numbers is %d" % part2(inp))
