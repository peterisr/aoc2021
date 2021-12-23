import fileinput

# import pytest
import itertools


def parse(inp):
    ret = {}
    scanner = None
    for line in inp:
        line = line.strip()
        if line.startswith("--- scanner"):
            scanner = int(line.split("scanner ")[1].split(" ")[0])
            ret[scanner] = []
        elif line == "":
            continue
        else:
            x, y, z = map(int, line.split(","))
            ret[scanner].append((x, y, z))
    return ret


def test_parse():
    assert {1: [(1, 2, 3), (-1, -2, -3)], 5: [(4, 5, 6)]} == parse(
        """
			--- scanner 1 ---
			1,2,3
			-1,-2,-3

			--- scanner 5 ---
			4,5,6
		""".split(
            "\n"
        )
    )


def convert(p, perm, dir):
    return (dir[0] * p[perm[0]], dir[1] * p[perm[1]], dir[2] * p[perm[2]])


def test_convert():
    assert (-2, 3, -1) == convert((1, 2, 3), (1, 2, 0), (-1, 1, -1))


def move(p, offset):
    return (offset[0] + p[0], offset[1] + p[1], offset[2] + p[2])


def test_move():
    assert (2, 3, -2) == move((1, 1, 1), (1, 2, -3))


def overlap_size(a, b):
    cnt = 0
    for p in b:
        if all([-1000 <= x <= 1000 for x in p]):
            if p not in a:
                return 0
            cnt += 1

    return cnt


def test_overlap_size():
    assert 1 == overlap_size([(1, 2, 3)], [(1, 2, 3)])
    assert 1 == overlap_size([(1, 2, 3)], [(1, 2, 3), (1001, 2, 3)])
    assert 2 == overlap_size(
        [(1, 2, 3), (10, 10, 10)], [(1, 2, 3), (10, 10, 10), (1001, 2, 3)]
    )
    assert 0 == overlap_size([(1, 2, 3)], [(1, 2, 3), (-1000, 2, 3)])


def sub(p1, p2):
    return tuple(x1 - x2 for x1, x2 in zip(p1, p2))


def test_sub():
    assert (1, 0, -1) == sub((1, 1, 1), (0, 1, 2))


def try_match(a, b, ap, bp, min_overlap=12):
    os = []
    for stable, to_move, sp, mp in [(a, b, ap, bp), (b, a, bp, ap)]:
        offset = sub(sp, mp)
        moved = [move(p, offset) for p in to_move]
        os.append(overlap_size(stable, moved))

    if os[0] != os[1] or os[0] < min_overlap:
        return None

    print("\t\ttry_match: %s, %s = %s" % (str(ap), str(bp), str(sub(ap, bp))))
    return sub(ap, bp)


def test_try_match():
    assert None == try_match(
        [(0, 0, 0), (1, 1, 1)],
        [(10, 10, 10), (12, 12, 12)],
        (0, 0, 0),
        (10, 10, 10),
        min_overlap=2,
    )
    assert (-10, -10, -10) == try_match(
        [(0, 0, 0), (1, 1, 1)],
        [(10, 10, 10), (11, 11, 11)],
        (0, 0, 0),
        (10, 10, 10),
        min_overlap=2,
    )
    assert (-10, -10, -10) == try_match(
        [(0, 0, 0), (1, 1, 1)],
        [(10, 10, 10), (11, 11, 11), (-999, -999, -999)],
        (0, 0, 0),
        (10, 10, 10),
        min_overlap=2,
    )
    assert (68, -1246, -43) == try_match(
        [(404, -588, -901)],
        [(336, 658, -858)],
        (404, -588, -901),
        (336, 658, -858),
        min_overlap=1,
    )
    assert (68, 1246, -43) == try_match(
        [(-336, 658, 858)],
        [(-404, -588, 901)],
        (-336, 658, 858),
        (-404, -588, 901),
        min_overlap=1,
    )


def orientations():
    ret = []
    for perm in itertools.permutations((0, 1, 2)):
        for a in [-1, 1]:
            for b in [-1, 1]:
                for c in [-1, 1]:
                    ret.append((perm, (a, b, c)))
    return tuple(ret)


def test_orientations():
    assert ((2, 0, 1), (-1, -1, 1)) in orientations()


def find_match(a, b, min_overlap=12):
    all_matches = set()
    for perm, dir in orientations():
        b_conv = [convert(p, perm, dir) for p in b]
        for idxa, match_a in enumerate(a):
            for idx, match_with in enumerate(b_conv):
                move = try_match(
                    a, b_conv, match_a, match_with, min_overlap=min_overlap
                )
                if move:
                    print(
                        "\t\tfind_match %s, %s orig=%s"
                        % (str(a[0]), str(match_with), str(b[idx]))
                    )
                    print("\t", perm, dir)
                    all_matches.add((perm, dir, move))

    # I don't need to find all matches;
    # but in order to confirm the validity of my solution,
    # I find them all and assert that there is no more than one.
    match_cnt = len(all_matches)
    if match_cnt == 0:
        return None
    elif match_cnt == 1:
        return tuple(all_matches)[0]
    else:
        print(all_matches)
        raise ValueError("Multiple (%d) matches found with %s" % (match_cnt, str(b)))


# @pytest.fixture
def sample_input():
    return {
        0: [
            (404, -588, -901),
            (528, -643, 409),
            (-838, 591, 734),
            (390, -675, -793),
            (-537, -823, -458),
            (-485, -357, 347),
            (-345, -311, 381),
            (-661, -816, -575),
            (-876, 649, 763),
            (-618, -824, -621),
            (553, 345, -567),
            (474, 580, 667),
            (-447, -329, 318),
            (-584, 868, -557),
            (544, -627, -890),
            (564, 392, -477),
            (455, 729, 728),
            (-892, 524, 684),
            (-689, 845, -530),
            (423, -701, 434),
            (7, -33, -71),
            (630, 319, -379),
            (443, 580, 662),
            (-789, 900, -551),
            (459, -707, 401),
        ],
        1: [
            (686, 422, 578),
            (605, 423, 415),
            (515, 917, -361),
            (-336, 658, 858),
            (95, 138, 22),
            (-476, 619, 847),
            (-340, -569, -846),
            (567, -361, 727),
            (-460, 603, -452),
            (669, -402, 600),
            (729, 430, 532),
            (-500, -761, 534),
            (-322, 571, 750),
            (-466, -666, -811),
            (-429, -592, 574),
            (-355, 545, -477),
            (703, -491, -529),
            (-328, -685, 520),
            (413, 935, -424),
            (-391, 539, -444),
            (586, -435, 557),
            (-364, -763, -893),
            (807, -499, -711),
            (755, -354, -619),
            (553, 889, -390),
        ],
        2: [
            (649, 640, 665),
            (682, -795, 504),
            (-784, 533, -524),
            (-644, 584, -595),
            (-588, -843, 648),
            (-30, 6, 44),
            (-674, 560, 763),
            (500, 723, -460),
            (609, 671, -379),
            (-555, -800, 653),
            (-675, -892, -343),
            (697, -426, -610),
            (578, 704, 681),
            (493, 664, -388),
            (-671, -858, 530),
            (-667, 343, 800),
            (571, -461, -707),
            (-138, -166, 112),
            (-889, 563, -600),
            (646, -828, 498),
            (640, 759, 510),
            (-630, 509, 768),
            (-681, -892, -333),
            (673, -379, -804),
            (-742, -814, -386),
            (577, -820, 562),
        ],
        3: [
            (-589, 542, 597),
            (605, -692, 669),
            (-500, 565, -823),
            (-660, 373, 557),
            (-458, -679, -417),
            (-488, 449, 543),
            (-626, 468, -788),
            (338, -750, -386),
            (528, -832, -391),
            (562, -778, 733),
            (-938, -730, 414),
            (543, 643, -506),
            (-524, 371, -870),
            (407, 773, 750),
            (-104, 29, 83),
            (378, -903, -323),
            (-778, -728, 485),
            (426, 699, 580),
            (-438, -605, -362),
            (-469, -447, -387),
            (509, 732, 623),
            (647, 635, -688),
            (-868, -804, 481),
            (614, -800, 639),
            (595, 780, -596),
        ],
        4: [
            (727, 592, 562),
            (-293, -554, 779),
            (441, 611, -461),
            (-714, 465, -776),
            (-743, 427, -804),
            (-660, -479, -426),
            (832, -632, 460),
            (927, -485, -438),
            (408, 393, -506),
            (466, 436, -512),
            (110, 16, 151),
            (-258, -428, 682),
            (-393, 719, 612),
            (-211, -452, 876),
            (808, -476, -593),
            (-575, 615, 604),
            (-485, 667, 467),
            (-680, 325, -822),
            (-627, -443, -432),
            (872, -547, -609),
            (833, 512, 582),
            (807, 604, 487),
            (839, -516, 451),
            (891, -625, 532),
            (-652, -548, -490),
            (30, -46, -14),
        ],
    }


def test_find_match():
    assert ((0, 1, 2), (1, 1, 1), (-10, -10, -10)) == find_match(
        [(0, 1, 3), (1, 4, 9), (-1, -1, -1)],
        [(10, 11, 13), (11, 14, 19), (9, 9, 9), (-999, -999, -999)],
        min_overlap=2,
    )
    assert None == find_match(
        [(0, 1, 3), (1, 4, 9), (-1, -1, -1)],
        [(10, 11, 13), (11, 14, 19), (9, 8, 9), (-999, -999, -999)],
        min_overlap=2,
    )


def test_find_match2(sample_input):
    assert ((0, 1, 2), (-1, 1, -1), (68, -1246, -43)) == find_match(
        sample_input[0], sample_input[1]
    )
    assert None == find_match(sample_input[0], sample_input[2])


def spread_transformations(t, target):
    ret = {target: [((0, 1, 2), (1, 1, 1), (0, 0, 0))]}
    in_queue = set()
    Q = [(next, target) for next in t[target].keys()]
    while len(Q) > 0:
        scanner, parent = Q[-1]
        Q.pop()
        ret[scanner] = [t[parent][scanner]] + ret[parent]
        for next in t[scanner].keys():
            if next not in in_queue:
                Q.insert(0, (next, scanner))
                in_queue.add(next)

    assert ret.keys() == t.keys()
    return ret


def test_spread_transformations():
    tid = ((0, 1, 2), (1, 1, 1), (0, 0, 0))
    t21 = ((0, 1, 2), (-1, -1, -1), (5, 55, 555))
    t32 = ((2, 1, 0), (1, 1, 1), (7, 77, 777))
    t = {1: {2: t21}, 2: {3: t32}, 3: {}}
    res = spread_transformations(t, 1)
    assert {
        1: [tid],
        2: [t21, tid],
        3: [t32, t21, tid],
    } == res


def part1(pinp, min_overlap=12):
    transformations = {k: {} for k in pinp.keys()}
    for scanner, points in pinp.items():
        for scanner2, points2 in pinp.items():
            if scanner == scanner2:
                continue
            match = find_match(points, points2, min_overlap=min_overlap)
            if match:
                transformations[scanner][scanner2] = match

    first = min(pinp.keys())
    import pprint

    pprint.pprint(transformations)
    t = spread_transformations(transformations, first)

    all_points = set()
    for scanner, trans in t.items():
        for p in pinp[scanner]:
            for tr in trans:
                p = move(convert(p, *tr[0:2]), tr[2])
            all_points.add(p)

    print("All points in the coordinates of the first scanner (%d):" % len(all_points))
    print(all_points)

    return len(all_points)


def test_part1(sample_input):
    assert 79 == part1(sample_input)


def part2(pinp, min_overlap=12):
    transformations = {k: {} for k in pinp.keys()}
    for scanner, points in pinp.items():
        for scanner2, points2 in pinp.items():
            if scanner == scanner2:
                continue
            match = find_match(points, points2, min_overlap=min_overlap)
            if match:
                transformations[scanner][scanner2] = match

    first = min(pinp.keys())
    import pprint

    pprint.pprint(transformations)
    t = spread_transformations(transformations, first)

    sc = []
    for scanner, trans in t.items():
        p = (0, 0, 0)
        for tr in trans:
            p = move(convert(p, *tr[0:2]), tr[2])
        sc.append(p)

    best = 0
    for a in sc:
        for b in sc:
            d = sum([abs(x) for x in sub(a, b)])
            best = max(best, d)

    return best


if __name__ == "__main__":
    inp = list(fileinput.input())
    pinp = parse(inp)
    # print("Part 1: %d" % part1(pinp))
    print("Part 2: %d" % part2(pinp))
