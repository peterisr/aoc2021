import fileinput


def fold(inp, along, at):
    ret = set()
    for x, y in inp:
        if along == "x":
            assert x != at
            if x > at:
                x = at - (x - at)
        elif along == "y":
            assert y != at
            if y > at:
                y = at - (y - at)
        else:
            raise ValueError("Invalid along direction: %s" % along)
        ret.add((x, y))

    assert all([x >= 0 and y >= 0 for x, y in ret])
    return ret


def fold_all(inp, folds):
    ret = set(inp)
    for f in folds:
        ret = fold(ret, *f)

    return ret


def to_board(points):
    mx, my = 0, 0
    for x, y in points:
        mx = max(mx, x)
        my = max(my, y)

    mx += 1
    my += 1

    board = [["." for _ in range(mx)] for _ in range(my)]
    for x, y in points:
        board[y][x] = "#"

    return "\n".join(["".join(row) for row in board])


finput = fileinput.input()
inp = set()
for line in finput:
    line = line.strip()
    if line == "":
        break
    inp.add(tuple(map(int, line.split(","))))

folds = []
for line in finput:
    line = line.strip()
    how, at = line.split("=")
    folds.append((how[-1], int(at)))

p1 = fold(inp, *folds[0])
print("After 1st fold there are %d points" % len(p1))

p2 = to_board(fold_all(inp, folds))
print("After all folds the board looks like this\n%s" % p2)
