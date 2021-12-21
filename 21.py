import fileinput


def parse(s):
    return int(s.split(":")[1].strip())


def upd_pos(p, roll):
    return (p + roll - 1) % 10 + 1


def part1(p1, p2):
    iter = 0
    dice = 0
    p = [p1, p2]
    s = [0, 0]
    while all([x < 1000 for x in s]):
        idx = iter % 2
        p[idx] = upd_pos(p[idx], dice * 3 + 6)
        s[idx] += p[idx]
        dice = ((dice + 3) - 1) % 100 + 1
        # print("Iter %d, p[%d] = %d, s[%d] = %d, dice = %d" %
        # 	(iter, idx, p[idx], idx, s[idx], dice))
        iter += 1

    winner = 0 if s[0] >= 1000 else 1
    loser = 0 if winner == 1 else 1
    assert winner != loser

    return s[loser] * iter * 3


def pos():
    return [[[0, 0] for _ in range(11)] for _ in range(11)]


def dp_dimensions(s1_range, s2_range):
    r = []
    for s1 in s1_range:
        for s2 in s2_range:
            for p1 in range(11):
                for p2 in range(11):
                    for next in range(2):
                        yield s1, s2, p1, p2, next


def part2(p1, p2):
    max_score1 = 30 + 1
    dp = [[pos() for _ in range(max_score1)] for _ in range(max_score1)]

    rolls = [a + b + c for a in range(1, 4) for b in range(1, 4) for c in range(1, 4)]

    dp[0][0][p1][p2][0] = 1
    for s1, s2, p1, p2, next in dp_dimensions(range(21), range(21)):
        other = {0: 1, 1: 0}[next]
        dpc = dp[s1][s2][p1][p2][next]
        for roll in rolls:
            if next == 0:
                npos = upd_pos(p1, roll)
                dp[s1 + npos][s2][npos][p2][other] += dpc
            else:
                npos = upd_pos(p2, roll)
                dp[s1][s2 + npos][p1][npos][other] += dpc

    ret = 0
    w = [0, 0]
    for win, lose, p1, p2, next in dp_dimensions(range(21, max_score1), range(21)):
        w[0] += dp[win][lose][p1][p2][next]
        w[1] += dp[lose][win][p1][p2][next]

    winner = 0 if w[0] > w[1] else 1
    return w[winner]


p1, p2 = fileinput.input()
p1, p2 = parse(p1), parse(p2)
print("Part 1: %d" % part1(p1, p2))
print("Part 2: %d" % part2(p1, p2))
