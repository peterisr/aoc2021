import fileinput


def parse_line(line):
	on_off, ranges = line.split(" ")
	parsed_ranges = map(lambda x: tuple(map(int, x.split("=")[1].split(".."))), ranges.split(","))
	return on_off == "on", *parsed_ranges


def test_parsed_line():
	assert (True, (-1, 1), (-10, 10), (-100, 100)) \
		== parse_line("on x=-1..1,y=-10..10,z=-100..100")
	assert (False, (-2, -1), (0, 1), (2, 4)) \
		== parse_line("off x=-2..-1,y=0..1,z=2..4")


class LeafDimension():
	def __init__(self):
		self.intervals = [] # on intervals

	def count(self):
		cnt = 0
		for l, r, _ in self.intervals:
			cnt += r - l + 1
		return cnt	

	def split(self, new_l, new_r, on):
		new = []

		last_p = None
		last_on = False
		def consider_point(p, on):
			nonlocal last_on, last_p

			if on != last_on:
				if last_on:
					new.append((last_p, p - 1, True))
				last_p = p
				last_on = on

		new_l_cons = False
		new_r_cons = False
		def maybe_consider_new(next_p):
			nonlocal new_l_cons, new_r_cons

			if not new_l_cons and next_p >= new_l:
				consider_point(new_l, on)
				new_l_cons = True

			if not new_r_cons and next_p > new_r and on:
				consider_point(new_r + 1, not on)
				new_r_cons = True

		
		for l, r, _ in self.intervals:
			for p, pon in [(l, True), (r + 1, False)]:
				if new_l <= p <= new_r:
					pon = on

				maybe_consider_new(p)
				consider_point(p, pon)

		maybe_consider_new(1e100)

		print("new intervals: ", new)
		self.intervals = new
		return len(self.intervals)



def test_leaf():
	leaf = LeafDimension()
	assert 0 == leaf.split(1, 10, False)
	assert 1 == leaf.split(1, 10, True)
	assert 2 == leaf.split(20, 30, True)
	assert 2 == leaf.split(31, 35, True)
	assert 3 == leaf.split(31, 32, False)
	assert 1 == leaf.split(-100, 100, True)
	leaf.split(-100, 100, False)
	assert False

if __name__ == '__main__':
	Q = []
	for line in fileinput.line():
		Q.append(parse_line(line.strip()))

	print("Part 1: %d" % part1(Q))
