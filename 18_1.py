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
            (a, da), (b, db) = f[explosion:explosion+2]
            assert da == db

            f = f[0:explosion+1] + f[explosion+2:]
            if explosion >= 1:
                f[explosion - 1][0] += a
            f[explosion] = [0, da - 1]
            if explosion + 1 < len(f):
                f[explosion + 1][0] += b
        elif split is not None:
            num, depth = f[split]
            f = f[0:split] \
                    + [[num // 2, depth + 1], [num // 2 + (num % 2), depth + 1]] \
                    + f[split+1:]
    return f


def sadd(f1, f2):
    f1 = [[num, depth + 1] for num, depth in f1]
    f2 = [[num, depth + 1] for num, depth in f2]
    return sreduce(f1 + f2)


def ssum(parsed):
    flats = [sflat(p) for p in parsed]
    res = sadd(*flats[0:2])
    for f in flats[2:]:
        res = sadd(res, f)
    return shier(res)


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

    h = [[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]], [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]
    assert h == shier(sflat(h))


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
    assert sflat([[[[0,9],2],3],4]) == sreduce(sflat([[[[[9,8],1],2],3],4]))
    assert sflat([7,[6,[5,[7,0]]]]) == sreduce(sflat([7,[6,[5,[4,[3,2]]]]]))
    assert sflat([[6,[5,[7,0]]],3]) == sreduce(sflat([[6,[5,[4,[3,2]]]],1]))
    #assert sflat([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == sreduce(sflat([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]))
    assert sflat([[3,[2,[8,0]]],[9,[5,[7,0]]]]) == sreduce(sflat([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]))

    # several reductions
    assert sflat([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == sreduce(sflat([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]))


def test_iso():
    assert sflat([[[[0,7],4],[[7,8],[6,0]]],[8,1]]) == sreduce(sflat([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]))


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
