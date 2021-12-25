import fileinput


def move(B, max_times=1e18):
    L = [list(row) for row in B]
    N = [["."] * len(row) for row in B]
    moved = set([-1])
    change = True
    cnt = 0
    while max_times > 0 and change:
        change = False
        moved.clear()
        for r, row in enumerate(L):
            for c, chr in enumerate(row):
                left = L[r][c - 1]
                if chr == "." and left == ">":
                    N[r][c - 1] = "."
                    N[r][c] = ">"
                    change = True
                    moved.add((r, c - 1 if c > 0 else len(row) - 1))
                else:
                    if (r, c) in moved:
                        chr = "."
                    N[r][c] = chr

        for r, row in enumerate(N):
            for c, chr in enumerate(row):
                up = N[r - 1][c]
                if chr == "." and up == "v":
                    L[r - 1][c] = "."
                    L[r][c] = "v"
                    change = True
                    moved.add((r - 1 if r > 0 else len(B) - 1, c))
                else:
                    if (r, c) in moved:
                        chr = "."
                    L[r][c] = chr

        if change:
            cnt += 1
        max_times -= 1
    return ["".join(row) for row in L], cnt


def test_move():
    assert (["..", ".."], 0) == move(["..", ".."], 1)
    assert ([">.", ".."], 1) == move([".>", ".."], 1)
    assert ([".>", ".."], 1) == move([">.", ".."], 1)
    assert ([".>", ".v"], 1) == move([">.", ".v"], 1)
    assert ([">v", ".."], 2) == move([">.", ".v"], 2)
    assert ([">>.>>"], 2) == move([">>>>."], 2)


def str2b(s):
    return [line.strip() for line in s.strip().split("\n")]


def test_sample():
    inp = str2b(
        """
		v...>>.vv>
		.vv>>.vv..
		>>.>v>...v
		>>v>>.>.v.
		v>v.vv.v..
		>.>>..v...
		.vv..>.>v.
		v.v..>>v.v
		....v..v.>
	"""
    )
    out = str2b(
        """
		..>>v>vv..
		..v.>>vv..
		..>>v>>vv.
		..>>>>>vv.
		v......>vv
		v>v....>>v
		vvv.....>>
		>vv......>
		.>v.vv.v..
	"""
    )
    assert (out, 57) == move(inp)


def part1(B):
    _, moves = move(B)
    return moves + 1


if __name__ == "__main__":
    lines = [line.strip() for line in fileinput.input()]
    print("Part 1: %d" % part1(lines))
