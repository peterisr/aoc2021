import fileinput
import sys


def neighbours(i, j, n):
    for r in range(i - 1, i + 2):
        for c in range(j - 1, j + 2):
            if r >= 0 and r < n and c >= 0 and c < n and (r != 0 or c != 0):
                yield (r, c)


def one_step(step_num, a):
    did_flash = [[False for _ in range(n)] for _ in range(n)]
    step_flash = 0
    a = [[x + 1 for x in row] for row in a]

    settled = False
    while not settled:
        settled = True
        for i in range(n):
            for j in range(n):
                if a[i][j] >= 10 and not did_flash[i][j]:
                    settled = False
                    did_flash[i][j] = True
                    for ni, nj in neighbours(i, j, n):
                        a[ni][nj] += 1

    a = [[x if x < 10 else 0 for x in row] for row in a]
    assert all([x != 10 for row in a for x in row])

    a_str = "\n".join(["".join([str(x) for x in row]) for row in a])
    step_flash = sum([1 for row in a for x in row if x == 0])
    # print("Step %d: %d flashes\n%s" % (step_num, step_flash, a_str), file=sys.stdout)
    return a, step_flash


a = []
for line in fileinput.input():
    a.append([int(c) for c in line.strip()])

n = len(a)
assert all([len(row) for row in a])

steps = 100
flashes = 0
for step in range(steps):
    a, step_flash = one_step(step + 1, a)
    flashes += step_flash

print("Total flashes after %d steps: %d" % (steps, flashes))

step_flash = 0
while step_flash < n * n:
    steps += 1
    a, step_flash = one_step(steps, a)

print("Synchronization after %d steps" % steps)
