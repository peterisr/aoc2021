import heapq


def calc(a, b, c, d):
    return a + b * 10 + c * 100 + d * 1000


def part1():
    # solved by hand
    # A9, C3, D5, A7, B2, C6, C4, B3, B4, D9, A3, A3
    return calc((9 + 7 + 3 + 3), (2 + 3 + 4), (3 + 6 + 4), (5 + 9))


"""
	#############
	#01.2.3.4.56#
	###7#1#5#9###
	  #8#2#6#0#
	  #9#3#7#1#
	  #0#4#8#2#
	  #########
"""


class State:
    @classmethod
    def fromstr(
        cls, top=".......", t1="....", t2="....", t3="....", t4="....", moves=0
    ):
        return cls(tuple(top + t1 + t2 + t3 + t4), moves)

    def __init__(self, d, moves):
        assert len(d) == 23, "".join(d)
        self.d = d
        self.moves = moves

    def free_top_places(self):
        for t in range(7):
            if self.d[t] == ".":
                yield t

    def is_clear_path(self, tower, top, incl=True):
        tower_first_left = 1 + tower
        tower_first_right = tower_first_left + 1
        if top <= tower_first_left:
            # going left
            for i in range(tower_first_left, top - int(incl), -1):
                if self.d[i] != ".":
                    return False

        else:
            # going right
            i = tower_first_right
            for i in range(tower_first_right, top + int(incl)):
                if self.d[i] != ".":
                    return False

        return True

    EXPECTED_TOWER = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
    }

    def is_tower_expected(self, t, start_pos=None):
        if start_pos is None:
            start_pos = 7 + t * 4

        end_pos = 7 + (t + 1) * 4
        return all(
            [
                self.EXPECTED_TOWER[self.d[pos]] == t
                for pos in range(start_pos, end_pos)
                if self.d[pos] != "."
            ]
        )

    def tower_first_free(self, t):
        i = 7 + t * 4
        end = 7 + (t + 1) * 4
        while i + 1 < end and self.d[i + 1] == ".":
            i += 1
        assert self.d[i] == "."
        return i

    def yield_tower_moves(self, tmin=0, tmax=3):
        for t in range(tmin, tmax + 1):
            s = 7 + t * 4
            smax = 7 + (t + 1) * 4
            while s < smax and self.d[s] == ".":
                s += 1
            tower_eq = True
            i = s + 1
            while i < smax:
                tower_eq = tower_eq and (self.d[i - 1] == self.d[i])
                i += 1

            tower_correct = self.is_tower_expected(t)
            if not tower_correct and s < smax:
                # could optimize here
                for top in self.free_top_places():
                    if self.is_clear_path(t, top):
                        yield self.move(s, top)

                et = self.EXPECTED_TOWER[self.d[s]]
                if t != et and self.is_tower_expected(et):
                    mi, ma = min(t, et), max(t, et)
                    mi + 2
                    if self.is_clear_path(t, mi + 2) and self.is_clear_path(t, ma + 1):
                        ff = self.tower_first_free(et)
                        yield self.move(s, ff)

    def yield_top_moves(self):
        for i in range(7):
            if self.d[i] == ".":
                continue

            t = self.EXPECTED_TOWER[self.d[i]]
            if self.is_tower_expected(t) and self.is_clear_path(t, i, False):
                ff = self.tower_first_free(t)
                yield self.move(i, ff)

    def yield_next_states(self):
        yield from self.yield_tower_moves()
        yield from self.yield_top_moves()

    def is_done(self):
        if not all([x == "." for x in self.d[0:7]]):
            return False

        for t in range(4):
            exp = self.EXPECTED_TOWER[t]
            t_start = 7 + t * 4
            if not all([x == exp for x in self.d[t_start : (t_start + 4)]]):
                return False

        return True

    def to_tower(self, pos):
        if pos <= 6:
            return None
        else:
            return (pos - 7) // 4

    TOP_ABS = {
        0: 0,
        1: 1,
        2: 3,
        3: 5,
        4: 7,
        5: 9,
        6: 10,
    }
    MOVE_COSTS = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }

    def move(self, src, dst):
        assert self.d[src] != "."
        assert self.d[dst] == "."
        tsrc, tdst = self.to_tower(src), self.to_tower(dst)
        assert tsrc is not None or tdst is not None

        if all([x is not None for x in [tsrc, tdst]]):
            # move: tower to tower
            assert tsrc != tdst
            t_mid = tsrc + 2 if tsrc < tdst else tsrc + 1
            p1 = self.move(src, t_mid)
            p2 = p1.move(t_mid, dst)
            return p2
        else:
            # move: top to tower or tower to top
            tower_pos, top_pos = (src, dst) if tsrc is not None else (dst, src)
            t = tsrc if tsrc is not None else tdst

            t_first = 7 + t * 4
            t_left = t + 1
            t_right = t + 2
            t_top = t_left if top_pos <= t_left else t_right

            moves_tower = tower_pos - t_first + 2
            moves_top = abs(self.TOP_ABS[top_pos] - self.TOP_ABS[t_top])

            moves = moves_tower + moves_top
            move_cost = self.MOVE_COSTS[self.d[src]] * moves
            return self.evolve(move_cost, (src, "."), (dst, self.d[src]))

    def evolve(self, new_moves, *args):
        d = list(self.d)
        for pos, v in args:
            d[pos] = v
        return State(tuple(d), self.moves + new_moves)

    def __eq__(self, other):
        return (
            isinstance(other, State) and self.d == other.d and self.moves == other.moves
        )

    def __lt__(self, other):
        return (self.moves, self.d) < (other.moves, other.d)

    def __str__(self):
        lines = [
            "#############",
            "#{0[0]}{0[1]}.{0[2]}.{0[3]}.{0[4]}.{0[5]}{0[6]}#",
            "  #{0[7]}#{0[11]}#{0[15]}#{0[19]}#",
            "  #{0[8]}#{0[12]}#{0[16]}#{0[20]}#",
            "  #{0[9]}#{0[13]}#{0[17]}#{0[21]}#",
            "  #{0[10]}#{0[14]}#{0[18]}#{0[22]}#",
            "  #########",
            "  moves={1}",
        ]
        return "\n".join(lines).format(self.d, self.moves)

    __repr__ = __str__


def test_state_free_top_places():
    s = State.fromstr()
    assert list(s.free_top_places()) == [0, 1, 2, 3, 4, 5, 6]

    s = State.fromstr(top="A.....C")
    assert list(s.free_top_places()) == [1, 2, 3, 4, 5]


def test_state_is_clear_path():
    s = State.fromstr(top="AB..C..")
    assert s.is_clear_path(1, 0) == False
    assert s.is_clear_path(1, 1) == False

    assert s.is_clear_path(1, 2) == True
    assert s.is_clear_path(1, 3) == True
    assert s.is_clear_path(1, 4) == False
    assert s.is_clear_path(1, 5) == False
    assert s.is_clear_path(1, 6) == False

    assert s.is_clear_path(2, 1) == False
    assert s.is_clear_path(2, 2) == True
    assert s.is_clear_path(2, 3) == True
    assert s.is_clear_path(2, 4) == False


def test_state_is_done():
    s = State.fromstr(top="A......", t1=".AAA", t2="BBBB", t3="CCCC", t4="DDDD")
    assert s.is_done() == False

    s = State.fromstr(top=".......", t1="AAAA", t2="BBBB", t3="CCCC", t4="DDDD")
    assert s.is_done() == True


def test_state_move():
    s = State.fromstr(top="A..B..C", t1="...A", moves=1)
    assert s.move(0, 9) == State.fromstr(top="...B..C", t1="..AA", moves=1 + 5)
    assert s.move(3, 14) == State.fromstr(
        top="A.....C", t1="...A", t2="...B", moves=1 + 5 * 10
    )
    assert s.move(6, 18) == State.fromstr(
        top="A..B...", t1="...A", t3="...C", moves=1 + 8 * 100
    )

    s = State.fromstr(t1="...D", moves=1)
    assert s.move(10, 22) == State.fromstr(t4="...D", moves=1 + (4 + 6 + 4) * 1000)

    s = State.fromstr(t4="...A", moves=1)
    assert s.move(22, 10) == State.fromstr(t1="...A", moves=1 + (4 + 6 + 4) * 1)

    s = State.fromstr(t4=".ABC", moves=1)
    assert s.move(20, 0) == State.fromstr(
        top="A......", t4="..BC", moves=1 + (2 + 8) * 1
    )

    s = State.fromstr(top="A......", t4="..BC", moves=1)
    assert s.move(0, 20) == State.fromstr(t4=".ABC", moves=1 + (2 + 8) * 1)


def test_state_yield_tower_moves():
    s = State.fromstr(top="AB..C..", t1=".BCD")
    assert list(s.yield_tower_moves()) == [
        s.move(8, 2),
        s.move(8, 3),
        s.move(8, 14),
    ]

    s = State.fromstr(top="AB..C..", t1="..AA")
    assert list(s.yield_tower_moves()) == []

    s = State.fromstr(top="AB..C..", t1="..AA", t2="...D")
    assert list(s.yield_tower_moves()) == [
        s.move(14, 2),
        s.move(14, 3),
    ]

    s = State.fromstr(top="ABD.D.C", t1="..AA", t2="...C")
    assert list(s.yield_tower_moves()) == [
        s.move(14, 3),
        s.move(14, 18),
    ]


def test_state_yield_top_moves():
    s = State.fromstr(top="A..B.CD", t1="..AA", t2="...C")
    assert list(s.yield_top_moves()) == [
        s.move(0, 8),  # A
        s.move(5, 18),  # C
    ]


def solve(s):
    res = None
    V = {}
    parent = {}
    Q = [(s, None)]
    while len(Q) > 0:
        (s, ps) = heapq.heappop(Q)
        if s.d in V:
            assert V[s.d] <= s.moves
            continue

        V[s.d] = s.moves
        parent[s.d] = ps

        if s.is_done():
            res = s
            break

        for ns in s.yield_next_states():
            heapq.heappush(Q, (ns, s))

    s = res
    path = []
    while s is not None:
        path.append(s)
        s = parent[s.d]

    path = reversed(path)
    for p in path:
        print(p)

    return res.moves


def test_solve():
    s = State.fromstr(t1="BDDA", t2="CCBD", t3="BBAC", t4="DACA")
    assert solve(s) == 44169


def part2():
    """
    #############
    #...........#
    ###B#B#D#A###
      #D#C#B#A#
      #D#B#A#C#
      #D#C#A#C#
      #########
    """
    s = State.fromstr(t1="BDDD", t2="BCBC", t3="DBAA", t4="AACC")
    return solve(s)


if __name__ == "__main__":
    print("Part 1: %d" % part1())
    print("Part 2: %d" % part2())
