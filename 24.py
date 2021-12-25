import fileinput
import functools
from multiprocessing import Pool
import os


def chunk(lines):
    # The input consists of 14 blocks with minor differences between each block
    # This function returns those blocks.
    ret = []
    chunk = []
    for l in lines:
        if l.startswith("inp "):
            if len(chunk) > 0:
                ret.append(chunk)
            chunk = []
        chunk.append(l)
    if len(chunk) > 0:
        ret.append(chunk)
    return ret


def test_chunk():
    s = """
		inp w
		add x 0
		inp y
		add z 1
	"""
    lines = [line.strip() for line in s.strip().split("\n")]
    assert [["inp w", "add x 0"], ["inp y", "add z 1"]] == chunk(lines)


def extract_significant_values(blocks):
    # each block only has a few things that change w.r.t. other blocks.
    ret = []
    for block in blocks:
        ret.append(
            (
                int(block[4].split(" ")[-1]),  # divz
                int(block[5].split(" ")[-1]),  # addx
                int(block[-3].split(" ")[-1]),  # addy
            )
        )
    return ret


# x = z_prev % 26 + $addx (10, 11, 12, 14, -4, -7, -9, -10, -15)
# z = z_prev div ($divz (1 or 26))
# x = x != w_inp
# y = 25 * x (0 or 1) + 1
# z = z * y
# y = (w_inp + $addy (1, 4, 5, 6, 7, 8, 10)) * x (0 or 1)
# z = z + y
def alu_block(e, w, z_prev):
    x = int((z_prev % 26 + e[1]) != w)
    y = x * 25 + 1
    z = z_prev // e[0] * y + (w + e[2]) * x
    return z


def test_alu_block():
    # corresponds to block0 from my input
    assert 138 == alu_block((1, 14, 7), 1, 5)


def alu(extracted, w_inp):
    z_prev = 0
    for e, w in zip(extracted, w_inp):
        z_prev = alu_block(e, w, z_prev)
    return z_prev


def solve_shard(extracted, fn_aggr, w_seed):
    z_seed = alu_block(extracted[0], w_seed, 0)

    zs = {z_seed: w_seed}
    for idx, e in enumerate(extracted[1:]):
        # print("Chunk with w_seed = %d progress: %d/%d" % (w_seed, idx + 2, len(extracted)))
        zn = {}
        for w in range(1, 10):
            for z_prev, w_acc in zs.items():
                z = alu_block(e, w, z_prev)
                w_acc = w_acc * 10 + w
                if z in zn:
                    zn[z] = fn_aggr(zn[z], w_acc)
                else:
                    zn[z] = w_acc
        zs = zn
    return zs[0] if 0 in zs else None


# Takes about 30 seconds with Python 3.9 on Ryzen 5800H; 10sec on pypy3 7.3.5.
# Could probably be sped up by early discarding Z values that will not work based on some rules / heuristics
# ... or solve it the proper way by finding more patterns in the input
def solve(extracted, fn_aggr):
    fn = functools.partial(solve_shard, extracted, fn_aggr)
    with Pool(9) as p:
        shard_res = [
            w_acc
            for w_acc in p.imap_unordered(fn, list(range(1, 10)), 1)
            if w_acc is not None
        ]
        if len(shard_res) == 0:
            return None
        else:
            return fn_aggr(shard_res)


def my_input():
    with open(os.path.join(os.path.dirname(__file__), "24.txt"), "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n")]
        return extract_significant_values(chunk(lines))


def test_solve():
    assert 59 == solve(my_input()[-2:], max)
    assert 15 == solve(my_input()[-2:], min)


def part1(lines):
    return solve(lines, max)


def part2(lines):
    return solve(lines, min)


def validate_answer(stdin):
    assert 14 == len(stdin)
    assert all([1 <= int(c) <= 9 for c in stdin])
    assert 0 == alu(my_input(), [int(c) for c in stdin])


def test_validate_part1():
    validate_answer("29599469991739")


def test_validate_part2():
    validate_answer("17153114691118")


if __name__ == "__main__":
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    extracted = extract_significant_values(chunk(lines))
    print("Part 1: %d" % part1(extracted))
    print("Part 2: %d" % part2(extracted))
