import fileinput
import heapq


def dijkstra(inp):
    m = len(inp)
    assert all([len(row) == m for row in inp])
    n = m * m

    diffs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    mrange = range(m)
    res = [[0] * m for _ in range(m)]
    visited = set()
    Q = [(0, 0, 0)]
    while len(Q) > 0:
        dist, x, y = heapq.heappop(Q)

        if (x, y) in visited:
            assert res[x][y] <= dist
            continue

        visited.add((x, y))
        res[x][y] = dist

        for dx, dy in diffs:
            nx, ny = x + dx, y + dy
            if nx in mrange and ny in mrange:
                heapq.heappush(Q, (dist + inp[nx][ny], nx, ny))

    return res


def part1(inp):
    shortest_paths = dijkstra(inp)
    return shortest_paths[-1][-1]


def part2(inp):
    n = len(inp)
    M = [[0] * n * 5 for _ in range(n * 5)]

    for i in range(n):
        for j in range(n):
            for k in range(5):
                for l in range(5):
                    val = inp[i][j] + k + l
                    if val >= 10:
                        val = val % 10 + 1
                    M[k * n + i][l * n + j] = val

    # print("\n".join(["".join(map(str, row)) for row in M]))

    shortest_paths = dijkstra(M)
    return shortest_paths[-1][-1]


inp = []
for line in fileinput.input():
    line_int = list(map(int, line.strip()))
    inp.append(line_int)

print("Shortest path from top left to bottom right: %d" % part1(inp))
print("Shortest path from top left to bottom right 5x5: %d" % part2(inp))
