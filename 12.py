import fileinput


def is_large(x):
    return x[0] >= "A" and x[0] <= "Z"


def paths(G, part):
    ret = []
    visits = {v: 0 for v in G.keys()}
    cur_path = []

    def run(node, fn_next):
        if node == "end":
            ret.append(tuple(cur_path))
            return

        visits[node] += 1
        cur_path.append(node)
        for next in fn_next(G, node):
            run(next, fn_next)
        visits[node] -= 1
        cur_path.pop()

    def next_p1(G, node):
        for next in G[node]:
            if is_large(next) or visits[next] == 0:
                yield next

    def next_p2(G, node):
        small2 = any([not is_large(n) and v >= 2 for n, v in visits.items()])
        for next in G[node]:
            if (
                is_large(next)
                or visits[next] == 0
                or (visits[next] == 1 and not small2 and next not in ["start", "end"])
            ):
                yield next

    run("start", next_p1 if part == 1 else next_p2)
    return ret


G = {}
for line in fileinput.input():
    a, b = line.strip().split("-")
    for x in [a, b]:
        if x not in G:
            G[x] = []

    G[a].append(b)
    G[b].append(a)

print("Total paths (part 1): %d" % len(paths(G, 1)))
print("Total paths (part 2): %d" % len(paths(G, 2)))
