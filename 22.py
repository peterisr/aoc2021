import copy
import fileinput
from intervaltree import IntervalTree, Interval


def parse_line(line):
    on_off, ranges = line.split(" ")
    parsed_ranges = map(
        lambda x: tuple(map(int, x.split("=")[1].split(".."))), ranges.split(",")
    )
    return (int(on_off == "on"), *parsed_ranges)


def test_parsed_line():
    assert (1, (-1, 1), (-10, 10), (-100, 100)) == parse_line(
        "on x=-1..1,y=-10..10,z=-100..100"
    )
    assert (0, (-2, -1), (0, 1), (2, 4)) == parse_line("off x=-2..-1,y=0..1,z=2..4")


class CubeTree:
    def __init__(self, min, max):
        min -= 1
        max += 1
        self.t = IntervalTree(
            [
                Interval(
                    min,
                    max,
                    IntervalTree(
                        [Interval(min, max, IntervalTree([Interval(min, max, 0)]))]
                    ),
                )
            ]
        )

    def slicer(self, iv, islower):
        return iv.data if islower else copy.deepcopy(iv.data)

    def doinsert(self, t, dims, val, depth=0):
        dim = dims[depth]

        if depth <= 1:
            for p in dim:
                t.slice(p, datafunc=self.slicer)

            for iv in t.envelop(*dim):
                self.doinsert(iv.data, dims, val, depth + 1)
        else:
            t.chop(*dim)
            if val == 1:
                t.addi(*dim, val)

    def insert(self, x, y, z, is_on):
        dims = [x, y, z]
        dims = [(p[0], p[1] + 1) for p in dims]
        self.doinsert(self.t, dims, is_on)

    @staticmethod
    def l(iv):
        return iv.length()

    def count(self):
        cnt = 0
        for xiv in self.t:
            for yiv in xiv.data:
                for ziv in yiv.data:
                    cnt += self.l(xiv) * self.l(yiv) * self.l(ziv) * ziv.data
        return cnt


def test_cube_tree():
    t = CubeTree(0, 10)
    assert t.count() == 0
    t.insert((1, 3), (4, 6), (7, 9), 1)
    assert t.count() == 3 * 3 * 3
    t.insert((1, 3), (5, 7), (3, 5), 1)
    assert t.count() == 3 * (1 * 3 + 2 * (3 + 3) + 1 * 3)


def solve(Q):
    mi, ma = (1e100, -1e100)
    for q in Q:
        all_c = [c for p in q[1:] for c in p]
        mi = min(mi, min(all_c))
        ma = max(ma, max(all_c))

    t = CubeTree(mi, ma)
    for idx, q in enumerate(Q):
        t.insert(*q[1:], q[0])
        print("Added %d/%d" % (idx + 1, len(Q)))

    return t.count()


def test_solve():
    assert 1 == solve([(1, (2, 2), (2, 2), (2, 2))])


def part1(Q):
    filtered = []
    for q in Q:
        if all([-50 <= c <= 50 for p in q[1:] for c in p]):
            filtered.append(q)
    return solve(filtered)


# Takes about 30 seconds with python3 on Ryzen 5800H, about 10sec with pypy3.
# I could eliminate unnecessary chopping and merge equal neighbouring intervals
# to boost the speed, but this is good enough for AoC.
def part2(Q):
    return solve(Q)


if __name__ == "__main__":
    Q = []
    for line in fileinput.input():
        Q.append(parse_line(line.strip()))

    print("Part 1: %d" % part1(Q))
    print("Part 2: %d" % part2(Q))
