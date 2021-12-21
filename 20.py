import fileinput


def bounded(x, y, h, w):
    return 0 <= x < h and 0 <= y < w


def pad(inp, padding):
    h, w = len(inp), len(inp[0])
    ret = [["."] * (w + padding * 2) for _ in range(h + padding * 2)]
    for r in range(h):
        for c in range(w):
            ret[r + padding][c + padding] = inp[r][c]
    return ret


def unpad(inp, padding):
    return [row[padding:-padding] for row in inp[padding:-padding]]


def enhance(map, inp, iters):
    expand_pad = iters * 2
    safety_pad = iters + 10
    inp = pad(inp, expand_pad + safety_pad)
    h, w = len(inp), len(inp[0])

    stack = [[list(row) for row in inp], [list(row) for row in inp]]
    for i in range(iters):
        read = stack[i % 2]
        write = stack[(i + 1) % 2]
        for r in range(h):
            for c in range(w):
                idx = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        idx *= 2
                        if (
                            0 <= r + x < h
                            and 0 <= c + y < w
                            and read[r + x][c + y] == "#"
                        ):
                            idx += 1
                write[r][c] = map[idx]

    # print("Before unpad")
    # print("\n".join(out))
    ret = unpad(write, safety_pad)
    # print("After unpadding\n")
    # print("\n".join(ret))
    return ret


def count(inp):
    return sum(
        [1 for r in range(len(inp)) for c in range(len(inp[r])) if inp[r][c] == "#"]
    )


def part1(map, inp):
    out = enhance(map, inp, 2)
    return count(out)


def part2(map, inp):
    out = enhance(map, inp, 50)
    return count(out)


all_inp = []
for line in fileinput.input():
    all_inp.append(line.strip())

map, inp = all_inp[0], all_inp[2:]
assert len(map) == 512
assert map[0] != map[-1]
print("Part 1: %d" % part1(map, inp))
print("Part 2: %d" % part2(map, inp))
