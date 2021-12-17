from enum import IntEnum
import fileinput
import functools
import operator


def hex2bin(s):
    return list(bin(int(s, 16))[2:].zfill(len(s) * 4))


class PacketType(IntEnum):
    LITERAL = 4


class Packet:
    def __init__(self, version, type):
        self.version = version
        self.type = type

    def __repr__(self):
        return f"Packet({self.version}, {self.type})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class LiteralPacket(Packet):
    def __init__(self, version, value):
        super().__init__(version, PacketType.LITERAL)
        self.value = value

    def __repr__(self):
        return f"LiteralPacket({self.version}, {self.type}, {self.value})"


class OperatorPacket(Packet):
    def __init__(self, version, type, subpackets):
        super().__init__(version, type)
        self.subpackets = subpackets

    def __repr__(self):
        return f"OperatorPacket({self.version}, {self.type}, {self.subpackets})"


def num(l, pos, *cnt):
    ret = []
    for c in cnt:
        ret.append(int("".join(l[pos : pos + c]), 2))
        pos = pos + c
    return (min(len(l), pos),) + tuple(ret)


def parse_bin(b, pos, end, max_cnt=None):
    ret = []

    while max_cnt is None or len(ret) < max_cnt:
        remains = end - pos
        if remains == 0:
            break
        elif remains < 16:
            pos_suffix, suffix = num(b, pos, remains)
            if suffix == 0:
                pos = suffix
                break

        pos, version, type = num(b, pos, 3, 3)
        if type == PacketType.LITERAL:
            value = 0
            while True:
                pos, bit, hextet = num(b, pos, 1, 4)
                value *= 16
                value += hextet
                if bit == 0:
                    break
            ret.append(LiteralPacket(version, value))
        else:
            # assuming OperatorPacket
            pos, length_type = num(b, pos, 1)
            if length_type == 0:
                pos, total_len = num(b, pos, 15)

                old_pos = pos
                pos, subpackets = parse_bin(b, pos, pos + total_len)
                assert old_pos + total_len == pos
            else:
                pos, subpacket_count = num(b, pos, 11)
                pos, subpackets = parse_bin(b, pos, end, max_cnt=subpacket_count)
                assert subpacket_count == len(subpackets)
            ret.append(OperatorPacket(version, type, subpackets))

    return pos, ret


def parse(s):
    b = hex2bin(s)
    _, ret = parse_bin(b, 0, len(b))
    return ret


def part1(parsed):
    ret = 0
    for p in parsed:
        ret += p.version
        if hasattr(p, "subpackets"):
            ret += part1(p.subpackets)
    return ret


TYPE_TO_FN = {
    0: sum,
    1: lambda ops: functools.reduce(operator.mul, ops),
    2: min,
    3: max,
    # no 4 #
    5: lambda ops: int(ops[0] > ops[1]),
    6: lambda ops: int(ops[0] < ops[1]),
    7: lambda ops: int(ops[0] == ops[1]),
}


def _part2(p):
    if not hasattr(p, "subpackets"):
        return p.value
    else:
        operands = []
        for sp in p.subpackets:
            operands.append(_part2(sp))

        return TYPE_TO_FN[p.type](operands)


def part2(parsed):
    assert len(parsed) == 1
    return _part2(parsed[0])


def test_hex2bin():
    assert hex2bin("2") == list("0010")
    assert hex2bin("72") == list("01110010")


def test_parse():
    assert parse("D2FE28") == [LiteralPacket(6, 2021)]
    assert parse("38006F45291200") == [
        OperatorPacket(1, 6, [LiteralPacket(6, 10), LiteralPacket(2, 20)])
    ]
    assert parse("EE00D40C823060") == [
        OperatorPacket(
            7, 3, [LiteralPacket(2, 1), LiteralPacket(4, 2), LiteralPacket(1, 3)]
        )
    ]


def test_part1():
    assert part1(parse("8A004A801A8002F478")) == 16
    assert part1(parse("620080001611562C8802118E34")) == 12
    assert part1(parse("C0015000016115A2E0802F182340")) == 23
    assert part1(parse("A0016C880162017C3686B18A3D4780")) == 31


def test_part2():
    assert part2(parse("C200B40A82")) == 3
    assert part2(parse("04005AC33890")) == 54
    assert part2(parse("880086C3E88112")) == 7
    assert part2(parse("CE00C43D881120")) == 9
    assert part2(parse("D8005AC2A8F0")) == 1
    assert part2(parse("F600BC2D8F")) == 0
    assert part2(parse("9C005AC2F8F0")) == 0
    assert part2(parse("9C0141080250320F1802104A08")) == 1


if __name__ == "__main__":
    line = next(fileinput.input())
    line = line.strip()
    parsed = parse(line)
    print("Version number sum is %d" % part1(parsed))
    print("Value of expression is %d" % part2(parsed))
