import fileinput
import math
import pytest
import re


def parse_input(line):
    match = re.match(
        r"^target area: x=([0-9]+)..([0-9]+), y=(-?[0-9]+)..(-?[0-9]+)$", line
    )
    if not match:
        raise ValueError("Bad input line: %s" % line)

    return (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
    )


def dist(v, steps):
    return v * (steps + 1) - steps * (steps + 1) // 2


def solve(line):
    x1, x2, y1, y2 = parse_input(line)

    hit_cnt = 0
    best = 0
    x = 1
    while x <= x2:
        y = y1
        while y <= abs(y1):
            step = 2 * max(y, 0)
            while dist(y, step) > y2:
                step += 1

            hit = False
            while dist(y, step) >= y1:
                if x1 <= dist(x, min(step, x)) <= x2:
                    hit = True
                    best = max(best, y)
                    break
                step += 1

            if hit:
                hit_cnt += 1
            y += 1
        x += 1

    return dist(best, best), hit_cnt


def test_parse():
    assert parse_input("target area: x=20..30, y=-10..-5") == (20, 30, -10, -5)


def test_part1():
    assert solve("target area: x=20..30, y=-10..-5")[0] == 45


def test_part2():
    assert solve("target area: x=20..30, y=-10..-5")[1] == 112


if __name__ == "__main__":
    (line,) = fileinput.input()
    line = line.strip()

    maxy, hit_cnt = solve(line)
    print("Highest y position is %d" % maxy)
    print("Number of different ways to hit: %d" % hit_cnt)
